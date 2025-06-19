import ollama
import pathlib
import sys
from langchain_ollama import ChatOllama
from langchain.text_splitter import MarkdownTextSplitter
from langchain_ollama import OllamaEmbeddings  # Updated import
from langchain_community.vectorstores import FAISS  # Updated import
from langchain.chains import RetrievalQA

def setup_llm():
    # Initialize the LLM
    local_llm = "mistral"
    llm = ChatOllama(model=local_llm, temperature=0)
    return llm

def process_markdown_files():
    # Read all markdown files from the markdown_docs folder
    markdown_folder = pathlib.Path("markdown_docs")
    all_content = []
    
    print("Reading markdown files...")
    for md_file in markdown_folder.glob("*.md"):
        print(f"Processing: {md_file.name}")
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            all_content.append(content)
    
    return "\n\n".join(all_content)

def create_qa_chain():
    # Initialize components
    llm = setup_llm()
    embeddings = OllamaEmbeddings(model="mistral")
    
    # Process markdown files
    content = process_markdown_files()
    
    # Split and create vector store
    text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(content)
    vector_store = FAISS.from_texts(chunks, embeddings)
    
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3})
    )

def main():
    # Check if a question was provided
    if len(sys.argv) < 2:
        print("Please provide a question as an argument")
        print("Example: python ask_about_docs.py 'What is the main content?'")
        sys.exit(1)

    # Get the question from command line arguments
    question = " ".join(sys.argv[1:])
    
    # Create QA chain
    print("Initializing QA system...")
    qa_chain = create_qa_chain()
    
    # Get answer
    try:
        result = qa_chain.invoke({"query": question})  # Updated to use invoke
        print("\nAnswer:", result["result"])
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please make sure Ollama is running (ollama serve)")

if __name__ == "__main__":
    main()