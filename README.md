# FastAPI + React + OpenAI

- [Backend](backend/README.md)
- [Frontend](frontend/README.md)

ai-assistant
├── backend
| ├── src
| | ├── main.py
| | ├── config.py
| | ├── routes
| | | └── websocket.py
| | ├── services
| | | ├── openai_service.py
| | | └── rag_service.py # Service for RAG functionalities
| | └── data_processing # Directory for data processing scripts  
| | └── document_ingestion.py # Script for ingesting documents
| ├── data # Directory for storing raw and processed data
| | ├── raw # Raw, unprocessed documents
| | └── processed # Processed and indexed documents
| └── ... (other backend files and directories)
├── frontend
| ├── src  
| | ├── App.js
| | └── ... (other frontend files and directories)
| └── ... (other frontend files and directories)
