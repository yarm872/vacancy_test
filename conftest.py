import pytest
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser", action="store", default="chrome", help="chrome or firefox"
    )

    parser.addoption(
        "--browser_version", action="store", default=None, help="Версия браузера"
    )