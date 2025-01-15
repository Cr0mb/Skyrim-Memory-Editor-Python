import pymem
import pymem.process



## ============================ ##
## ============OFFSETS========== ##
## ============================= ##
print("Skyrim Memory Read")
print("[=================================]")
print("\n\n           Made by Cr0mb\n\n")
print("[=================================]\n")

skyrim_offsets = {
    "Base_Pointer": "SkyrimSE.exe+03169D48",
    "Offsets": {
        "Common": [0xAD8, 0x0, 0x50, 0x170],
        "Stamina": 0x5C,
        "Magicka": 0x58,
        "Health": 0x54,
        "Restoration": 0x48,
        "Illusion": 0x44,
        "Destruction": 0x40,
        "Alteration": 0x38,
        "Speech": 0x34,
        "Alchemy": 0x30,
        "Lockpicking": 0x28,
        "Pickpocket": 0x24,
        "Light_Armor": 0x20,
        "Smithing": 0x18,
        "Block": 0x14,
        "Sneak": 0x2C,
        "One_Handed": 0xC,
        "Archery": 0x10,
        "Enchanting": 0x50,
    }
}

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

if __name__ == "__main__":
    for attribute in skyrim_offsets["Offsets"]:
        if attribute != "Common":
            get_attribute_value(attribute)
