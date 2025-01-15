import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pymem
import pymem.process


print("Skyrim Memory Read")
print("[=================================]")
print("\n\n           Made by Cr0mb\n\n")
print("[=================================]\n")
## ============================ ##
## ============OFFSETS========== ##
## ============================= ##
skyrim_offsets = {
    "Base_Pointer": "SkyrimSE.exe+03169D48",
    "Offsets": {
        "Common": [0xAD8, 0x0, 0x50, 0x170],
        "Stamina": 0x5C,
        "Magicka": 0x58,
        "Health": 0x54,
        "Illusion": 0x48,
        "Destruction": 0x44,
        "Conjuration": 0x40,
        "Speech": 0x38,
        "Alchemy": 0x34,
        "Sneak": 0x30,
        "PickPocket": 0x28,
        "Light_Armor": 0x24,
        "Heavy Armor": 0x20,
        "Block": 0x18,
        "Archery": 0x14,
        "Lockpicking": 0x2C,
        "One_Handed": 0xC,
        "Two-Handed": 0x10,
        "Enchanting": 0x50,
        "Alteration": 0x3C,
        "Restoration": 0x4C,
        "Smithing": 0x1C
    }
}

attribute_groups = {
    "Mage": ["Illusion", "Destruction", "Conjuration", "Alteration", "Restoration", "Speech"],
    "Melee": ["One_Handed", "Two-Handed", "Block", "Archery"],
    "Thief": ["Sneak", "PickPocket", "Lockpicking"],
    "Crafting": ["Alchemy", "Smithing", "Enchanting"],
    "Combat": ["Stamina", "Health", "Magicka"],
    "Armor": ["Light_Armor", "Heavy Armor"]
}

class SkyrimModMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Skyrim Memory Editor")
        self.geometry("400x300")
        self.pm = pymem.Pymem("SkyrimSE.exe")
        self.base_address = pymem.process.module_from_name(self.pm.process_handle, "SkyrimSE.exe").lpBaseOfDll
        self.create_widgets()

    def create_widgets(self):
        self.entries = {}
        self.group_var = tk.StringVar()
        self.group_var.set("Mage")

        self.group_dropdown = ttk.Combobox(self, textvariable=self.group_var, values=list(attribute_groups.keys()))
        self.group_dropdown.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.group_dropdown.bind("<<ComboboxSelected>>", self.update_group)

        self.attributes_frame = tk.Frame(self)
        self.attributes_frame.grid(row=1, column=0, columnspan=3)

        self.exit_button = tk.Button(self, text="Exit", command=self.quit)
        self.exit_button.grid(row=100, column=1, pady=10)

        self.update_group()

    def update_group(self, event=None):
        # Clear the current group widgets
        for widget in self.attributes_frame.winfo_children():
            widget.destroy()

        selected_group = self.group_var.get()
        attributes = attribute_groups[selected_group]
        row = 0

        for attribute in attributes:
            label = tk.Label(self.attributes_frame, text=attribute)
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

            value = tk.Entry(self.attributes_frame)
            value.grid(row=row, column=1, padx=10, pady=5)
            self.entries[attribute] = value

            current_value = self.get_current_value(attribute)
            value.insert(0, str(current_value))

            update_button = tk.Button(self.attributes_frame, text="Update", command=lambda attr=attribute: self.update_value(attr))
            update_button.grid(row=row, column=2, padx=10, pady=5)

            row += 1

    def get_current_value(self, attribute_name):
        try:
            base_pointer = self.base_address + int(skyrim_offsets["Base_Pointer"].split('+')[1], 16)
            pointer = self.pm.read_longlong(base_pointer)

            for offset in skyrim_offsets["Offsets"]["Common"]:
                pointer = self.pm.read_longlong(pointer + offset)

            attribute_offset = skyrim_offsets["Offsets"][attribute_name]
            current_value = self.pm.read_float(pointer + attribute_offset)
            return current_value
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve current value for {attribute_name}: {e}")
            return 0.0

    def update_value(self, attribute_name):
        try:
            base_pointer = self.base_address + int(skyrim_offsets["Base_Pointer"].split('+')[1], 16)
            pointer = self.pm.read_longlong(base_pointer)

            for offset in skyrim_offsets["Offsets"]["Common"]:
                pointer = self.pm.read_longlong(pointer + offset)

            attribute_offset = skyrim_offsets["Offsets"][attribute_name]
            new_value = float(self.entries[attribute_name].get())

            self.pm.write_float(pointer + attribute_offset, new_value)

            messagebox.showinfo("Success", f"Your {attribute_name} has been updated to {new_value}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = SkyrimModMenu()
    app.mainloop()
