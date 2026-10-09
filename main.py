from tempfile import TemporaryDirectory
import argparse
from pathlib import Path
import zipfile

from map_tools import extract_far4, pack_far4, SaveKey, pack_to_mod
from extract_old_craftworld_toolkit_mod_format import extract_old_craftworld_toolkit_mod_format


def merge_mod_files(merged_mod_output: Path, *mods_to_be_merged: Path) -> None:
    with TemporaryDirectory() as str_tp:
        tp = Path(str_tp)
        parent_mod_dump_dir = tp / 'p_m'
        parent_mod_dump_dir.mkdir()
        for i,mod_file in enumerate(mods_to_be_merged):
            mod_dump_dir = parent_mod_dump_dir / f'm_{i:x}'
            mod_dump_dir.mkdir()
            try:
                with zipfile.ZipFile(mod_file, 'r') as zip_ref:
                    if zip_ref.getinfo('data.farc').file_size > 99_000_000:
                        raise Exception('mod file too big')
                    zip_ref.extract('data.farc',tp)
            except (zipfile.BadZipfile,zipfile.LargeZipFile):
                with open(mod_file, 'rb') as f:
                    f.seek(0,2)
                    if f.tell() > 99_000_000:
                        raise Exception('mod file too big') from None
                    f.seek(0)
                    extract_old_craftworld_toolkit_mod_format(f,mod_dump_dir,flat_dir = True)
                    
            else:
                extract_far4(Path(tp,'data.farc'),mod_dump_dir)
        with zipfile.ZipFile(merged_mod_output,'w') as f:
            pack_to_mod(parent_mod_dump_dir,f)

def main() -> None:
    parser = argparse.ArgumentParser('Merge Craftworld Toolkit .mod files into one .mod file')
    parser.add_argument('merged_mod', help='output of merged mod file, eg merged.mod', type=Path)
    parser.add_argument('-m', '--mods', nargs='+', required=True, help='Craftworld Toolkit .mod files', type=Path)
    args = parser.parse_args()
    
    merge_mod_files(args.merged_mod,*args.mods)


if __name__ == '__main__':
    main()