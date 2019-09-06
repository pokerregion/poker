from pathlib import Path
import pytest


@pytest.fixture
def testdir():
    return Path(__file__).parent
