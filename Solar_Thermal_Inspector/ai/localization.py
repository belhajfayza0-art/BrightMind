#Still needs more precision and more details
def assign_panel_id(index):

    sectors = ["A", "B", "C", "D"]

    sector_size = 100
    row_size = 10

    sector = sectors[(index // sector_size) % len(sectors)]

    row = (index % sector_size) // row_size
    panel = index % row_size

    return f"NOOR_ATLAS_SEC_{sector}_ROW_{row:02}_PANEL_{panel:02}"