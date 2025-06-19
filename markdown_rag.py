import torch
import ollama
import os
from openai import OpenAI
import argparse
from pathlib import Path

# ANSI escape codes for colors
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

def process_markdown_folder(folder_path):
    """Process all markdown files in a folder and return combined content"""
    print(f"Processing markdown files in: {folder_path}")
    all_content = []
    
    # Get all .md files in the folder
    md_files = list(Path(folder_path).glob('*.md'))
    print(f"Found {len(md_files)} markdown files")
    
    for md_file in md_files:
        print(f"Processing: {md_file.name}")
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Split into lines and filter out empty lines
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            all_content.extend(lines)
            print(f"  - Added {len(lines)} lines from {md_file.name}")
    
    print(f"Total lines processed: {len(all_content)}")
    return all_content

def get_relevant_context(rewritten_input, vault_embeddings, vault_content, top_k=3):
    if vault_embeddings.nelement() == 0:
        return []
    input_embedding = ollama.embeddings(model='mistral', prompt=rewritten_input)["embedding"]
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
    top_k = min(top_k, len(cos_scores))
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context

def ollama_chat(user_input, system_message, vault_embeddings, vault_content, conversation_history):
    relevant_context = get_relevant_context(user_input, vault_embeddings, vault_content, top_k=3)
    if relevant_context:
        context_str = "\n".join(relevant_context)
        print("Context Pulled from Documents: \n\n" + CYAN + context_str + RESET_COLOR)
    else:
        print(CYAN + "No relevant context found." + RESET_COLOR)
    
    user_input_with_context = user_input
    if relevant_context:
        user_input_with_context = context_str + "\n\n" + user_input
    
    conversation_history.append({"role": "user", "content": user_input_with_context})
    
    messages = [
        {"role": "system", "content": system_message},
        *conversation_history
    ]
    
    response = client.chat.completions.create(
        model="mistral",
        messages=messages
    )
    
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="Markdown RAG Chat System with Mistral")
    parser.add_argument("--folder", required=True, help="Path to folder containing markdown files")
    args = parser.parse_args()

    # Initialize Ollama client
    client = OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='mistral'
    )

    # Process markdown files
    vault_content = process_markdown_folder(args.folder)

    # Generate embeddings for the vault content
    print("Generating embeddings...")
    vault_embeddings = []
    for content in vault_content:
        if content.strip():  # Skip empty lines
            response = ollama.embeddings(model='mistral', prompt=content)
            vault_embeddings.append(response["embedding"])

    vault_embeddings_tensor = torch.tensor(vault_embeddings)
    print(f"Generated {len(vault_embeddings)} embeddings")

    # Conversation loop
    conversation_history = []
    system_message = "You are a helpful assistant that is an expert at extracting the most useful information from a given text"

    while True:
        user_input = input(YELLOW + "Ask a question about your markdown files (or type 'quit' to exit): " + RESET_COLOR)
        if user_input.lower() == 'quit':
            break

        response = ollama_chat(user_input, system_message, vault_embeddings_tensor, vault_content, conversation_history)
        print(NEON_GREEN + "Response: \n\n" + response + RESET_COLOR)

if __name__ == "__main__":
    main()