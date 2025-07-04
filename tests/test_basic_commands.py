import os
import shutil
import tempfile
from pathlib import Path
import pytest
import time

from agentic_system.core import Agent
from agentic_system.commands.basic.cat import CatCommand
from agentic_system.commands.basic.copy import CopyCommand
from agentic_system.commands.basic.delete import DeleteCommand
from agentic_system.commands.basic.grep import GrepCommand
from agentic_system.commands.basic.ls import LsCommand
from agentic_system.commands.basic.move import MoveCommand
from agentic_system.commands.basic.tree import TreeCommand
from agentic_system.commands.basic.write import WriteCommand
from agentic_system.commands.basic.pwd import PwdCommand
from agentic_system.commands.basic.mkdir import MkdirCommand
from agentic_system.commands.basic.rmdir import RmdirCommand
from agentic_system.commands.basic.touch import TouchCommand


class TestBasicCommands:
    def setup_method(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.temp_dir.name)
        # Create some files and folders
        (self.base / 'file1.txt').write_text('hello world')
        (self.base / 'file2.txt').write_text('foo bar')
        (self.base / 'subdir').mkdir()
        (self.base / 'subdir' / 'file3.txt').write_text('baz qux')

    def teardown_method(self):
        self.temp_dir.cleanup()

    def test_ls(self):
        cmd = LsCommand(str(self.base))
        output = cmd.execute()
        assert 'file1.txt' in output and 'file2.txt' in output and 'subdir' in output

    def test_cat(self):
        cmd = CatCommand(str(self.base / 'file1.txt'))
        output = cmd.execute()
        assert output == 'hello world'

    def test_write(self):
        cmd = WriteCommand(str(self.base / 'newfile.txt'), content='new content')
        output = cmd.execute()
        assert (self.base / 'newfile.txt').read_text() == 'new content'

    def test_copy(self):
        dst = self.base / 'copydest'
        dst.mkdir()
        cmd = CopyCommand(str(self.base), str(dst), files=['file1.txt'])
        output = cmd.execute()
        assert (dst / 'file1.txt').exists()
        assert 'file1.txt' in output

    def test_move(self):
        dst = self.base / 'movedest'
        dst.mkdir()
        cmd = MoveCommand(str(self.base), str(dst), files=['file2.txt'])
        output = cmd.execute()
        assert (dst / 'file2.txt').exists()
        assert not (self.base / 'file2.txt').exists()

    def test_delete(self):
        cmd = DeleteCommand(str(self.base), files=['file1.txt'])
        output = cmd.execute()
        assert not (self.base / 'file1.txt').exists()
        assert 'file1.txt' in output

    def test_grep(self):
        cmd = GrepCommand(str(self.base), pattern='foo')
        output = cmd.execute()
        assert 'file2.txt' in output

    def test_tree(self):
        cmd = TreeCommand(str(self.base))
        output = cmd.execute()
        assert 'file1.txt' in output and 'subdir' in output and 'file3.txt' in output

    def test_pwd(self):
        cmd = PwdCommand()
        output = cmd.execute()
        assert output == str(Path.cwd())

    def test_mkdir(self):
        new_dir = self.base / 'newdir'
        cmd = MkdirCommand(str(new_dir))
        output = cmd.execute()
        assert new_dir.exists() and new_dir.is_dir()
        assert 'Directory created' in output or 'Directory already exists' in output

    def test_rmdir(self):
        # Test removing empty directory
        empty_dir = self.base / 'emptydir'
        empty_dir.mkdir()
        cmd = RmdirCommand(str(empty_dir))
        output = cmd.execute()
        assert not empty_dir.exists()
        assert 'removed' in output
        # Test removing non-empty directory with force
        nonempty_dir = self.base / 'nonemptydir'
        nonempty_dir.mkdir()
        (nonempty_dir / 'file.txt').write_text('data')
        cmd_force = RmdirCommand(str(nonempty_dir), force=True)
        output_force = cmd_force.execute()
        assert not nonempty_dir.exists()
        assert 'removed' in output_force

    def test_uname(self):
        from agentic_system.commands.basic.uname import UnameCommand
        import platform
        cmd = UnameCommand()
        output = cmd.execute()
        assert platform.uname().system in output 

    def test_touch(self):
        file_path = self.base / 'touched.txt'
        # Test file creation
        cmd = TouchCommand(str(file_path))
        output = cmd.execute()
        assert file_path.exists()
        assert 'File created' in output
        # Test timestamp update
        old_time = file_path.stat().st_mtime
        time.sleep(1)
        cmd2 = TouchCommand(str(file_path))
        output2 = cmd2.execute()
        new_time = file_path.stat().st_mtime
        assert new_time > old_time
        assert 'Timestamp updated' in output2 

    def test_echo(self):
        from agentic_system.commands.basic.echo import EchoCommand
        text = "Hello, test!"
        cmd = EchoCommand(text)
        output = cmd.execute()
        assert output == text 