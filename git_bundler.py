#!/bin/python
import os, shutil, pickle, argparse

GIT_CMD_HEAD   = "git -C "
GIT_CMD_SUB    = " bundle create "
GIT_CMD_END    = ".bundle --all"
MAIN_REPO_PATH = os.getcwd()
ROOT_PATH      = "".join(["/" + folder for folder in MAIN_REPO_PATH.split("/")[1:-1]])
SPLIT          = "~!~"

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-e', '--extract', default=None, help="Path to table and bundles")
ARGS = PARSER.parse_args()

def make_bundles():
    if ".git" in os.listdir(MAIN_REPO_PATH):
        if "bundles" in os.listdir(MAIN_REPO_PATH):
            os.system("rm -rf ./bundles")

        modules       = []
        modules_rel   = []
        modules_table = {}
        os.system("mkdir -p bundles")

        for root, _, _ in os.walk(MAIN_REPO_PATH):
            if ".git" in os.listdir(root):
                repo_rel_path = os.path.relpath(root, ROOT_PATH)
                modules.append(root)
                modules_rel.append(repo_rel_path)
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

        for module_path, module_rel_path in zip(modules, modules_rel):
            module_name     = module_path.split("/")[-1]
            module_rel_path = SPLIT.join(module_rel_path.split("/"))

            print("\033[96m {}\033[00m" .format("\nBundling Repo: " + module_name))
            os.system(GIT_CMD_HEAD + module_path + GIT_CMD_SUB + module_name + GIT_CMD_END)
            shutil.move(module_path + "/" + module_name + ".bundle", MAIN_REPO_PATH + "/bundles/" + module_rel_path + ".bundle")

    else:
        Exception("Please attach this script to the root of your main repo")

def extract_bundles(bundles_path):
    for bundle_name in os.listdir(bundles_path):
        if ".bundle" in bundle_name:
            bundle_rel_path = os.path.join(bundles_path, "/".join(bundle_name[:-7].split(SPLIT)))
            print("\033[96m {}\033[00m" .format("\nExtracting Repo: " + bundle_rel_path))
            os.system("git -C " + bundles_path + " clone " + bundle_name)

    print(f"\033[96m\n\nCopying ...\033[00m")
    for bundle_name in os.listdir(bundles_path):
        if ".bundle" in bundle_name:
            repo_chain = bundle_name[:-7].split(SPLIT)
            bundle_rel_path = os.path.join(bundles_path, "/".join(repo_chain))
            print(f"\033[96m{os.path.join(bundles_path, bundle_name)[:-7]} "
                  f"-> {bundle_rel_path} \033[00m")

            shutil.move(os.path.join(bundles_path, bundle_name)[:-7], os.path.join(bundles_path, repo_chain[-1]))
            shutil.move(os.path.join(bundles_path, repo_chain[-1])+"/", bundle_rel_path)     

if __name__ == "__main__":
    if ARGS.extract:
        extract_bundles(ARGS.extract)
        print("Args: " + ARGS.extract)

    else:
        make_bundles()