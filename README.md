# Skyrim-Memory-Editor-Python
A Python-based tool for reading and modifying in-game attributes for Skyrim Special Edition (SkyrimSE). This script utilizes the pymem library to access the game's memory and allows users to modify character attributes directly. It features a graphical user interface (GUI) built with tkinter for ease of use. All values in this script was found with pointer scanning and generating pointer maps.


## Features

Read Current Attribute Values:
- Retrieve real-time values of attributes such as Health, Magicka, Stamina, and skills like Alchemy, Sneak, and more.

Modify Attributes:
- Update attribute values directly in memory with a simple input field.


Graphical User Interface:
- Intuitive GUI with dropdown menus and entry fields.

## Offsets

The script uses the following memory offsets for attribute values:
- Base Pointer: ``SkyrimSE.exe+03169D48``
  Attribute Offsets:
  - Health: ``0x54``
  - Magicka: ``0x58``
  - Stamina: ``0x5C``
And many more (refer to the source code for the complete list).

```
# Retrieve and print current attribute value
def get_attribute_value(attribute_name):
    try:
        pm = pymem.Pymem("SkyrimSE.exe")
        base_address = pymem.process.module_from_name(pm.process_handle, "SkyrimSE.exe").lpBaseOfDll

        base_pointer = base_address + int(skyrim_offsets["Base_Pointer"].split('+')[1], 16)
        pointer = pm.read_longlong(base_pointer)

        for offset in skyrim_offsets["Offsets"]["Common"]:
            pointer = pm.read_longlong(pointer + offset)
        
        attribute_offset = skyrim_offsets["Offsets"][attribute_name]
        attribute_value = pm.read_float(pointer + attribute_offset)
        print(f"{attribute_name}: {attribute_value}")

    except Exception as e:
        print(f"An error occurred: {e}")
```
