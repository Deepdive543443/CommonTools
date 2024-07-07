#!/usr/bin/python3

'''
A tiny scrip[t] I used to bundling and extracting large git repositories with submodules
Only apply for Linux env

'''
import os, shutil, argparse

ARGS = argparse.ArgumentParser()
ARGS.add_argument('-b', '--bundle' , default=os.getcwd(), help="Path to the main repo root dir")
ARGS.add_argument('-e', '--extract', default=None,        help="Path to bundles to extract")
ARGS.add_argument('-o', '--output' , default=None,        help="Path to store output bundles")

ARGS           = ARGS.parse_args()
SPLIT          = "~!~"
GIT_CMD_HEAD   = "git -C "
GIT_CMD_BUNDLE = " bundle create "
GIT_CMD_CLONE  = " clone "
GIT_CMD_END    = ".bundle --all"


def gitmodules_parser(root_path: str) -> [list, list]:
    repo_paths     = []
    repo_rel_paths = []

    if ".git" not in os.listdir(root_path):
        return repo_paths, repo_rel_paths

    repo_paths.append(root_path)
    repo_rel_paths.append("")
    print("\033[96m {}\033[00m" .format("Find main repo: " + root_path))    # Adding Main repository

    if ".gitmodules" not in os.listdir(root_path):
        print("\033[96m {}\033[00m" .format("\nNo submodules"))
        return repo_paths, repo_rel_paths

    with open(os.path.join(root_path, ".gitmodules"), "r") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            if "[submodule" in line:
                
                repo_rel_path = line.split('"')[1]
                repo_path     = os.path.join(root_path, repo_rel_path)

                repo_rel_paths.append(repo_rel_path)
                repo_paths.append(repo_path)                                # Adding Sub Repositories
                print("\033[96m {}\033[00m" .format("Find sub repo: " + repo_path))
        f.close()
    return repo_paths, repo_rel_paths


def make_bundles(main_repo_dir: str):
    main_repo_pardir = os.path.abspath(os.path.join(main_repo_dir, os.pardir))
    main_repo_name   = os.path.abspath(main_repo_dir).split("/")[-1]

    module_paths, modules_rel_paths = gitmodules_parser(main_repo_dir)
    if len(module_paths) == 0 or len(modules_rel_paths) == 0:
        Exception("Please attach this script to the root of your main repo")

    output_dir = os.path.abspath(os.path.join(ARGS.output, "bundles")) if ARGS.output else os.path.join(main_repo_dir, "bundles")
    os.system(f"rm    -rf {output_dir}")
    os.system(f"mkdir -p  {output_dir}")

    for module_path, module_rel_path in zip(module_paths, modules_rel_paths):
        module_name     = module_path.split("/")[-1]
        bundle_path     = os.path.join(module_path, module_name + ".bundle")
        module_rel_name = main_repo_name if len(module_rel_path.split("/")) == 1 else SPLIT.join(os.path.join(main_repo_name, module_rel_path).split("/"))

        print("\033[96m {}\033[00m" .format("\nBundling Repo: " + module_name))
        os.system(GIT_CMD_HEAD + module_path + GIT_CMD_BUNDLE + module_name + GIT_CMD_END)
        shutil.move(
            os.path.join(module_path, module_name + ".bundle"),
            os.path.join(output_dir, module_rel_name + ".bundle")
        )   # Copy and bundles to bundle folder and rename with its path
    shutil.copy(os.getcwd() + "/git_bundler.py", main_repo_dir + "/bundles")


def extract_bundles(bundles_path: str):
    bundles_pardir = os.path.abspath(os.path.join(bundles_path, os.pardir))
    bundles        = os.listdir(bundles_path)
    module_names   = [bundle[:-7] for bundle in bundles]

    # Extracting bundles
    for bundle_name in bundles:
        if ".bundle" in bundle_name:
            module_rel_path = os.path.join(bundles_path, "/".join(bundle_name[:-7].split(SPLIT)))
            print("\033[96m {}\033[00m" .format("\nExtracting Repo: " + module_rel_path))
            os.system(GIT_CMD_HEAD + bundles_path + GIT_CMD_CLONE + bundle_name)       # Extract repo from .bundle files

    # Copy bundles to its location
    print(f"\033[96m\n\nCopying ...\033[00m")
    for bundle_name in os.listdir(bundles_path):
        if ".bundle" in bundle_name:

            repo_chain = bundle_name[:-7].split(SPLIT)
            bundle_rel_path = os.path.join(bundles_path, "/".join(repo_chain))

            print(f"\033[96m{os.path.join(bundles_path, bundle_name)[:-7]} "
                  f"-> {bundle_rel_path} \033[00m")

            if os.path.isdir(bundle_rel_path) and len(repo_chain) > 1:          # Check if the dir already exists
                shutil.rmtree(bundle_rel_path)

            shutil.move(
                os.path.join(bundles_path, bundle_name)[:-7],
                os.path.join(bundles_path, repo_chain[-1])                      # Rename
            )
            shutil.move(
                os.path.join(bundles_path, repo_chain[-1]),                     # Move
                bundle_rel_path
            )


if __name__ == "__main__":
    if ARGS.extract:
        extract_bundles(ARGS.extract)

    else:
        make_bundles(ARGS.bundle)
