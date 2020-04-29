from pathlib import Path
import pytest


@pytest.fixture
def test_dir():
    return Path(__file__).parent
