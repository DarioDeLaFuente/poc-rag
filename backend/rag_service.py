from langchain_ollama import ChatOllama
from langchain.text_splitter import MarkdownTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List



import pathlib

app = FastAPI()

# Add CORS middleware for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust if your frontend runs elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    text: str

class Questions(BaseModel):
    questions: List[str]

# Initialize components
llm = ChatOllama(model="mistral", temperature=0)
embeddings = OllamaEmbeddings(model="mistral")

def get_qa_chain():
    markdown_folder = pathlib.Path("markdown_docs")
    all_content = []

    if not markdown_folder.exists():
        raise Exception(f"Folder 'markdown_docs' not found. Please create it and add your markdown files.")

    md_files = list(markdown_folder.glob("*.md"))
    if not md_files:
        raise Exception(f"No markdown files found in 'markdown_docs' folder. Please add some .md files.")

    print(f"Found {len(md_files)} markdown files")
    for md_file in md_files:
        print(f"Processing: {md_file.name}")
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            all_content.append(content)

    if not all_content:
        raise Exception("No content found in markdown files")

    text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text("\n\n".join(all_content))

    if not chunks:
        raise Exception("No text chunks created from markdown files")

    print(f"Created {len(chunks)} text chunks")
    vector_store = FAISS.from_texts(chunks, embeddings)

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3})
    )

# Initialize QA chain
try:
    qa_chain = get_qa_chain()
except Exception as e:
    print(f"Error initializing QA chain: {str(e)}")
    qa_chain = None

@app.post("/ask")
async def ask_question(question: Question):
    if qa_chain is None:
        return {"error": "QA system not properly initialized. Please check the server logs."}
    try:
        result = qa_chain.invoke({"query": question.text})
        return {"answer": result["result"]}
    except Exception as e:
        return {"error": str(e)}

@app.post("/ask-multi")
async def ask_multiple_questions(questions: Questions):
    if qa_chain is None:
        return {"error": "QA system not properly initialized. Please check the server logs."}
    answers = []
    for q in questions.questions:
        try:
            result = qa_chain.invoke({"query": q})
            answers.append({"question": q, "answer": result["result"]})
        except Exception as e:
            answers.append({"question": q, "error": str(e)})
    return {"results": answers}