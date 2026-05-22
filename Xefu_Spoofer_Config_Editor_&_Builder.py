import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import struct
import os

class XeFuConfigEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("XeFu Spoofer - Config Editor & Builder")
        self.root.geometry("640x620")
        self.root.resizable(False, False)
        
        # Main Layout Container
        main_frame = ttk.Frame(root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- TITLE ID SECTION ---
        title_frame = ttk.LabelFrame(main_frame, text=" Game Information ", padding="10")
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(title_frame, text="Target Game Title ID:").pack(side=tk.LEFT, padx=(0, 10))
        self.title_id_var = tk.StringVar(value="4541000D")
        self.title_id_entry = ttk.Entry(title_frame, textvariable=self.title_id_var, width=15, font=("Courier", 10, "bold"))
        self.title_id_entry.pack(side=tk.LEFT)
        
        # --- CONFIGURATION SETS GRID ---
        cfg_frame = ttk.LabelFrame(main_frame, text=" Configuration Sets (cfg01 - cfg14) ", padding="10")
        cfg_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        canvas = tk.Canvas(cfg_frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(cfg_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Default baseline values from research templates to autofill on check
        self.default_templates = {
            "cfg01": ("80000000", "00000001"), # Media / Region base hook
            "cfg02": ("80000000", "00000002"), # Video resolution indicator
            "cfg03": ("80000000", "00000004"), # Memory structure limitation block
            "cfg04": ("80000000", "00000001"), # Cache processing
            "cfg05": ("00000000", "00000000"),
            "cfg06": ("00000000", "00000000"),
            "cfg07": ("00000000", "00000000"),
            "cfg08": ("00000000", "00000000"),
            "cfg09": ("00000000", "00000000"),
            "cfg10": ("00000000", "00000000"),
            "cfg11": ("00000000", "00000000"),
            "cfg12": ("00000000", "00000000"),
            "cfg13": ("00000000", "00000000"),
            "cfg14": ("00000000", "00000000"),
        }
        
        self.cfg_inputs = {}
        self.create_config_rows()
        
        # --- ACTIONS SECTION ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X)
        
        self.status_var = tk.StringVar(value="Ready.")
        status_label = ttk.Label(action_frame, textvariable=self.status_var, font=("Segoe UI", 9, "italic"))
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        clear_btn = ttk.Button(action_frame, text="Reset Form", command=self.reset_form)
        clear_btn.pack(side=tk.RIGHT, padx=2)
        
        open_btn = ttk.Button(action_frame, text="Open Existing .bin", command=self.open_binary)
        open_btn.pack(side=tk.RIGHT, padx=2)
        
        compile_btn = ttk.Button(action_frame, text="Save / Compile .bin", command=self.compile_binary)
        compile_btn.pack(side=tk.RIGHT, padx=2)

    def on_checkbutton_toggle(self, cfg_key):
        """Automatically supplies valid hex baselines when enabled, or clears them when disabled."""
        cfg_set = self.cfg_inputs[cfg_key]
        if cfg_set['enabled'].get():
            # If the fields are just blank or zeroed out, auto-populate them with foundational values
            if cfg_set['address'].get() == "00000000" and cfg_set['value'].get() == "00000000":
                default_addr, default_val = self.default_templates[cfg_key]
                cfg_set['address'].set(default_addr)
                cfg_set['value'].set(default_val)
        else:
            # Revert back to null block safely if user unchecks it
            cfg_set['address'].set("00000000")
            cfg_set['value'].set("00000000")

    def create_config_rows(self):
        """Generates input rows for all 14 config patches."""
        ttk.Label(self.scrollable_frame, text="Enable", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.scrollable_frame, text="Config Set", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(self.scrollable_frame, text="Patch Address (Hex)", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(self.scrollable_frame, text="Patch Value / Arg (Hex)", font=("Segoe UI", 9, "bold")).grid(row=0, column=3, padx=5, pady=5)
        
        hints = {
            1: "Media Check / Region patch block",
            2: "Display / Resolution adjustment",
            3: "Memory Allocation override limits",
            4: "Texture Cache & Framebuffer handling"
        }
        
        for i in range(1, 15):
            cfg_key = f"cfg{i:02d}"
            enabled_var = tk.BooleanVar(value=False)
            addr_var = tk.StringVar(value="00000000")
            val_var = tk.StringVar(value="00000000")
            
            # Map tracking configuration data references
            self.cfg_inputs[cfg_key] = {
                'enabled': enabled_var,
                'address': addr_var,
                'value': val_var
            }
            
            # Checkbox linking to the auto-fill callback system
            chk = ttk.Checkbutton(
                self.scrollable_frame, 
                variable=enabled_var, 
                command=lambda k=cfg_key: self.on_checkbutton_toggle(k)
            )
            chk.grid(row=i, column=0, padx=5, pady=4)
            
            label_text = cfg_key
            if i in hints:
                label_text += f" ({hints[i]})"
            lbl = ttk.Label(self.scrollable_frame, text=label_text, width=30, anchor="w")
            lbl.grid(row=i, column=1, padx=5, pady=4, sticky="w")
            
            ent_addr = ttk.Entry(self.scrollable_frame, textvariable=addr_var, width=12, font=("Courier", 9), justify="center")
            ent_addr.grid(row=i, column=2, padx=5, pady=4)
            
            ent_val = ttk.Entry(self.scrollable_frame, textvariable=val_var, width=12, font=("Courier", 9), justify="center")
            ent_val.grid(row=i, column=3, padx=5, pady=4)

    def reset_form(self):
        """Clears all form data back to default null configurations."""
        self.title_id_var.set("4541000D")
        for i in range(1, 15):
            cfg_set = self.cfg_inputs[f"cfg{i:02d}"]
            cfg_set['enabled'].set(False)
            cfg_set['address'].set("00000000")
            cfg_set['value'].set("00000000")
        self.status_var.set("Form reset completely.")

    def open_binary(self):
        """Opens a compiled custom binary file, parses the data blocks, and displays values."""
        file_path = filedialog.askopenfilename(
            title="Select Custom XeFu Patch File",
            filetypes=[("Binary Files", "*.bin"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "rb") as f:
                binary_data = f.read()

            expected_size = 14 * 8 
            if len(binary_data) != expected_size:
                messagebox.showwarning(
                    "Size Mismatch", 
                    f"Warning: File size is {len(binary_data)} bytes. Standard config files are exactly {expected_size} bytes."
                )

            base_name = os.path.splitext(os.path.basename(file_path))[0]
            if len(base_name) == 8:
                try:
                    int(base_name, 16)
                    self.title_id_var.set(base_name.upper())
                except ValueError:
                    pass

            for i in range(1, 15):
                cfg_key = f"cfg{i:02d}"
                offset = (i - 1) * 8

                if offset + 8 <= len(binary_data):
                    addr, val = struct.unpack_from('>II', binary_data, offset)
                    cfg_set = self.cfg_inputs[cfg_key]
                    
                    cfg_set['address'].set(f"{addr:08X}")
                    cfg_set['value'].set(f"{val:08X}")
                    
                    # If the loaded data has values, keep it checked!
                    if addr != 0 or val != 0:
                        cfg_set['enabled'].set(True)
                    else:
                        cfg_set['enabled'].set(False)
                else:
                    self.cfg_inputs[cfg_key]['enabled'].set(False)

            self.status_var.set(f"Successfully loaded and parsed: {os.path.basename(file_path)}")

        except Exception as ex:
            messagebox.showerror("Parsing Error", f"Could not decompress file structures correctly:\n{str(ex)}")

    def compile_binary(self):
        """Parses UI inputs and outputs a structurally complete, padded binary block."""
        title_id = self.title_id_var.get().strip().upper().replace("0X", "")
        
        if len(title_id) != 8:
            messagebox.showerror("Validation Error", "The Title ID must be exactly 8 characters long.")
            return
            
        output_file = filedialog.asksaveasfilename(
            title="Save Custom XeFu Patch File",
            initialfile=f"{title_id}.bin",
            filetypes=[("Binary Files", "*.bin"), ("All Files", "*.*")]
        )
        if not output_file:
            return
            
        binary_payload = bytearray()
        
        try:
            for i in range(1, 15):
                cfg_key = f"cfg{i:02d}"
                cfg_set = self.cfg_inputs[cfg_key]
                
                # Checkbox state dictates whether we compile input or write empty pads
                if cfg_set['enabled'].get():
                    addr_str = cfg_set['address'].get().strip().replace("0x", "")
                    val_str = cfg_set['value'].get().strip().replace("0x", "")
                    
                    addr = int(addr_str, 16) if addr_str else 0
                    val = int(val_str, 16) if val_str else 0
                else:
                    addr = 0x00000000
                    val = 0x00000000
                    
                binary_payload.extend(struct.pack('>II', addr, val))
            
            with open(output_file, 'wb') as f:
                f.write(binary_payload)
                
            self.status_var.set(f"Successfully compiled patch: {os.path.basename(output_file)}")
            messagebox.showinfo("Success", f"Configuration file successfully written out!")
            
        except ValueError as hex_err:
            messagebox.showerror("Hex Failure", f"Please check row formatting configurations.\nDetails: {str(hex_err)}")
        except Exception as ex:
            messagebox.showerror("Error", f"An unexpected issue occurred while compiling binary:\n{str(ex)}")

if __name__ == "__main__":
    window = tk.Tk()
    app = XeFuConfigEditor(window)
    window.mainloop()