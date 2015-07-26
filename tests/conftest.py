# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

from pathlib import Path
import pytest


@pytest.fixture
def testdir():
    return Path(__file__).parent
