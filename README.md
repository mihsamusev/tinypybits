# tinypybits
Repository for minimal examples for some python problems and solution ideas

## I/O
_Reading, writting, transfering data_

How to zip data (for example csv) in memory into bytes buffer that can be saved on disk:
- [in_memory_zip.py](/io/in_memory_zip.py)

How to zip data (for example csv) in memory into bytes buffer that and served with FastAPI streaming response. After starting the server you can try downloading by visiting your browser at `http://127.0.0.1:8005/download/1` or with curl:
```bash
curl http://127.0.0.1:8005/download/1 --output 1.zip
```

- [in_memory_zip_fastapi.py](/io/in_memory_zip_fastapi.py)

How to create pandas dataframes with its synchronous read API but asynchronously
- `.csv` from HTTP [async_pandas_from_http.py](/io/async_pandas_from_http.py)
- `.csv` from filesystem with [aiofiles](https://github.com/Tinche/aiofiles) -  [async_pandas_from_filesystem.py](/io/async_pandas_from_filesystem.py)

How to support reading pandas dataframes of multiple formats with a single function
- TODObump
