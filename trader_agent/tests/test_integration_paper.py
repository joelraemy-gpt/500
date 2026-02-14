from typer.testing import CliRunner

from trader_agent.main import app


def test_paper_mode_e2e() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["paper", "--symbols", "AAPL", "--iterations", "3"])
    assert result.exit_code == 0
    assert "paper run complete" in result.stdout
