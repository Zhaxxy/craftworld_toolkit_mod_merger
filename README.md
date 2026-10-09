# craftworld_toolkit_mod_merger
Merge Craftworld Toolkit .mod files into one .mod file

# Usage
if you have python installed on windows, just click the green CODE button, download as zip, extract into its own folder and double click gui.py, it should just work
otherwise cd to the folder and run the command
```
python gui.py
```
or `python3` if on linux

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
