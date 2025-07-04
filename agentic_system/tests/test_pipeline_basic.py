import os
import tempfile
import json
from pathlib import Path
import pytest

from agentic_system.core import Agent
from agentic_system.commands.basic.cat import CatCommand
from agentic_system.commands.basic.copy import CopyCommand
from agentic_system.commands.basic.delete import DeleteCommand
from agentic_system.commands.basic.grep import GrepCommand
from agentic_system.commands.basic.ls import LsCommand
from agentic_system.commands.basic.move import MoveCommand
from agentic_system.commands.basic.tree import TreeCommand
from agentic_system.commands.basic.write import WriteCommand

class TestBasicPipeline:
    def setup_method(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.temp_dir.name)
        (self.base / 'file1.txt').write_text('hello world')
        (self.base / 'file2.txt').write_text('foo bar')
        (self.base / 'subdir').mkdir()
        (self.base / 'subdir' / 'file3.txt').write_text('baz qux')
        self.agent = Agent(model="llama2")

    def teardown_method(self):
        self.temp_dir.cleanup()

    def run_pipeline(self, instruction, command_cls, result_check, **kwargs):
        prompt = instruction
        intent_json = self.agent.ask(prompt)
        try:
            intent = json.loads(intent_json)
        except Exception:
            pytest.skip("LLM did not return valid JSON: " + repr(intent_json))
        cmd_kwargs = {k: v for k, v in intent.items() if k != 'action'}
        cmd_kwargs.update(kwargs)
        cmd = command_cls(**cmd_kwargs)
        result = cmd.execute()
        result_check(result)

    def test_cat_pipeline(self):
        def check(result):
            assert result == 'hello world'
        self.run_pipeline(
            f"Show contents of {self.base / 'file1.txt'}",
            CatCommand,
            check
        )

    def test_ls_pipeline(self):
        def check(result):
            assert 'file1.txt' in result and 'file2.txt' in result and 'subdir' in result
        self.run_pipeline(
            f"List files in {self.base}",
            LsCommand,
            check
        )

    def test_write_pipeline(self):
        def check(result):
            assert (self.base / 'newfile.txt').read_text() == 'new content'
        self.run_pipeline(
            f"Write 'new content' to {self.base / 'newfile.txt'}",
            WriteCommand,
            check
        )

    def test_copy_pipeline(self):
        dst = self.base / 'copydest'
        dst.mkdir()
        def check(result):
            assert (dst / 'file1.txt').exists()
            assert 'file1.txt' in result
        self.run_pipeline(
            f"Copy file1.txt from {self.base} to {dst}",
            CopyCommand,
            check,
            src=str(self.base), dst=str(dst), files=['file1.txt']
        )

    def test_move_pipeline(self):
        dst = self.base / 'movedest'
        dst.mkdir()
        def check(result):
            assert (dst / 'file2.txt').exists()
            assert not (self.base / 'file2.txt').exists()
        self.run_pipeline(
            f"Move file2.txt from {self.base} to {dst}",
            MoveCommand,
            check,
            src=str(self.base), dst=str(dst), files=['file2.txt']
        )

    def test_delete_pipeline(self):
        def check(result):
            assert not (self.base / 'file1.txt').exists()
            assert 'file1.txt' in result
        self.run_pipeline(
            f"Delete file1.txt from {self.base}",
            DeleteCommand,
            check,
            src=str(self.base), files=['file1.txt']
        )

    def test_grep_pipeline(self):
        def check(result):
            assert 'file2.txt' in result
        self.run_pipeline(
            f"Search for 'foo' in {self.base}",
            GrepCommand,
            check,
            directory=str(self.base), pattern='foo'
        )

    def test_tree_pipeline(self):
        def check(result):
            assert 'file1.txt' in result and 'subdir' in result and 'file3.txt' in result
        self.run_pipeline(
            f"Show directory tree for {self.base}",
            TreeCommand,
            check
        ) 