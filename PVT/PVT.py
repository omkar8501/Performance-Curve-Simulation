import pandas as pd

# Path of the Excel file and name of sheet containing the PVT Data
pvt_file: str = r'C:\Users\Omkar\OneDrive\Desktop\Reservoir Simulation\Simulation\Performance Curve Simulation\PVT\PVT Table.xlsx'
pvt_sheet_name: str = 'PVT'


pvt_table: pd.DataFrame = pd.read_excel(pvt_file, pvt_sheet_name)
print(pvt_table)
