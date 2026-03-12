"""Tests for syllabus.sync functions."""

import os
from pathlib import Path

import pytest

from syllabus.sync import (
    check_structure,
    compile_syllabus,
    is_lesson,
    is_lesson_set,
    is_module,
    renumber_lessons,
    regroup_lessons,
    what_is,
)


class TestCheckStructure:
    def test_valid_structure(self, simple_source):
        assert check_structure(simple_source) is True

    def test_not_a_directory(self, tmp_path):
        fake = tmp_path / "nonexistent"
        with pytest.raises(ValueError, match="is not a directory"):
            check_structure(fake)

    def test_loose_file_at_top(self, tmp_path):
        lessons = tmp_path / "lessons"
        lessons.mkdir()
        (lessons / "10_Module").mkdir()
        (lessons / "stray.py").write_text("x = 1\n")
        with pytest.raises(ValueError, match="Unexpected file"):
            check_structure(lessons)

    def test_unranked_directory(self, tmp_path):
        lessons = tmp_path / "lessons"
        lessons.mkdir()
        (lessons / "NoRank").mkdir()
        with pytest.raises(ValueError, match="missing rank prefix"):
            check_structure(lessons)


class TestIsLesson:
    def test_file_with_rank(self, simple_source):
        p = simple_source / "10_Basics" / "10_Hello.py"
        assert is_lesson(p)

    def test_file_without_rank(self, simple_source):
        p = simple_source / "10_Basics" / "README.md"
        assert not is_lesson(p)


class TestIsModule:
    def test_module_dir(self, simple_source):
        assert is_module(simple_source / "10_Basics") is True

    def test_non_module(self, simple_source):
        assert is_module(simple_source / "README.md") is False


class TestWhatIs:
    def test_lesson_file(self, simple_source):
        result = what_is(simple_source / "10_Basics" / "10_Hello.py")
        assert result == "LF"

    def test_module(self, simple_source):
        result = what_is(simple_source / "10_Basics")
        assert result == "MO"

    def test_readme(self, simple_source):
        result = what_is(simple_source / "README.md")
        assert result == "RM"


class TestCompileSyllabus:
    def test_compile_simple(self, simple_source):
        course = compile_syllabus(simple_source)
        assert course.name == "Simple Test Course"
        assert course.description == "A simple test course"
        assert len(course.modules) == 2
        assert course.modules[0].name == "Basics"
        assert course.modules[1].name == "Advanced"

    def test_compile_lessons(self, lessons_source):
        course = compile_syllabus(lessons_source)
        assert course.name == "Your First Lessons in Python"
        assert len(course.modules) == 2
        assert course.modules[0].name == "Yeah Loops"

    def test_golden_master_simple(self, simple_source, golden_dir):
        course = compile_syllabus(simple_source)
        actual = course.to_yaml()
        expected = (golden_dir / "simple-source-syllabus.yaml").read_text()
        assert actual == expected, (
            f"Compiled output differs from golden master.\n"
            f"Expected:\n{expected}\nActual:\n{actual}"
        )

    def test_golden_master_lessons(self, lessons_source, golden_dir):
        course = compile_syllabus(lessons_source)
        actual = course.to_yaml()
        expected = (
            golden_dir / "lessons-source-syllabus.yaml"
        ).read_text()
        assert actual == expected, (
            f"Compiled output differs from golden master.\n"
            f"Expected:\n{expected}\nActual:\n{actual}"
        )


class TestRenumberLessons:
    def test_renumber_increment_100(self, simple_source, golden_dir):
        renumber_lessons(simple_source, increment=100, dryrun=False)

        # Build file listing
        listing = []
        for root, dirs, files in os.walk(simple_source):
            for f in sorted(files):
                listing.append(
                    str(Path(root, f).relative_to(simple_source))
                )
        actual = "\n".join(sorted(listing)) + "\n"
        expected = (
            golden_dir / "simple-source-renumber100-listing.txt"
        ).read_text()
        assert actual == expected, (
            f"Directory listing after renumber differs from golden.\n"
            f"Expected:\n{expected}\nActual:\n{actual}"
        )

    def test_renumber_preserves_content(self, simple_source):
        original = (
            simple_source / "10_Basics" / "10_Hello.py"
        ).read_text()
        renumber_lessons(simple_source, increment=10, dryrun=False)
        renamed = (
            simple_source / "10_Basics" / "10_Hello.py"
        ).read_text()
        assert renamed == original


class TestRegroupLessons:
    def test_regroup_creates_directories(self, lessons_source):
        """The lessons-source has 20_Crazy_Tina.py and 20_Crazy_Tina.md
        in the Loops module which should be regrouped."""
        regroup_lessons(lessons_source, dryrun=False)
        grouped_dir = lessons_source / "10_Loops" / "20_Crazy_Tina"
        assert grouped_dir.is_dir(), (
            f"Expected regrouped directory {grouped_dir} to exist"
        )

    def test_regroup_dryrun_no_changes(self, lessons_source):
        """Dry run should not create any new directories."""
        before = set(str(p) for p in lessons_source.rglob("*"))
        regroup_lessons(lessons_source, dryrun=True)
        after = set(str(p) for p in lessons_source.rglob("*"))
        assert before == after
