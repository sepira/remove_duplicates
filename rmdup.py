from pathlib import Path
import os
import sys
import hashlib


def read_chunk(f_obj, chunk_size=1024):
    """Check in chunks of bytes specially if the file size is large"""
    while True:
        chunk = f_obj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def remove_duplicates(path, hash=hashlib.md5):
    """
    :param path: <pass a directory and read it's subdirectories and files>
    :param hash: <pass a hash algorithm; default is md5>
    :return: None
    """
    unique_hash = set()
    for filename in Path(path).glob('**/*'):
        if filename.is_file():
            hash_obj = hash()
            for chunk in read_chunk(open(filename, 'rb')):
                hash_obj.update(chunk)
            hash_file = hash_obj.hexdigest()
            if hash_file in unique_hash:
                print(str(filename) + " is a duplicate and is being removed..")
                os.remove(filename)
            unique_hash.add(hash_file)


if __name__ == '__main__':
    try:
        remove_duplicates(sys.argv[1])
    except IndexError:
        print("Please pass a directory path as an argument. Run python rmdup.py <directory_path>")