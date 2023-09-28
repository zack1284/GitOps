'''
使用gitpython執行git各項操作
'''
import os
import logging
import git
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    handlers = [logging.StreamHandler()])
gitlogger = logging.getLogger(name='git')

class GitOps():
    '''
    定義git的操作
    '''
    def __init__(self,remote_repo_url,local_repo_path,branch) -> None:
        self.remote_repo_url = remote_repo_url
        self.local_repo_path = local_repo_path
        self.repo = self.set_up(branch)
        

    def set_up(self, branch):
        '''
        若local端有git repo則執行; 若無則從遠端clone
    
       '''
        if not os.path.exists(self.local_repo_path):
            os.makedirs(self.local_repo_path, exist_ok=True)
            gitlogger.info("Clone from remote") 
            repo = git.Repo.clone_from(self.remote_repo_url,self.local_repo_path,branch=branch)  
            assert repo.__class__ is git.Repo, "Not a Repo"             
        else:
            try:
                repo = git.Repo(self.local_repo_path)
                assert repo.__class__ is git.Repo, "Not a Repo"
                repo_name = repo.remotes.origin.url.split('/')[-1].split('.git')[0]
                

                print("Current Git repository name:", repo_name) 
            except Exception:
                #repo = git.Repo.clone_from(self.remote_repo_url,self.local_repo_path,branch=branch)
                #repo = git.Repo.init(self.local_repo_path)
                #_ = repo.create_remote("origin", self.remote_repo_url)
                gitlogger.warning("This is not a git repository")

        return repo

    def create_new_branch(self, new_branch):
        '''
        新增git分支
        '''
        if new_branch not in self.repo.branches:
            new_branch = self.repo.create_head(f"{new_branch}") 
            new_branch.checkout()
            gitlogger.info("Create and checkout to new branch %s", new_branch)
        else:
            self.repo.git.checkout(new_branch)
            gitlogger.info("%s already exists. Checkout to new branch", new_branch)


    def checkout(self, checkout_branch):
        '''
        切換分支
        '''
        if checkout_branch in self.repo.branches:
            if not self.repo.is_dirty():
                self.repo.git.checkout(checkout_branch)
                gitlogger.info("Currently on %s", self.repo.active_branch.name)
            else:
                gitlogger.warning("you have uncommited changes")
        else:
            gitlogger.info("checkout branch not exists, please create a new one")


    def add_files(self,untracked = False , modified = False, delete=False):
        '''
        執行git add 語法，並且將新增檔案分為新增(untracked), 修改(modified), 刪除(deleted)
        '''
        changed_files = []

        if untracked:
            untracked_files = self.repo.git.ls_files(others=True).splitlines()
            changed_files.extend(untracked_files)
            gitlogger.debug("新增的檔案:%s",untracked_files)
        if modified:
            modified_files = self.repo.git.diff("--name-only","--diff-filter=dr").splitlines()
            changed_files.extend(modified_files)
            gitlogger.debug("修改的檔案:%s",modified_files)
        if delete:
           deleted_files = self.repo.git.diff("--name-only", "--diff-filter=D").splitlines()
           changed_files.extend(deleted_files)
           gitlogger.debug("刪除的檔案:%s",deleted_files)

        self.repo.git.add(changed_files)      
        return changed_files 
    
    def push(self, branch, origin):
        '''
        執行upload 
        '''
        origin = self.repo.remote(origin)
        if origin.exists():
            try :
                self.repo.git.push(origin,"a")
                pushinfo= origin.push()[0]
                gitlogger.info(pushinfo.summary)
            except Exception as e:
                gitlogger.error(e)

    def commit(self,commit_messages):
        '''
        執行commit
        '''
        self.repo.index.commit(f"{commit_messages}")


    def close_repository(self):
        '''
        關閉repo連線
        '''
        if self.repo:
            self.repo.close()  # Close the repository