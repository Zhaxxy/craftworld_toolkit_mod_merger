![icon](icon.png)
# craftworld_toolkit_mod_merger
Merge Craftworld Toolkit .mod files into one .mod file

# Usage
if you are on windows, download the exe in the releases tab and double click that<br><br>
otherwise cd to the folder and run the command
```
python3 gui.py
```

# if gui.py no work or you prefer cli
cli (`main.py`) usage
```
usage: Merge Craftworld Toolkit .mod files into one .mod file [-h] -m MODS [MODS ...] merged_mod

positional arguments:
  merged_mod            output of merged mod file, eg merged.mod

options:
  -h, --help            show this help message and exit
  -m, --mods MODS [MODS ...]
                        Craftworld Toolkit .mod files

```
eg command
```
python3 main.py merged_mod_output.mod -m mod1.mod mod2.mod
```
