import sys
import argparse

from commands.init_cmd import init_cmd
from commands.hash_object_cmd import hash_object_cmd
from commands.cat_file_cmd import cat_file_cmd
from objects.object import get_object_type
from commands.update_index_cmd import update_index_from_cache, update_index_from_file
from objects.tree import write_tree
from objects.commit import write_commit
from utils.config import get_config, add_config
from commands.log_cmd import log_cmd

def main() -> None:
    parser = argparse.ArgumentParser(prog="mygit", description="MyGit Repository Management")

    subparsers = parser.add_subparsers(dest="command")

    # `init` command
    init_parser = subparsers.add_parser('init', help="Initialize a new mygit repository")
    init_parser.add_argument("path", nargs='?', default='.', help="Path to the repository")

    # `config` command
    config_parser = subparsers.add_parser('config', help="Configure the repository")
    config_parser.add_argument("key", help="Key to configure")
    config_parser.add_argument("value", help="Value to configure")
    config_parser.add_argument("-g", "--get", action="store_true", help="Get the value of the key")

    # `hash-object` command
    hash_object_parser = subparsers.add_parser('hash-object', help="Hash an object")
    hash_object_parser.add_argument("file", nargs='?', default=None, help="File to hash")
    hash_object_parser.add_argument("-w", "--write", action="store_true", help="Write the object to the repository")
    hash_object_parser.add_argument("--stdin", action="store_true", help="Read input text from stdin")

    # `cat-file` command
    cat_file_parser = subparsers.add_parser('cat-file', help="Display the contents of an object")
    cat_file_parser.add_argument("-p", action="store_true", help="First figure out type of content, then display it appropriately")
    cat_file_parser.add_argument("-t", action="store_true", help="Display the type of the object")
    cat_file_parser.add_argument("hash", help="Hash of object to display")

    # `update-index` command
    update_index_parser = subparsers.add_parser('update-index', help="Update the index")
    update_index_parser.add_argument("mode", type=int, nargs='?', default=None, help="Mode of the object")
    update_index_parser.add_argument("sha1_hex", nargs='?', default=None, help="SHA-1 hash of the object")
    update_index_parser.add_argument("filename_or_path", help="Filename or path of the object")
    update_index_parser.add_argument("--add", action="store_true", help="Add the object to the index")
    update_index_parser.add_argument("--cacheinfo", action="store_true", help="Add the object to the index from cache")

    # `write-tree` command
    write_tree_parser = subparsers.add_parser('write-tree', help="Write the tree to the repository")

    # `read-tree` command
    read_tree_parser = subparsers.add_parser('read-tree', help="Read the tree from the repository")
    read_tree_parser.add_argument("--prefix", help="Name of the directory to read the tree into")
    read_tree_parser.add_argument("tree_sha1", help="SHA-1 hash of the tree to read")

    # `commit` command
    commit_parser = subparsers.add_parser('commit-tree', help="Commit the repository")
    commit_parser.add_argument("tree_sha1", help="SHA-1 hash of the tree to commit")
    commit_parser.add_argument("-p", "--parent", help="SHA-1 hash of the parent commit")

    # `log` command
    log_parser = subparsers.add_parser('log', help="Show commit logs")
    log_parser.add_argument("commit_sha1", help="SHA-1 hash of the commit to show logs for")

    args = parser.parse_args()
    if args.command == "init":
        init_cmd(args.path)

    elif args.command == "config":
        if args.get:
            print(get_config(args.key))
        else:
            add_config(args.key, args.value)

    elif args.command == "hash-object":
        input = args.file

        if args.stdin and not sys.stdin.isatty():
            input = sys.stdin.read()
        
        if not input:
            raise ValueError("No input provided")

        object_hash = hash_object_cmd(input, args.write)
        print(object_hash)

    elif args.command == "cat-file":
        if args.t:
            object_type = get_object_type(args.hash)
            print(object_type)
        else:
            content = cat_file_cmd(args.hash, args.p)
            print(content)

    elif args.command == "update-index":
        if args.cacheinfo:
            if args.mode is None or args.sha1_hex is None or args.filename_or_path is None:
                raise ValueError("Mode, SHA-1 hash, and filename are required for --cacheinfo")
            
            update_index_from_cache(args.mode, args.sha1_hex, args.filename_or_path)

        elif args.add:
            update_index_from_file(args.filename_or_path)

    elif args.command == "write-tree":
        tree_sha1 = write_tree()
        print(tree_sha1)

    elif args.command == "read-tree":
        if get_object_type(args.tree_sha1) != "tree":
            raise ValueError("Provided SHA-1 is not for a tree object")
        
        update_index_from_cache(40000, args.tree_sha1, args.prefix)

    elif args.command == "commit-tree":
        input = sys.stdin.read()
        if not input:
            raise ValueError("No input provided")
        
        commit_sha1 = write_commit(input, args.tree_sha1, args.parent)
        print(commit_sha1)

    elif args.command == "log":
        print(log_cmd(args.commit_sha1))


if __name__ == "__main__":
    main()
