import os
import sys
from random import randint


# Append null bytes to the end of the file
def add_null_bytes(file_path: str, null_count: int):
    file = open(file_path, "r+b")
    file.seek(0, 2)
    file.write(b"\0" * null_count)
    file.close()


# remove null bytes from the end of the file
# reverts change_hash function
# doesn't work for files that need ending null bytes
def remove_null_bytes(file_path: str):
    file = open(file_path, "r+b")
    file.seek(-1, 2)
    while file.read(1) == b"\0":
        file.seek(-2, 1)
    file.truncate()
    file.close()


def count_null_bytes_at_end(file_path: str):
    file = open(file_path, "rb")
    file.seek(-1, 2)
    count_before = file.tell()
    while file.read(1) == b"\0":
        file.seek(-2, 1)
    count_after = file.tell()
    file.close()
    return count_before - count_after + 1


# loop files in directory and change hash
def verify_add_null_bytes(file_path: str):
    before = count_null_bytes_at_end(file_path)
    add_null_bytes(file_path, randint(1, 8) * 4)
    after = count_null_bytes_at_end(file_path)
    if after > before:
        msg = "OK"
    if after <= before:
        msg = "FAIL"
    if after == 0 and before == 0:
        msg = "FAIL_NO_CHANGE"
    print(msg, before, "-->", after, file_path)


def verify_remove_null_bytes(file_path: str):
    before = count_null_bytes_at_end(file_path)
    remove_null_bytes(file_path)
    after = count_null_bytes_at_end(file_path)
    if after < before:
        msg = "OK"
    if after >= before:
        msg = "FAIL"
    if after == 0 and before == 0:
        msg = "OK_NO_CHANGE"
    print(msg, before, "-->", after, file_path)


def prepare_paths(args):
    file_paths = []
    for arg in args:
        if os.path.isdir(arg):
            # extend full file paths
            file_paths.extend([os.path.join(arg, filename)
                              for filename in os.listdir(arg)])
        else:
            file_paths.append(arg)
    return file_paths


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print(
            "Change hash: python3 change-hash.py -c <file1/directory1> [<file2/directory2> ...]")
        print(
            "Revert back: python3 change-hash.py -r <file1/directory1> [<file2/directory2> ...]")
        exit()

    files = prepare_paths(sys.argv[2:])
    for file in files:
        print(file)

    # check if command line argument is -c or -r
    if sys.argv[1] == "-c":
        print("Changing hashes by adding null characters:")
        for file in files:
            try:
                verify_add_null_bytes(file)
            except Exception as e:  # ignore exception if file is not readable and proceed to next file
                print(e)


    elif sys.argv[1] == "-r":
        print("Reverting changed files by removing all null characters at the end of the files:")
        for file in files:
            try:
                verify_remove_null_bytes(file)
            except Exception as e:  # ignore exception if file is not readable and proceed to next file
                print(e)
