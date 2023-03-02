from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn
import zipfile
import csv
from io import BytesIO, StringIO
import asyncio


REQUEST_LATENCY_SECONDS = 1
app = FastAPI()


@app.get("/download/{data_id}")
async def get_zipped(data_id: int):
    # get csv data (from db for example)
    csv_string = create_csv_string()
    zipped = zip_string(file_name=f"{data_id}.csv", data=csv_string)

    await asyncio.sleep(REQUEST_LATENCY_SECONDS)

    return StreamingResponse(
        iter([zipped.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment;filename={data_id}.zip"},
    )


def create_csv_string() -> StringIO:
    """
    dummy stringIO object representing a CSV
    """
    fstream = StringIO()
    data = [("price", 1), ("generation", 2), ("stuff", 3)]
    csv.writer(fstream).writerows(data)
    return fstream


def zip_string(file_name: str, data: StringIO) -> BytesIO:
    """
    Use zipfile to generate zipped bytes buffer
    """
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "a", zipfile.ZIP_DEFLATED, False) as zip:
        zip.writestr(file_name, data.getvalue())

    return buffer


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)
    print("running")
