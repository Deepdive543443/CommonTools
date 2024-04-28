#!/bin/python
import os, shutil

GIT_CMD_HEAD   = "git -C "
GIT_CMD_SUB    = " bundle create "
GIT_CMD_END    = ".bundle --all"
MAIN_REPO_PATH = os.getcwd()
ROOT_PATH      = "".join(["/" + folder for folder in MAIN_REPO_PATH.split("/")[1:-1]])


if __name__ == "__main__":
    if ".git" in os.listdir(MAIN_REPO_PATH):
        if "bundles" in os.listdir(MAIN_REPO_PATH):
            os.system("rm -rf ./bundles")

        modules = []
        os.system("mkdir -p bundles")

        for root, _, _ in os.walk(MAIN_REPO_PATH):
            if ".git" in os.listdir(root):
                modules.append(root)
                print("Find repo: " + root)

        for module_path in modules:
            module_name        = module_path.split("/")[-1]
            module_rel_path    = os.path.relpath(module_path, ROOT_PATH)
            module_parent_path = os.path.abspath(os.path.join(module_rel_path, ".."))
            bundle_dir_path    = MAIN_REPO_PATH + "/bundles/" + module_rel_path
            bundle_path        = os.path.abspath(bundle_dir_path + "/..")

            print("\nBundling Repo: " + module_name)
            os.system(GIT_CMD_HEAD + module_path + GIT_CMD_SUB + module_name + GIT_CMD_END)
            os.system("mkdir -p " + bundle_dir_path)
            shutil.move(module_path + "/" + module_name + ".bundle", bundle_path)

    else:
        Exception("Please attach this script to the root of your main repo")