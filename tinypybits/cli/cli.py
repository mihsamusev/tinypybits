import typer

ENDPOINT = "http://localhost:8888"
app = typer.Typer()


@app.command()
def hello():
    # response = requests.get(url=ENDPOINT)
    # print(response.json())
    print("hello")


if __name__ == "__main__":
    app()


# token in local storage (like temp folder)?
# - yes -> try call API with this token, success?
#       - yes -> do task at hand
#       - no -> ask to login again

# - no -> login -> put token in local storage
