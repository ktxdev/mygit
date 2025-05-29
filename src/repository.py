import sys
import argparse

from src.commands.init_cmd import init_cmd
from src.commands.hash_object_cmd import hash_object_cmd
from src.commands.cat_file_cmd import cat_file_cmd, get_object_type_and_content

def main() -> None:
    parser = argparse.ArgumentParser(prog="mygit", description="MyGit Repository Management")

    subparsers = parser.add_subparsers(dest="command")

    # `init` command
    init_parser = subparsers.add_parser('init', help="Initialize a new mygit repository")
    init_parser.add_argument("path", nargs='?', default='.', help="Path to the repository")

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

    args = parser.parse_args()
    if args.command == "init":
        init_cmd(args.path)

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
            object_type, _ = get_object_type_and_content(args.hash)
            print(object_type)
        else:
            content = cat_file_cmd(args.hash, args.p)
            print(content)


if __name__ == "__main__":
    main()
