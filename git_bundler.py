#!/bin/python
import os, shutil, pickle

GIT_CMD_HEAD   = "git -C "
GIT_CMD_SUB    = " bundle create "
GIT_CMD_END    = ".bundle --all"
MAIN_REPO_PATH = os.getcwd()
ROOT_PATH      = "".join(["/" + folder for folder in MAIN_REPO_PATH.split("/")[1:-1]])

def make_bundles():
    if ".git" in os.listdir(MAIN_REPO_PATH):
        if "bundles" in os.listdir(MAIN_REPO_PATH):
            os.system("rm -rf ./bundles")

        modules = []
        modules_table = {}
        os.system("mkdir -p bundles")

        for root, _, _ in os.walk(MAIN_REPO_PATH):
            if ".git" in os.listdir(root):
                modules.append(root)
                
                repo_rel_path = os.path.relpath(root, ROOT_PATH)
                print("Find repo: " + repo_rel_path)
                
                repo_chain = repo_rel_path.split("/")
                if len(repo_chain) <= 1:
                    modules_table[repo_chain[0]] = set()

                else:
                    for idx, repo in enumerate(repo_chain[:-1]):
                        try:
                            modules_table[repo].add(repo_chain[idx + 1])
                        except:
                            modules_table[repo] = set()
                            modules_table[repo].add(repo_chain[idx + 1])

        for module_path in modules:
            module_name = module_path.split("/")[-1]

            print("\033[96m {}\033[00m" .format("\nBundling Repo: " + module_name))
            os.system(GIT_CMD_HEAD + module_path + GIT_CMD_SUB + module_name + GIT_CMD_END)
            shutil.move(module_path + "/" + module_name + ".bundle", MAIN_REPO_PATH + "/bundles/")

        with open('bundles/table.pickle', 'wb') as file:
            file.write(pickle.dumps(modules_table))
            file.close()
            print("\033[96m {}\033[00m" .format("\nSaving module table"))

        # with open('table.pickle', 'rb') as file:
        #     serials = file.read()
        #     file.close()

        # print(pickle.loads(serials))

    else:
        Exception("Please attach this script to the root of your main repo")

if __name__ == "__main__":
    make_bundles()