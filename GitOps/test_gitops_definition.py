import os
import pytest
import shutil
from gitops_definition import gitops
import stat
import time


class TestGit:
    def setup_method(self):
        self.test_repo_path = r"C:\Users\user\Downloads\giteapy_testing"
        self.remote_repo_url = "https://gitea.com/zack1284/giteapy_testing.git"
        if os.path.exists(self.test_repo_path):
            shutil.rmtree(self.test_repo_path, onerror=self.remove_readonly)

    def teardown_method(self):
        if os.path.exists(self.test_repo_path):
            shutil.rmtree(self.test_repo_path, onerror=self.remove_readonly)

    @staticmethod
    def remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path, onerror=func)
            else:
                os.remove(path)
        except Exception as e:
            print(f"Error while removing directory or file: {e}")

    def count_git_add_files(
        self, git_operations, *files, untracked=True, modified=True
    ):
        all_files = git_operations.add_files(untracked=untracked, modified=modified)
        file_count = sum(1 for file_name in all_files if file_name in files)
        return file_count

    def clone(self):
        os.makedirs(self.test_repo_path, exist_ok=True)
        git_operations = gitops(
            self.remote_repo_url, self.test_repo_path, branch=None, clone_or_not=True
        )

        return git_operations

    @pytest.mark.parametrize(
        "untracked, modified",
        [
            (False, True),  # Scenario 2: Files Modified Only
            (True, True),  # Scenario 3: Files added Only
            (True, False),  # Files added or deleted
        ],
    )
    def test_add_file(self, untracked, modified):
        create_file = "pytest.txt"  # newly created
        modify_file = "ok.txt"  # needs to be a file already exists
        delete_file = "test.py"

        git_operations = self.clone()
        with open(os.path.join(self.test_repo_path, create_file), "w") as file:
            file.write("This is a sample file created using Python")
        with open(os.path.join(self.test_repo_path, modify_file), "w") as file:
            file.write("Modified File")

        if os.path.exists(os.path.join(self.test_repo_path, delete_file)):
            os.remove(os.path.join(self.test_repo_path, delete_file))

        expected_file_count = 2 if (untracked and modified) else 1
        assert self.count_git_add_files(git_operations,create_file,modify_file,untracked=untracked,modified=modified)== expected_file_count

    def test_commit_upload(self):
        timestamp = int(time.time())
        create_file = f"file_{timestamp}.txt"
        commit_message = f"new commit at {timestamp}"
        git_operations = self.clone()
        with open(os.path.join(self.test_repo_path, create_file), "w") as file:
            file.write("testing")
        git_operations.add_files(untracked=True, modified=True)
        git_operations.commit_upload(branch=None, commit_messages=commit_message)
        git_operations.close_repository()
        self.teardown_method()
        git_operations = self.clone()
        assert os.path.exists(os.path.join(self.test_repo_path, create_file))
        assert commit_message == git_operations.repo.head.commit.message
        git_operations.close_repository()
