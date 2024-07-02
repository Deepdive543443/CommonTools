#!/bin/python3

'''
A tiny scrip[t] I used to bundling and extracting large git repositories with submodules

'''

import os, shutil, pickle, argparse

GIT_CMD_HEAD   = "git -C "
GIT_CMD_SUB    = " bundle create "
GIT_CMD_END    = ".bundle --all"
SPLIT          = "~!~"

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-b', '--bundle', default=None, help="Path to the main repo root dir")
PARSER.add_argument('-e', '--extract', default=None, help="Path to table and bundles")
ARGS = PARSER.parse_args()

def make_bundles(main_repo_dir):
    root_path = "".join(["/" + folder for folder in main_repo_dir.split("/")[1:-1]])
    if ".git" in os.listdir(main_repo_dir):
        if "bundles" in os.listdir(main_repo_dir):
            os.system(f"rm -rf {main_repo_dir}/bundles")
        os.system(f"mkdir -p {main_repo_dir}/bundles")


        modules     = []
        modules_rel = []

        for root, _, _ in os.walk(main_repo_dir):
            if ".git" in os.listdir(root):
                repo_rel_path = os.path.relpath(root, root_path)
                modules.append(root)
                modules_rel.append(repo_rel_path)
                print("Find repo: " + repo_rel_path)

        for module_path, module_rel_path in zip(modules, modules_rel):
            module_name     = module_path.split("/")[-1]
            module_rel_path = SPLIT.join(module_rel_path.split("/"))

            print("\033[96m {}\033[00m" .format("\nBundling Repo: " + module_name))
            os.system(GIT_CMD_HEAD + module_path + GIT_CMD_SUB + module_name + GIT_CMD_END)
            shutil.move(module_path + "/" + module_name + ".bundle", main_repo_dir + "/bundles/" + module_rel_path + ".bundle")

        shutil.copy(os.getcwd() + "/git_bundler.py", main_repo_dir + "/bundles/")

    else:
        Exception("Please attach this script to the root of your main repo")

def extract_bundles(bundles_path):
    # Extracting bundles
    for bundle_name in os.listdir(bundles_path):
        if ".bundle" in bundle_name:
            bundle_rel_path = os.path.join(bundles_path, "/".join(bundle_name[:-7].split(SPLIT)))
            print("\033[96m {}\033[00m" .format("\nExtracting Repo: " + bundle_rel_path))
            os.system("git -C " + bundles_path + " clone " + bundle_name)

    # Copy bundles to its location
    print(f"\033[96m\n\nCopying ...\033[00m")
    for bundle_name in os.listdir(bundles_path):
        if ".bundle" in bundle_name:

            repo_chain = bundle_name[:-7].split(SPLIT)
            bundle_rel_path = os.path.join(bundles_path, "/".join(repo_chain))

            print(f"\033[96m{os.path.join(bundles_path, bundle_name)[:-7]} "
                  f"-> {bundle_rel_path} \033[00m")

            if os.path.isdir(bundle_rel_path) and len(repo_chain) > 1:
                shutil.rmtree(bundle_rel_path)

            shutil.move(os.path.join(bundles_path, bundle_name)[:-7], os.path.join(bundles_path, repo_chain[-1]))
            shutil.move(os.path.join(bundles_path, repo_chain[-1]), bundle_rel_path)

if __name__ == "__main__":
    if ARGS.bundle:
        make_bundles(ARGS.bundle)
    
    elif ARGS.extract:
        extract_bundles(ARGS.extract)

    else:
        make_bundles(os.getcwd())