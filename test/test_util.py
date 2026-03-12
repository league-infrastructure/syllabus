"""Tests for syllabus.util functions."""

from pathlib import Path

from syllabus.util import (
    DISPLAY_MODULES,
    clean_filename,
    extract_metadata_markdown,
    extract_metadata_python,
    extract_rank_string,
    match_rank,
    match_rank_name,
    rand62,
    replace_rank,
)


class TestMatchRank:
    def test_simple_rank(self):
        assert match_rank(Path("10_Hello")) == "10"

    def test_multi_digit_rank(self):
        assert match_rank(Path("100_Hello")) == "100"

    def test_rank_with_letters(self):
        assert match_rank(Path("04b_List_Story")) == "04b"

    def test_no_rank(self):
        assert match_rank(Path("Hello")) is None

    def test_no_underscore(self):
        assert match_rank(Path("10Hello")) is None

    def test_file_extension(self):
        assert match_rank(Path("10_Hello.py")) == "10"


class TestMatchRankName:
    def test_simple(self):
        rank, base = match_rank_name(Path("10_Hello.py"))
        assert rank == "10"
        assert base == "Hello"

    def test_multi_word(self):
        rank, base = match_rank_name(Path("20_Crazy_Tina.py"))
        assert rank == "20"
        assert base == "Crazy_Tina"

    def test_no_match(self):
        rank, base = match_rank_name(Path("README.md"))
        assert rank is None
        assert base is None


class TestCleanFilename:
    def test_removes_rank(self):
        assert clean_filename("10_Hello") == "Hello"

    def test_replaces_underscores(self):
        assert clean_filename("20_Crazy_Tina") == "Crazy Tina"

    def test_replaces_dashes(self):
        assert clean_filename("10_Hello-World") == "Hello World"

    def test_no_rank(self):
        assert clean_filename("Hello_World") == "Hello World"


class TestReplaceRank:
    def test_replace(self):
        result = replace_rank(Path("10_Hello.py"), "20")
        assert result == Path("20_Hello.py")

    def test_no_rank(self):
        result = replace_rank(Path("README.md"), "10")
        assert result == Path("README.md")

    def test_zero_pad(self):
        result = replace_rank(Path("10_Hello.py"), "100")
        assert result == Path("100_Hello.py")


class TestExtractRankString:
    def test_single_level(self):
        assert extract_rank_string(Path("10_Loops")) == "10"

    def test_nested(self):
        result = extract_rank_string(Path("20_Turtles/01_First"))
        assert result == "20/01"


class TestRand62:
    def test_length(self):
        result = rand62(8)
        assert len(result) == 8

    def test_characters(self):
        import string
        valid = set(string.ascii_letters + string.digits)
        result = rand62(100)
        assert all(c in valid for c in result)


class TestExtractMetadataPython:
    def test_comment_metadata(self, tmp_path):
        p = tmp_path / "test.py"
        p.write_text('# name: Hello\n# uid: abc123\nprint("hi")\n')
        md = extract_metadata_python(p)
        assert md["name"] == "Hello"
        assert md["uid"] == "abc123"

    def test_docstring_metadata(self, tmp_path):
        p = tmp_path / "test.py"
        p.write_text('"""\nname: From Docstring\nuid: doc123\n"""\nprint("hi")\n')
        md = extract_metadata_python(p)
        assert md["name"] == "From Docstring"
        assert md["uid"] == "doc123"

    def test_with_doc(self, tmp_path):
        p = tmp_path / "test.py"
        p.write_text('"""\nSome description.\nname: Test\n"""\nprint("hi")\n')
        md, doc = extract_metadata_python(p, with_doc=True)
        assert md["name"] == "Test"
        assert "Some description" in doc


class TestExtractMetadataMarkdown:
    def test_frontmatter(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text("---\nuid: md123\nname: Test Lesson\n---\n\n# Hello\n")
        md = extract_metadata_markdown(p)
        assert md["uid"] == "md123"
        assert md["name"] == "Test Lesson"


class TestDisplayModules:
    def test_known_modules(self):
        assert "turtle" in DISPLAY_MODULES
        assert "guizero" in DISPLAY_MODULES
        assert "pygame" in DISPLAY_MODULES
        assert "tkinter" in DISPLAY_MODULES
