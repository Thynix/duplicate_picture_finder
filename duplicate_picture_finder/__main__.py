import collections
import argparse
import hashlib
import os

picture_types = [
    ".jpg",
    ".jpeg",
    ".jfif",
    ".jpeg_large",
    ".svg",
    ".png",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".",
                        help="Directory to find duplicate pictures in.")
    parser.add_argument("--remove-duplicates", action="store_true",
                        help="If specified, delete all but the shortest-named "
                             "occurrence of a given picture.")
    args = parser.parse_args()

    for file_hash, paths in find_duplicate_paths(args.path).items():
        if len(paths) > 1:
            print(f"Found in {len(paths)} places:")
            for path in paths:
                print(f"  {path}")

            if args.remove_duplicates:
                shortest_path = min(paths, key=lambda s: len(s))
                paths.remove(shortest_path)

                for path in paths:
                    os.remove(path)


def find_duplicate_paths(starting_path):
    hashes = collections.defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(starting_path):
        for filename in filenames:
            # Only consider files with an extension type.
            if not any(map(lambda s: filename.lower().endswith(s),
                           picture_types)):
                continue

            file_path = os.path.join(dirpath, filename)
            with open(file_path, "rb") as infile:
                file_hash = hashlib.blake2b(infile.read()).digest()

            hashes[file_hash].append(file_path)

    return hashes
