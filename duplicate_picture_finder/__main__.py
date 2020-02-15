import collections
import argparse
import hashlib
import os
import re
import sys

picture_types = [
    ".jpg",
    ".jpeg",
    ".jfif",
    ".jpeg_large",
    ".svg",
    ".png",
]


def main():
    backends = {
        "file_hash": find_by_file_hash,
        "filename": find_by_filename,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".",
                        help="Directory to find duplicate pictures in.")
    parser.add_argument("--remove-duplicates", action="store_true",
                        help="If specified, delete all but the shortest-named "
                             "occurrence of a given picture.")
    parser.add_argument("--find-by", default="filename",
                        choices=backends.keys())
    parser.add_argument("--pictures-only", action="store_true",
                        help="If specified, only consider files with picture "
                             "filename extensions.")
    args = parser.parse_args()

    # os.walk() does not raise an exception if its initial path does not exist.
    if not os.path.exists(args.path):
        print(f"Error: starting path {os.path.realpath(args.path)} not found.")
        exit(1)

    for paths in backends[args.find_by](args.path, args.pictures_only):
        if len(paths) > 1:
            if args.remove_duplicates:
                shortest_path = min(paths, key=lambda s: len(s))
                paths.remove(shortest_path)
                print(f"Removing {len(paths)} duplicates of "
                      f"{os.path.realpath(shortest_path)}")

                for path in paths:
                    os.remove(path)
            else:
                print(f"Found in {len(paths)} places:")
                for path in paths:
                    print(f"  {path}")


def find_by_filename(starting_path, pictures_only):
    # Number in parenthesis just before extension.
    numbered_file = re.compile(r" \(\d+\)\.[^.]+$")
    extension = re.compile(r"\.[^.]+$")

    names = collections.defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(starting_path):
        for filename in filenames:
            if pictures_only:
                # Only consider files with an extension type.
                if not any(map(lambda s: filename.lower().endswith(s),
                               picture_types)):
                    continue

            match = numbered_file.search(filename)
            if match:
                # That before the number if one is given.
                base_filename = filename[:match.start()]
            else:
                # Otherwise that before the extension.
                extension_match = extension.search(filename)
                base_filename = filename[:extension_match.start()]

            file_path = os.path.join(dirpath, filename)
            names[base_filename].append(file_path)

    return names.values()


def find_by_file_hash(starting_path, pictures_only):
    hashes = collections.defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(starting_path):
        for filename in filenames:
            if pictures_only:
                # Only consider files with an extension type.
                if not any(map(lambda s: filename.lower().endswith(s),
                               picture_types)):
                    continue

            file_path = os.path.join(dirpath, filename)
            with open(file_path, "rb") as infile:
                file_hash = hashlib.blake2b(infile.read()).digest()

            hashes[file_hash].append(file_path)

    return hashes.values()
