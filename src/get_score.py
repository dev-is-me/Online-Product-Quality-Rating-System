from openpyxl import load_workbook
# from read_write import update_excel
import xlwings as xw

# directory_Calc = r'C:\Users\dell\Desktop\Codes'

def recalculate_excel(file_path):
    try:
        app = xw.App(visible=False)
        wb = app.books.open(file_path)
        wb.app.calculate()
        wb.save()
        wb.close()
        app.quit()
        print("Workbook recalculated and saved successfully.")
    except Exception as e:
        print(f"Error recalculating workbook: {e}")

def get_score(directory_Calc, key):
    excel_path = f"{directory_Calc}/Calc_Worksheet.xlsx"

    try:
        # recalculate_excel(excel_path)
        workbook = load_workbook(excel_path, data_only=True)
        sheet = workbook['Sheet3']

        rows = sheet.iter_rows(min_row=2, values_only=True)

        percentage_contributions = []

        for row in rows:
            defect_type, defect_name, percentage_contribution = row[0], row[1], row[2]

            if defect_type == key:
                if percentage_contribution is None:
                    percentage_contribution = 0
                elif not isinstance(percentage_contribution, (int, float)):
                    percentage_contribution = 0

                percentage_contributions.append(percentage_contribution)

        if not percentage_contributions:
            raise ValueError(f"No data found for defect type: {key}")

        total_percentage = sum(percentage_contributions)
        return 100 - total_percentage

    except Exception as e:
        print(f"Error reading or processing the file: {e}")
        return 0

# update_excel()
# print(get_score(directory_Calc, 'Product'))
# print(get_score(directory_Calc, 'Primary'))
# print(get_score(directory_Calc, 'Secondary'))