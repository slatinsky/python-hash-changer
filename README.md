# Python hash changer
Change file hash using the least destructive way possible.
It works by appending null bytes at the end of the the files.

Other hash changers calculate the hash, change the file, calculate the hash again to verify the change - which is slow for large files, because the entire file needs to be read twice.

This hash changer directly seeks to the end of the file, which is much faster. Verification is just counting the null bytes at the end of the file. Because we actually do not verify the hash, there is very very very very small change, that hash collision may happen.

Written in Python 3.

And as always, don't forget to back up your original files!

## Usage
### Change hash
 - appends from 4 to 32 null bytes to the files
 - does not recursively search subdirectories

```bash
python3 change-hash.py -c <file1/directory1> [<file2/directory2> ...]
```

### Revert back
 - removes all null bytes at the end of the file
 ```bash
python3 change-hash.py -r <file1/directory1> [<file2/directory2> ...]
```

### Check usage
Run without arguments to see the usage.
```bash
python3 change-hash.py
```

## License
MIT License

