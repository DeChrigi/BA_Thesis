import os
import pandas as pd

directory = 'raw_data/cartel_shareholders'

for filename in os.listdir(directory):
    if filename.endswith('.xls'):
        file_path = os.path.join(directory, filename)
        output_path = os.path.join(directory, os.path.splitext(filename)[0] + '.xlsx')
        # read second sheet of the excel file
        df = pd.read_excel(file_path, sheet_name=1)
        df.to_excel(output_path, index=False)
        os.remove(file_path)


