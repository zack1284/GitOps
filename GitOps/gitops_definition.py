'''
使用gitpython執行git各項操作
'''
import git 

class Gitops():
    '''
    定義git的操作
    '''
    def __init__(self,remote_repo_url,local_repo_path,branch,clone_or_not, main="main") -> None:
        self.remote_repo_url = remote_repo_url
        self.local_repo_path = local_repo_path
        self.untracked_files = []
        self.modified_files = []
        self.main = main
        self.repo = self.set_up(clone_or_not,branch)
 
    def set_up(self, clone_or_not, branch):
        '''
        若local端有git repo則執行; 若無則從遠端clone
        '''
        if clone_or_not and branch is not None:
            repo = git.Repo.clone_from(self.remote_repo_url,self.local_repo_path,branch=branch)
            print(f"Clone remote branch {branch}.")
        elif clone_or_not and branch is None:
            repo = git.Repo.clone_from(self.remote_repo_url,self.local_repo_path)
            print("Clone remote main.")
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

    def add_files(self,untracked,modified, all=False):
        '''
        執行git add 語法，並且將新增檔案分為新增(untracked), 修改(modified), 刪除(deleted)
        以達到客製化的需求
        '''
        if untracked:
            self.untracked_files = self.repo.git.ls_files(others=True).split('\n')
        if modified:
            self.modified_files = self.repo.git.diff("--name-only","--diff-filter=dr").split('\n')
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




