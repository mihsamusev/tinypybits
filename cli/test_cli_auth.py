from typer.testing import CliRunner
from cli import app

runner = CliRunner()


def test_app():
    results = runner.invoke(app)
    assert results.stdout == "hello\n"
