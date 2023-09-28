'''
測試GitOps_definitions
'''
import os
import shutil
import stat
from datetime import datetime
import pytest
from gitops import GitOps

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
        self.branch = "main" # if None = main/master  
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

    def count_git_add_files(self, git_operations, untracked, modified, delete):
        '''
        用於計算git add 的檔案數量
        '''
        all_files = git_operations.add_files(untracked=untracked, modified=modified, delete=delete)
        file_count = len(all_files)
        return file_count

    @pytest.mark.parametrize(
        "untracked, modified, delete",
        [   (False, False, False), #0
            (False, True, False), #1
            (False, True, True),  #2
            (True, False, False), #1
            (True, False, True), #2
            (True, True, False), #2
            (True, True, True),  #3
            (False,False,True) #1
        ],
    )
    @pytest.mark.addfiles
    def test_add_file(self, untracked, modified, delete):
        '''
        將git add 的檔案區分成新增(untracked), 修改(modified), 刪除(deleted)
        透過untracked, modified去設定需要Push什麼
        delete files 一律不上傳遠端
        '''

        create_file = "pytest.txt"  # newly created
        modify_file = "ok.txt"      # needs to be any file that's already exists
        delete_file = "test.py"     # needs to be any file that's already exists

        git_operations = GitOps(self.remote_repo_url, self.test_repo_path, branch=self.branch)
        with open(os.path.join(self.test_repo_path, create_file), "w", encoding="utf-8") as file:
            file.write("This is a sample file created using Python")
        with open(os.path.join(self.test_repo_path, modify_file), "w", encoding="utf-8") as file:
            file.write("Modified File")

        if os.path.exists(os.path.join(self.test_repo_path, delete_file)):
            os.remove(os.path.join(self.test_repo_path, delete_file))


        if (untracked and modified and delete):
            expected_file_count = 3
        elif (untracked and modified) and not delete:
            expected_file_count = 2
        elif (untracked and delete) and not modified:
            expected_file_count = 2
        elif (modified and delete) and not untracked:
            expected_file_count = 2
        elif not (untracked and modified) and delete:
            expected_file_count = 1
        elif not (untracked and delete) and modified:
            expected_file_count = 1
        elif not (modified and delete) and untracked:
            expected_file_count = 1
        else:
            expected_file_count = 0

        assert self.count_git_add_files(git_operations, untracked=untracked, modified=modified, delete=delete) == expected_file_count


    @pytest.mark.commit_push
    def test_commit_push(self):
        '''
        測試commit message與是否成功上傳
        測試push新檔案是否成功上傳
        '''
        formatted_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        create_file = f"file_{formatted_time}.txt"
        commit_message = f"new commit at {formatted_time}"
        git_operations = GitOps(self.remote_repo_url, self.test_repo_path, branch=self.branch)

        with open(os.path.join(self.test_repo_path, create_file), "w", encoding="utf-8") as file:
            file.write("testing")

        git_operations.add_files(untracked=True, modified=True)
        git_operations.commit(commit_messages=commit_message)
        git_operations.push(branch=self.branch, origin="origin")
        git_operations.close_repository()

        self.teardown_method()
        git_operations = GitOps(self.remote_repo_url, self.test_repo_path, branch=self.branch)
        assert os.path.exists(os.path.join(self.test_repo_path, create_file))
        assert commit_message == git_operations.repo.head.commit.message
        git_operations.close_repository()

    @pytest.mark.newbranch_checkout
    def test_newbranch_checkout(self):
        '''
        測試切換分支
        '''
        git_operations = GitOps(self.remote_repo_url, self.test_repo_path, branch=self.branch)
        git_operations.create_new_branch('test_branch')
        assert git_operations.repo.active_branch.name == 'test_branch'     
        git_operations.checkout(checkout_branch='main')
        assert git_operations.repo.active_branch.name == 'main' 
        git_operations.close_repository()