import os
import pandas as pd
from openpyxl import load_workbook
from glob import glob
from openpyxl.utils.dataframe import dataframe_to_rows

def get_latest_file(directory, extension="csv"):
    """Returns the latest created file in the specified directory with the given extension."""
    list_of_files = glob(f"{directory}/*.{extension}")
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def update_excel(directory,directory_Calc):
    try:
        # Load data from CSV file
        source_file = get_latest_file(directory)  # CSV file path
        if source_file is None:
            print("No CSV files found in the directory.")
            return

        data = pd.read_csv(source_file)  # Reading the CSV file
        print("CSV data read successfully.")

        # Delete the last two columns
        data = data.iloc[:, :-2]
        
        # Transpose the DataFrame such that the last column becomes the first
        data= data.iloc[:, ::-1]
        
        # Write data to Workbook A
        target_file = f"{directory_Calc}/Calc_Worksheet.xlsx"

        # Load the workbook
        workbook = load_workbook(target_file)

        # If "Sheet1" exists, remove it
        if "Sheet1" in workbook.sheetnames:
            del workbook["Sheet1"]

        # Add the data to a new "Sheet1"
        worksheet = workbook.create_sheet("Sheet1")

        for r_idx, row in enumerate(dataframe_to_rows(data, index=False, header=True), 1):
            for c_idx, value in enumerate(row, 1):
                worksheet.cell(row=r_idx, column=c_idx, value=value)

        # Save the workbook
        workbook.save(target_file)
        print("Data updated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
      

# from directory import directory,directory_Calc
# update_excel(directory,directory_Calc)