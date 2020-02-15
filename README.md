# duplicate-picture-finder
 Find duplicate files in a directory

I made this after I accidentally used a different form of Windows photo import that gave me duplicates of each photo it
processed.

## Usage:

List duplicates based on filename - `IMG_E0778 (1).JPG` is a duplicate of `IMG_E0778.JPG`. 
```shell script
    python duplicate-picture-finder.py [path-to-directory]
``` 

List duplicates based on file content hash:
```shell script
    python duplicate-picture-finder.py --find-by=file_name [path-to-directory]
```

To remove these duplicates instead of printing each path, add `--remove-duplicates`.

See `--help` for more information.
