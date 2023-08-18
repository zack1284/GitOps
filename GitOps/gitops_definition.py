import git 

class gitops():

    def __init__(self,remote_repo_url,local_repo_path,branch,clone_or_not, main="main") -> None:
        self.remote_repo_url = remote_repo_url
        self.local_repo_path = local_repo_path
        self.untracked_files = []
        self.modified_files = []
        self.main = main
        self.repo = self.set_up(clone_or_not,branch)

 
    def set_up(self, clone_or_not, branch):
        if clone_or_not and branch is not None:
            repo = git.Repo.clone_from(self.remote_repo_url,self.local_repo_path,branch)
            print("Clone remote branch {}.".format(branch))
        elif clone_or_not and branch is None:
            repo = git.Repo.clone_from(self.remote_repo_url,self.local_repo_path)
            print("Clone remote main.")
        else:
            repo = git.Repo(self.local_repo_path)
            print("Local repo initialized.")  
        return repo

    def create_new_branch(self, branch, main):
        origin = self.repo.remote("origin")
        assert origin.exists()
        if branch not in self.repo.branches:
            new_branch = self.repo.create_head(f"{branch}", origin.refs[main]) 
            new_branch.checkout()
        else:
            self.repo.git.checkout(branch)
            print("branch {} already exists. Switch to {}".format(branch,branch) )

    def add_files(self,untracked,modified, all=False):

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
        origin = self.repo.remote("origin")
        assert origin.exists()
        self.repo.index.commit(f"{commit_messages}")
        self.repo.git.push(origin, branch)
        
        return True

    def close_repository(self):
        if self.repo:
            self.repo.close()  # Close the repository




