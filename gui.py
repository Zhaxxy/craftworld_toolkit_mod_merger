"""
https://chatgpt.com/share/6ac962fd-1b80-83eb-a3ad-01b60811e4b6
"""
import argparse
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from main import merge_mod_files


class ModMergerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Craftworld Toolkit Mod Merger")
        self.root.geometry("650x400")
        self.root.minsize(500, 300)

        self.mods: list[Path] = []
        self.output_path = tk.StringVar()

        self._build_ui()

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        # Input files
        ttk.Label(main, text="Input .mod files").pack(anchor=tk.W)

        list_frame = ttk.Frame(main)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(4, 8))

        self.mod_list = tk.Listbox(
            list_frame,
            selectmode=tk.EXTENDED,
            height=10,
        )
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            command=self.mod_list.yview,
        )
        self.mod_list.configure(yscrollcommand=scrollbar.set)

        self.mod_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        input_buttons = ttk.Frame(main)
        input_buttons.pack(fill=tk.X, pady=(0, 12))

        ttk.Button(
            input_buttons,
            text="Add .mod files...",
            command=self.add_mods,
        ).pack(side=tk.LEFT)

        ttk.Button(
            input_buttons,
            text="Remove selected",
            command=self.remove_selected,
        ).pack(side=tk.LEFT, padx=(8, 0))

        ttk.Button(
            input_buttons,
            text="Clear",
            command=self.clear_mods,
        ).pack(side=tk.LEFT, padx=(8, 0))

        # Output file
        ttk.Label(main, text="Output merged file").pack(anchor=tk.W)

        output_frame = ttk.Frame(main)
        output_frame.pack(fill=tk.X, pady=(4, 12))

        ttk.Entry(
            output_frame,
            textvariable=self.output_path,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(
            output_frame,
            text="Browse...",
            command=self.choose_output,
        ).pack(side=tk.LEFT, padx=(8, 0))

        # Merge button
        self.merge_button = ttk.Button(
            main,
            text="Merge Mods",
            command=self.merge,
        )
        self.merge_button.pack(anchor=tk.E)

    def add_mods(self) -> None:
        filenames = filedialog.askopenfilenames(
            parent=self.root,
            title="Select Craftworld Toolkit mod files",
            filetypes=[
                ("Mod files", "*.mod"),
                ("All files", "*.*"),
            ],
        )

        for filename in filenames:
            path = Path(filename)

            if path not in self.mods:
                self.mods.append(path)
                self.mod_list.insert(tk.END, str(path))

        # Suggest an output filename based on the first input.
        if self.mods and not self.output_path.get():
            first = self.mods[0]
            self.output_path.set(str(first.with_name("merged.mod")))

    def remove_selected(self) -> None:
        selected = list(self.mod_list.curselection())

        for index in reversed(selected):
            self.mod_list.delete(index)
            del self.mods[index]

    def clear_mods(self) -> None:
        self.mods.clear()
        self.mod_list.delete(0, tk.END)

    def choose_output(self) -> None:
        filename = filedialog.asksaveasfilename(
            parent=self.root,
            title="Save merged mod file",
            defaultextension=".mod",
            filetypes=[
                ("Mod files", "*.mod"),
                ("All files", "*.*"),
            ],
            initialfile="merged.mod",
        )

        if filename:
            self.output_path.set(filename)

    def merge(self) -> None:
        if not self.mods:
            messagebox.showwarning(
                "No input files",
                "Please add at least one .mod file.",
                parent=self.root,
            )
            return

        output = self.output_path.get().strip()

        if not output:
            messagebox.showwarning(
                "No output file",
                "Please choose an output .mod file.",
                parent=self.root,
            )
            return

        output_path = Path(output)

        if output_path.suffix.lower() != ".mod":
            messagebox.showwarning(
                "Invalid output file",
                "The output filename must have a .mod extension.",
                parent=self.root,
            )
            return

        self.merge_button.configure(state=tk.DISABLED)
        self.root.config(cursor="watch")
        self.root.update_idletasks()

        try:
            merge_mod_files(output_path, *self.mods)

        except Exception as exc:
            messagebox.showerror(
                "Merge failed",
                f"Could not merge the mod files:\n\n{exc}",
                parent=self.root,
            )

        else:
            messagebox.showinfo(
                "Merge complete",
                f"Successfully merged {len(self.mods)} mod file(s).\n\n"
                f"Output:\n{output_path}",
                parent=self.root,
            )

        finally:
            self.root.config(cursor="")
            self.merge_button.configure(state=tk.NORMAL)


def main() -> None:
    root = tk.Tk()
    root.iconbitmap(str(Path(__file__).parent / "icon.ico"))
    ModMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()