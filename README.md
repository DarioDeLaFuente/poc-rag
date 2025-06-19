
### POC - RAG
---

### 5. Run the backend

From the root directory, start the backend:

```bash
uvicorn backend.rag_service:app --reload
```

- The API will be available at [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 6. Set up and run the frontend

```bash
cd frontend
npm install
npm run dev
```

- The frontend will be available at [http://localhost:5173](http://localhost:5173)

---

## Usage

- Open [http://localhost:5173](http://localhost:5173) in your browser.
- Ask questions about your documents, select from predefined questions, or write your own.
- All answers will be in Norwegian.
- Use the `/generate-nav-soknad` endpoint to generate formal NAV applications (see backend code for details).

---

## Troubleshooting

- **Port already in use:**  
  Kill the process using the port (e.g., `kill $(lsof -t -i:8000)`).
- **Ollama not running:**  
  Start with `ollama serve`.
- **No markdown files found:**  
  Add `.md` files to `markdown_docs/` and restart the backend.
- **CORS errors:**  
  Ensure CORS is enabled in `rag_service.py` and both frontend/backend are on `localhost`.
- **Reactivate your virtual environment and reinstall packages if needed:**
  ```bash
  source .venv/bin/activate
  pip install ollama langchain langchain-ollama faiss-cpu
  ```

---

## Project Structure

├── backend/
│ └── rag_service.py # FastAPI backend with RAG endpoints
├── frontend/
│ └── src/components/rag/ # React components (RagChat, PredefinedQuestions, etc.)
├── markdown_docs/ # Your .md files for RAG
├── pdf-rag-reader.py # Script to convert PDFs to markdown
├── README.md
└── ...


---

## Example API Endpoints

- **Single question:** `POST /ask`  
  `{ "text": "Hva kan jeg få dekket for hjelpemidler som solbriller?" }`
- **Multiple questions:** `POST /ask-multi`  
  `{ "questions": ["Hva kan jeg få dekket for hjelpemidler som solbriller?", "Hva er hovedinnholdet?"] }`
- **NAV søknad generation:** `POST /generate-nav-soknad`  
  (See backend for required fields)

---

## Credits

- [LangChain](https://github.com/langchain-ai/langchain)
- [Ollama](https://ollama.com/)
- [Mistral](https://mistral.ai/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Vite](https://vitejs.dev/)
- [React](https://react.dev/)

---

## License

MIT License

---

## Contact

For questions or contributions, open an issue or contact [Dario].



Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

## Ollama 
# Pull popular models
ollama pull mistral

# List installed models
ollama list

# Start an interactive chat
ollama run mistral

Then install the required packages:
pip install ollama langchain langchain-ollama faiss-cpu

# Ask for specific tasks
ollama run mistral "Write a Python script to analyze stock prices"


# Run the script:
Apply to raede.md

python markdown_rag.py --folder markdown_docs

# The script will:
Process all .md files in the specified folder
Generate embeddings for all the content
Allow you to ask questions about any of the content in your markdown files
Show relevant context from the files in the responses

markdown_docs/
  ├── report.md
  ├── notes.md
  └── other_docs.md

# Make the .md 
run :
python3 pdf-rag-reader.py


Run the backend:
rag_service....

Run:
uvicorn rag_service:app --reload
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)


Updating reg:
You need to reactivate your virtual environment and reinstall the required packages. 
Reactivate your virtual environment:
source .venv/bin/activate

Then install the required packages:
pip install ollama langchain langchain-ollama faiss-cpu

Stop and restart Ollama (ollama serve)
Stop and restart your backend (uvicorn backend.rag_service:app --reload)
Refresh your frontend
