import io
import zipfile
import csv


def create_csv_string() -> io.StringIO:
    """
    dummy stringIO object representing a CSV
    """
    fstream = io.StringIO()
    data = [("price", 1), ("generation", 2), ("stuff", 3)]
    csv.writer(fstream).writerows(data)
    return fstream


def zip_string(file_name: str, data: io.StringIO) -> io.BytesIO:
    """
    Use zipfile to generate zipped bytes buffer
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "a", zipfile.ZIP_DEFLATED, False) as zip:
        zip.writestr(file_name, data.getvalue())

    return buffer


def main():
    s = create_csv_string()
    zipped = zip_string(file_name="1.csv", data=s)

    # save zip (or stream it)
    with open("test.zip", "wb") as fout:
        fout.write(zipped.getvalue())


if __name__ == "__main__":
    main()
