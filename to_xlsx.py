import json
import argparse
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def convert_pickle_to_excel(pickle_file_path, excel_file_path):
    df = pd.read_pickle(pickle_file_path)

    print(f'{json.dumps(df.to_dict(orient="records"), indent=4)}')
    
workbook = Workbook()
sheet = workbook.active

    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            cell = sheet.cell(row=r_idx, column=c_idx, value=value)
            if c_idx == df.columns.get_loc('SSC_Link') + 1 and r_idx > 1:
                cell.hyperlink = df.iloc[r_idx - 2]['SSC_Link']

    workbook.save(excel_file_path)
    print('엑셀 파일 저장 성공\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert pickle file to Excel file.')
    parser.add_argument('pickle_file_path', help='Path to the input pickle file containing the DataFrame.')
    parser.add_argument('excel_file_path', help='Path to the output Excel file.')
    args = parser.parse_args()

    convert_pickle_to_excel(args.pickle_file_path, args.excel_file_path)
