'''
使用gitpython執行git各項操作
'''
import os
import git 

class GitOps():
    '''
    定義git的操作
    '''
    def __init__(self,remote_repo_url,local_repo_path,branch, main="main") -> None:
        self.remote_repo_url = remote_repo_url
        self.local_repo_path = local_repo_path
        self.untracked_files = []
        self.modified_files = []
        self.main = main
        self.repo = self.set_up(branch)

    def set_up(self, branch):
        '''
        若local端有git repo則執行; 若無則從遠端clone
       '''
        if not os.path.exists(self.local_repo_path):
            os.makedirs(self.local_repo_path, exist_ok=True)
            repo = git.Repo.clone_from(self.remote_repo_url,self.local_repo_path,branch=branch) 
            print("Clone from remote")               
        else:
            repo = git.Repo(self.local_repo_path)
            print("Local repo initialized.")
        return repo

    def create_new_branch(self, branch, main):
        '''
        新增git分支
        '''
        origin = self.repo.remote("origin")
        assert origin.exists()
        if branch not in self.repo.branches:
            new_branch = self.repo.create_head(f"{branch}", origin.refs[main]) 
            new_branch.checkout()
        else:
            self.repo.git.checkout(branch)
            print(f"branch {branch} already exists.")

    def add_files(self,untracked = False , modified = False, all=False):
        '''
        執行git add 語法，並且將新增檔案分為新增(untracked), 修改(modified), 刪除(deleted)
        '''
        if untracked:
            self.untracked_files = self.repo.git.ls_files(others=True).split('\n')
            print(f"新增的檔案:{self.untracked_files}")
        if modified:
            self.modified_files = self.repo.git.diff("--name-only","--diff-filter=dr").split('\n')
            print(f"修改的檔案:{self.modified_files}")
        if all:
            self.repo.git.add(all=True) 
        all_files = (self.untracked_files + self.modified_files)
        self.repo.git.add([file_path for file_path in all_files if file_path])      
        return all_files 

    def commit_upload(self, branch,commit_messages):
        '''
        執行commit & upload 
        '''
        origin = self.repo.remote("origin")
        assert origin.exists()
        self.repo.index.commit(f"{commit_messages}")
        self.repo.git.push(origin, branch)

    def close_repository(self):
        '''
        關閉repo
        '''
        if self.repo:
            self.repo.close()  # Close the repository