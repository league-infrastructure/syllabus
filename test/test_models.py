"""Tests for syllabus.models."""

import yaml
from pathlib import Path

from syllabus.models import Course, Lesson, Module, LessonSet, to_yaml


class TestLesson:
    def test_create_lesson(self):
        lesson = Lesson(name="Test Lesson")
        assert lesson.name == "Test Lesson"
        assert lesson.display is False
        assert lesson.exercise is None

    def test_new_lesson_from_py(self, simple_source):
        lesson = Lesson.new_lesson(
            simple_source,
            Path("10_Basics/10_Hello.py")
        )
        assert lesson.name == "Hello World"
        assert lesson.uid == "test1234"
        assert lesson.exercise == "10_Basics/10_Hello.py"

    def test_new_lesson_from_md(self, simple_source):
        lesson = Lesson.new_lesson(
            simple_source,
            Path("10_Basics/20_Variables.md")
        )
        assert lesson.name == "Variables Introduction"
        assert lesson.uid == "test5678"
        assert lesson.lesson == "10_Basics/20_Variables.md"


class TestModule:
    def test_create_module(self):
        module = Module(name="Test Module", path="10")
        assert module.name == "Test Module"
        assert module.lessons == []

    def test_sort(self):
        module = Module(name="Test", path="10", lessons=[
            Lesson(name="B", path="20"),
            Lesson(name="A", path="10"),
        ])
        module.sort()
        assert module.lessons[0].name == "A"
        assert module.lessons[1].name == "B"


class TestCourse:
    def test_create_course(self):
        course = Course(name="Test Course")
        assert course.name == "Test Course"
        assert course.modules == []

    def test_to_yaml(self):
        course = Course(
            name="Test",
            uid="abc",
            modules=[
                Module(name="Mod1", path="10", lessons=[
                    Lesson(name="Lesson1", exercise="10/hello.py")
                ])
            ]
        )
        result = course.to_yaml()
        parsed = yaml.safe_load(result)
        assert parsed["name"] == "Test"
        assert parsed["uid"] == "abc"
        assert len(parsed["modules"]) == 1

    def test_to_yaml_file(self, tmp_path):
        course = Course(name="File Test", uid="xyz")
        outpath = tmp_path / "syllabus.yaml"
        course.to_yaml(path=outpath)
        assert outpath.exists()
        parsed = yaml.safe_load(outpath.read_text())
        assert parsed["name"] == "File Test"

    def test_from_yaml(self, golden_dir):
        course = Course.from_yaml(
            golden_dir / "simple-source-syllabus.yaml"
        )
        assert course.name == "Simple Test Course"
        assert len(course.modules) == 2

    def test_to_json(self):
        course = Course(name="JSON Test", uid="j123")
        result = course.to_json()
        import json
        parsed = json.loads(result)
        assert parsed["name"] == "JSON Test"

    def test_sort(self):
        course = Course(name="Test", modules=[
            Module(name="B", path="20"),
            Module(name="A", path="10"),
        ])
        course.sort()
        assert course.modules[0].name == "A"
