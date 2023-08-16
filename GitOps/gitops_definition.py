import git 

class gitops():

    def __init__(self,remote_repo_url,local_repo_path) -> None:
        self.remote_repo_url = remote_repo_url
        self.local_repo_path = local_repo_path
        self.untracked_files = []
        self.modified_files = []
    
    def initialization(self, clone_bool, branch):
        if clone_bool:
            repo = git.Repo.clone_from(self.remote_repo_url,self.local_repo_path, branch)
            print("Clone remote repo.") 
        else:
            repo = git.Repo(self.local_repo_path)
            print("Local repo initialized.")  

        return repo
    
    def create_new_branch(self,repo, branch, main):
        origin = repo.remote("origin")
        assert origin.exists()
        if branch not in repo.branches:
            new_branch = repo.create_head(f"{branch}", origin.refs[main])  # replace prod with master/ main/ whatever you named your main branch
            new_branch.checkout()
        else:
            print("branch {} already exists".format(branch) )

    def add_files(self,**kwargs):
        repo = kwargs["repo"]
        untracked = kwargs["untracked"]
        modified = kwargs["modified"]
        deleted = kwargs["deleted"]

        if untracked:
            self.untracked_files = repo.git.ls_files(others=True).split('\n')
        if modified and not deleted:
            self.modified_files = repo.git.diff("--name-only","--diff-filter=dr").split('\n')
        else:
            repo.git.add(all=True) 
        
        return self.untracked_files + self.modified_files
    

    def commit_upload(self, repo, branch, all_files):

        for file_path in all_files:
            if file_path:
                repo.git.add(file_path)

        origin = repo.remote("origin")
        repo.index.commit("Add untracked files")
        repo.git.push(origin, branch, force=True)






