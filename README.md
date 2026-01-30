# AI Document Assistant - RAG System

A Retrieval-Augmented Generation (RAG) system that allows users to ask questions about major tech companies (Tesla, Nvidia, Google, Microsoft, SpaceX) using natural language queries. The system combines document retrieval with generative AI to provide accurate, context-aware answers.

## Features

- **Document Ingestion**: Load and process text documents from a specified directory
- **Vector Search**: Use ChromaDB with Google Gemini embeddings for efficient document retrieval
- **Conversational AI**: Chat interface powered by Google Gemini 3 Flash model
- **Web API**: RESTful Flask API for backend processing
- **Streamlit UI**: User-friendly chat interface for asking questions
- **Conversation History**: Maintains context across multiple questions

## Architecture

The system consists of four main components:

1. **Ingestion Pipeline** (`ingestion_pipeline.py`): Processes documents and creates vector embeddings
2. **Retrieval Pipeline** (`retrival_pipeline.py`): Handles document search and question answering
3. **API Server** (`rag_api.py`): Flask REST API for chat functionality
4. **Streamlit App** (`streamlit_app.py`): Web interface for user interaction

## Prerequisites

- Python 3.8+
- Google AI API key (for Gemini models)
- Git (for version control)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/abhinavppwrk/simple-rag.git
cd rag-document-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirement.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your_google_ai_api_key_here
```

## Usage

### 1. Ingest Documents

Run the ingestion pipeline to process documents and create the vector database:

```bash
python ingestion_pipeline.py
```

This will:
- Load all `.txt` files from the `docs/` directory
- Split documents into chunks
- Generate embeddings using Google Gemini
- Store vectors in ChromaDB

### 2. Start the API Server

```bash
python rag_api.py
```

The API will run on `http://127.0.0.1:5000`

### 3. Launch the Streamlit App

In a new terminal:

```bash
streamlit run streamlit_app.py
```

Access the app at `http://localhost:8501`

## API Endpoints

### POST /chat

Send a question to get an AI-powered answer.

**Request:**
```json
{
  "question": "Who is the CEO of Tesla?"
}
```

**Response:**
```json
{
  "answer": "Elon Musk is the CEO of Tesla."
}
```

## Document Format

Place your documents in the `docs/` directory as `.txt` files. The system currently includes sample documents about:

- Tesla
- Nvidia
- Google
- Microsoft
- SpaceX

## Configuration

You can modify the following parameters in the code:

- **Chunk Size**: Adjust in `ingestion_pipeline.py` (default: 700 characters)
- **Chunk Overlap**: Adjust in `ingestion_pipeline.py` (default: 70 characters)
- **Number of Retrieved Documents**: Adjust `k` parameter in retrievers (default: 3)
- **Embedding Model**: Change model in embedding initialization (default: `models/text-embedding-004`)
- **LLM Model**: Change model in ChatGoogleGenerativeAI (default: `gemini-3-flash-preview`)

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your `GOOGLE_API_KEY` is set correctly in `.env`
2. **No Documents Found**: Check that `docs/` directory exists and contains `.txt` files
3. **Connection Error**: Make sure the Flask API is running before starting Streamlit
4. **Memory Issues**: Reduce chunk size or number of retrieved documents for lower RAM usage

### Database Reset

To reset the vector database:

```bash
rm -rf db/chroma_db/
python ingestion_pipeline.py
```

## Dependencies

- Flask & Flask-CORS: Web API framework
- LangChain: LLM framework and integrations
- ChromaDB: Vector database
- Google Generative AI: Embeddings and chat models
- Streamlit: Web UI framework
- python-dotenv: Environment variable management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [Google Gemini](https://ai.google.dev/)
- UI by [Streamlit](https://streamlit.io/)
