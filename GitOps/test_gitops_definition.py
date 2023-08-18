'''
測試gitops_definitions
'''
import os
import shutil
import stat
import time
import pytest
from gitops_definition import Gitops

class TestGit:
    '''
    定義測試內容
    '''
    def setup_method(self):
        '''
        setup
        '''
        self.test_repo_path = r"C:\Users\user\Downloads\giteapy_testing"
        self.remote_repo_url = "https://gitea.com/zack1284/giteapy_testing.git"
        self.branch = None # if None = main/master  
        if os.path.exists(self.test_repo_path):
            shutil.rmtree(self.test_repo_path, onerror=self.remove_readonly)

    def teardown_method(self):
        '''
        teardown
        '''
        if os.path.exists(self.test_repo_path):
            shutil.rmtree(self.test_repo_path, onerror=self.remove_readonly)

    @staticmethod
    def remove_readonly(func, path, excinfo):
        '''
        為了刪除read-only的 .git files, 新增write權限
        '''
        os.chmod(path, stat.S_IWRITE)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path, onerror=func)
            else:
                os.remove(path)
        except Exception as error_exception:
            print(f"Error while removing directory or file: {error_exception}")

    def count_git_add_files(self, git_operations, *files, untracked=True, modified=True):
        '''
        用於計算git add 的檔案數量
        '''
        all_files = git_operations.add_files(untracked=untracked, modified=modified)
        file_count = sum(1 for file_name in all_files if file_name in files)
        return file_count

    def clone(self):
        '''
        執行 git clone
        '''
        os.makedirs(self.test_repo_path, exist_ok=True)
        git_operations = Gitops(self.remote_repo_url, self.test_repo_path, branch=self.branch, clone_or_not=True)
        return git_operations

    @pytest.mark.parametrize(
        "untracked, modified",
        [
            (False, True),  # Scenario 2: Files Modified Only
            (True, True),   # Scenario 3: Files added Only
            (True, False),  # Files added or deleted
        ],
    )
    def test_add_file(self, untracked, modified):
        '''
        將git add 的檔案區分成新增(untracked), 修改(modified), 刪除(deleted)
        透過untracked, modified去設定需要Push什麼
        delete files 一律不上傳遠端
        '''

        create_file = "pytest.txt"  # newly created
        modify_file = "ok.txt"      # needs to be a file already exists
        delete_file = "test.py"     # needs to be a file already exists

        git_operations = self.clone()
        with open(os.path.join(self.test_repo_path, create_file), "w", encoding="utf-8") as file:
            file.write("This is a sample file created using Python")
        with open(os.path.join(self.test_repo_path, modify_file), "w", encoding="utf-8") as file:
            file.write("Modified File")

        if os.path.exists(os.path.join(self.test_repo_path, delete_file)):
            os.remove(os.path.join(self.test_repo_path, delete_file))

        expected_file_count = 2 if (untracked and modified) else 1
        assert self.count_git_add_files(git_operations, create_file, modify_file, untracked=untracked, modified=modified) == expected_file_count

    def test_commit_upload(self):
        '''
        測試commit message與是否成功上傳
        測試upload新檔案是否成功上傳
        '''
        timestamp = int(time.time())
        create_file = f"file_{timestamp}.txt"
        commit_message = f"new commit at {timestamp}"
        git_operations = self.clone()

        with open(os.path.join(self.test_repo_path, create_file), "w", encoding="utf-8") as file:
            file.write("testing")

        git_operations.add_files(untracked=True, modified=True)
        git_operations.commit_upload(branch=self.branch, commit_messages=commit_message)
        git_operations.close_repository()

        self.teardown_method()
        git_operations = self.clone()
        assert os.path.exists(os.path.join(self.test_repo_path, create_file))
        assert commit_message == git_operations.repo.head.commit.message
        git_operations.close_repository()
