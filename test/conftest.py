"""Shared pytest fixtures for syllabus tests."""

import shutil
from pathlib import Path

import pytest

TEST_DIR = Path(__file__).parent


@pytest.fixture
def simple_source(tmp_path: Path) -> Path:
    """Copy the simple-source fixture to a temp directory."""
    dest = tmp_path / "simple-source"
    shutil.copytree(TEST_DIR / "simple-source", dest)
    return dest


@pytest.fixture
def lessons_source(tmp_path: Path) -> Path:
    """Copy the lessons-source fixture to a temp directory."""
    dest = tmp_path / "lessons-source"
    shutil.copytree(TEST_DIR / "lessons-source", dest)
    return dest


@pytest.fixture
def golden_dir() -> Path:
    """Return the path to the golden master directory."""
    return TEST_DIR / "golden"
