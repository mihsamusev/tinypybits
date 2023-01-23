import typer
import requests

ENDPOINT = "http://localhost:8888"
app = typer.Typer()

@app.command()
def hello():
    response = requests.get(url=ENDPOINT)
    print(response.json())

if __name__ == "__main__":
    app()