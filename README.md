# tinypybits
Repository for minimal examples for some python problems and solution ideas

## I/O
_Reading, writting, transfering data_

how to zip data (for example csv) in memory into bytes buffer that can be saved on disk:
- [in_memory_zip.py](/io/in_memory_zip.py)

how to zip data (for example csv) in memory into bytes buffer that and served with FastAPI streaming response. After starting the server you can try downloading by visiting your browser at `http://127.0.0.1:8005/download/1` or with curl `curl http://127.0.0.1:8005/download/1 --output 1.zip`
- [in_memory_zip_fastapi.py](/io/in_memory_zip_fastapi.py)