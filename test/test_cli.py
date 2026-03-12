"""Tests for the CLI using Click's CliRunner."""

import os
from pathlib import Path

from click.testing import CliRunner

from syllabus.cli.main import cli


class TestCLI:
    def test_version(self, simple_source):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["-l", str(simple_source), "version"]
        )
        assert result.exit_code == 0
        assert "Syllabus CLI version" in result.output

    def test_compile_simple(self, simple_source):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["-l", str(simple_source), "compile"]
        )
        assert result.exit_code == 0
        assert "Course YAML written to" in result.output

    def test_check_valid(self, simple_source):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["-l", str(simple_source), "check"]
        )
        assert result.exit_code == 0

    def test_check_invalid(self, tmp_path):
        bad_dir = tmp_path / "bad"
        bad_dir.mkdir()
        (bad_dir / "stray.py").write_text("x = 1\n")
        runner = CliRunner()
        result = runner.invoke(cli, ["-l", str(bad_dir), "check"])
        assert result.exit_code == 1

    def test_renumber_dryrun(self, simple_source):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["-v", "-l", str(simple_source), "renumber", "-d"]
        )
        assert result.exit_code == 0

    def test_regroup_dryrun(self, simple_source):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["-v", "-l", str(simple_source), "regroup", "-d"]
        )
        assert result.exit_code == 0

    def test_meta_dryrun(self, simple_source):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["-v", "-l", str(simple_source), "meta", "-d"]
        )
        assert result.exit_code == 0
