import pandas as pd
import subprocess
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from pycomm3 import LogixDriver

from directory import directory_Calc



# Data structure for IPs, Device Names, and Tag Names
ip_device_tag_data = [
    {"IP Address": "172.102.1.101", "Device Name": "Axtel", "Tag Names": ["HOPP_02.Actual_Weight"]},
    {"IP Address": "172.102.1.109", "Device Name": "New Mixer", "Tag Names": ["HMI_Manual_Mixing_Time_Mins", "HMI_Dough_Temperature"]},
    {"IP Address": "172.102.1.111", "Device Name": "Depositor", "Tag Names": []},
    {"IP Address": "172.102.1.116", "Device Name": "Oven", "Tag Names": [
        "HMI_Z1.PV.Temperature", "HMI_Z2.PV.Temperature", "HMI_Z3.PV.Temperature", 
        "HMI_Z4.PV.Temperature",
        "Recipe_Running.Zone[1].TopButtom_Heat_Setp", "Recipe_Running.Zone[1].Bottom_Heat_Setp",
        "Recipe_Running.Zone[2].TopButtom_Heat_Setp", "Recipe_Running.Zone[2].Bottom_Heat_Setp",
        "Recipe_Running.Zone[3].TopButtom_Heat_Setp", "Recipe_Running.Zone[3].Bottom_Heat_Setp",
        "Recipe_Running.Zone[4].TopButtom_Heat_Setp", "Recipe_Running.Zone[4].Bottom_Heat_Setp"
    ]},
    {"IP Address": "172.102.1.127", "Device Name": "Packing Machine 1", "Tag Names": [
        "SI_Fin2Temp",
        "SI_Fin3Temp",
        "SI_PreheatTemp",
        "AutoSpeed",
        "SI_CrimperUpTemp",
        "SI_CrimperDownTemp",
        "SI_Rej_MeltedFilm",
        "SI_Rej_RollSplicing",
        "SI_Rej_UncutPack"
    ]},
    {"IP Address": "172.102.1.128", "Device Name": "Packing Machine 2", "Tag Names": [
        "SI_Fin2Temp",
        "SI_Fin3Temp",
        "SI_PreheatTemp",
        "AutoSpeed",
        "SI_CrimperUpTemp",
        "SI_CrimperDownTemp",
        "SI_Rej_MeltedFilm",
        "SI_Rej_RollSplicing",
        "SI_Rej_UncutPack"
    ]},
    {"IP Address": "172.102.1.129", "Device Name": "Packing Machine 3", "Tag Names": [
        "SI_Fin2Temp",
        "SI_Fin3Temp",
        "SI_PreheatTemp",
        "AutoSpeed",
        "SI_CrimperUpTemp",
        "SI_CrimperDownTemp",
        "SI_Rej_MeltedFilm",
        "SI_Rej_RollSplicing",
        "SI_Rej_UncutPack"
    ]},
    {"IP Address": "172.102.1.130", "Device Name": "Packing Machine 4", "Tag Names": [
        "SI_Fin2Temp",
        "SI_Fin3Temp",
        "SI_PreheatTemp",
        "AutoSpeed",
        "SI_CrimperUpTemp",
        "SI_CrimperDownTemp",
        "SI_Rej_MeltedFilm",
        "SI_Rej_RollSplicing",
        "SI_Rej_UncutPack"
    ]},
    {"IP Address": "172.102.1.131", "Device Name": "Packing Machine 5", "Tag Names": [
        "SI_Fin2Temp",
        "SI_Fin3Temp",
        "SI_PreheatTemp",
        "AutoSpeed",
        "SI_CrimperUpTemp",
        "SI_CrimperDownTemp",
        "SI_Rej_MeltedFilm",
        "SI_Rej_RollSplicing",
        "SI_Rej_UncutPack"
    ]},
    {"IP Address": "172.102.1.132", "Device Name": "Packing Machine 6", "Tag Names": [
        "SI_Fin2Temp",
        "SI_Fin3Temp",
        "SI_PreheatTemp",
        "AutoSpeed",
        "SI_CrimperUpTemp",
        "SI_CrimperDownTemp",
        "SI_Rej_MeltedFilm",
        "SI_Rej_RollSplicing",
        "SI_Rej_UncutPack"
    ]},
    {"IP Address": "172.102.1.126", "Device Name": "PDS", "Tag Names": []}
]

# Initialize an empty DataFrame
df = pd.DataFrame(columns=["IP Address", "Device Name", "Tag Name", "Tag Value"])

# Function to ping an IP address
def ping_ip(ip_address):
    try:
        response = subprocess.run(["ping", "-c", "1", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return response.returncode == 0
    except Exception as e:
        print(f"Error pinging {ip_address}: {e}")
        return False

# Function to generate a status table for IPs
def generate_status_table():
    status_data = []
    for entry in ip_device_tag_data:
        ip = entry["IP Address"]
        status = 1 if ping_ip(ip) else 0
        status_data.append({"IP Address": ip, "Status": status})
    return pd.DataFrame(status_data)

# Function to capture tag values from the PLC
def capture_tag_values(plc_ip, tag_names, plc_slot=0):
    tag_values = []
    try:
        with LogixDriver(plc_ip, plc_slot) as plc:
            for tag in tag_names:
                try:
                    result = plc.read(tag)
                    if isinstance(result, list) and result:
                        # Extract the value from the Tag object
                        tag_name = result[0].tag
                        tag_value = result[0].value  # This gives the numeric value
                        tag_values.append((tag_name, tag_value))
                    elif result:
                        # If the result is a single value (not a list)
                        tag_name = result.tag
                        tag_value = result.value  # This gives the numeric value
                        tag_values.append((tag_name, tag_value))
                    else:
                        # If result is None or empty, append default value
                        tag_values.append((tag, "000"))
                except Exception as e:
                    print(f"Error reading tag {tag} from PLC at {plc_ip}: {e}")
                    tag_values.append((tag, "000"))
    except Exception as e:
        print(f"Error connecting to PLC at {plc_ip}: {e}")
        for tag in tag_names:
            tag_values.append((tag, "000"))
    return tag_values


# Function to update the DataFrame with tag values
def update_tags_in_dataframe(status_table):
    global df1, df2  # Separate data frames for different sets of IP addresses
    df1 = pd.DataFrame(columns=["IP Address", "Device Name", "Tag Name", "Tag Value"])
    df2 = pd.DataFrame(columns=["IP Address", "Device Name", "Tag Name", "Tag Value"])
    
    ip_addresses_df2 = ["172.102.1.127", "172.102.1.128", "172.102.1.129", "172.102.1.130", "172.102.1.131", "172.102.1.132"]
    
    for entry in ip_device_tag_data:
        ip = entry["IP Address"]
        device_name = entry["Device Name"]
        tag_names = entry["Tag Names"]
        
        # Check the status of the IP address
        status = status_table.loc[status_table["IP Address"] == ip, "Status"].values[0]
        
        if status == 1:
            # If the IP is reachable, capture and update tag values
            tag_values = capture_tag_values(ip, tag_names)
            for tag, value in tag_values:
                new_row = pd.DataFrame([{"IP Address": ip, "Device Name": device_name, "Tag Name": tag, "Tag Value": value}])
                if ip in ip_addresses_df2:
                    df2 = pd.concat([df2, new_row], ignore_index=True)
                else:
                    df1 = pd.concat([df1, new_row], ignore_index=True)
        else:
            # If the IP is not reachable, append default values
            for tag in tag_names:
                new_row = pd.DataFrame([{"IP Address": ip, "Device Name": device_name, "Tag Name": tag, "Tag Value": "000"}])
                if ip in ip_addresses_df2:
                    df2 = pd.concat([df2, new_row], ignore_index=True)
                else:
                    df1 = pd.concat([df1, new_row], ignore_index=True)

write_df2_shifted = False # Initialize the boolean to track column shift
def write_to_excel(df1, df2, sheet_name, workbook_path, shift_df2_columns):
    try:
        # Load the workbook with openpyxl
        workbook = load_workbook(workbook_path)
        
        # Check if the sheet exists, create if not
        if sheet_name not in workbook.sheetnames:
            worksheet = workbook.create_sheet(sheet_name)
        else:
            worksheet = workbook[sheet_name]
            
        
        # Write df1 to the sheet
        for r_idx, row in enumerate(dataframe_to_rows(df1, index=False, header=True), 1):
            for c_idx, value in enumerate(row, 1):
                worksheet.cell(row=r_idx, column=c_idx, value=value)
        
        # Leave an empty row between df1 and df2
        start_row_df2 = len(df1) + 2
        
        # Determine the starting column for df2
        start_col_df2 = 1 if not shift_df2_columns else 6  # 6 columns offset
        
        # Write df2 to the sheet
        for r_idx, row in enumerate(dataframe_to_rows(df2, index=False, header=True), start_row_df2):
            for c_idx, value in enumerate(row, start_col_df2):
                worksheet.cell(row=r_idx, column=c_idx, value=value)
        
        worksheet["G1"]=shift_df2_columns
        # Save the workbook
        workbook.save(workbook_path)
        print(f"Data successfully written to {sheet_name} in {workbook_path}!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def plcdata(directory_Calc):
    global write_df2_shifted  # Make sure to declare the global variable

    # Generate the status table
    status_table = generate_status_table()
    # print(status_table)

    # Update the tags in the dataframe using the status table
    update_tags_in_dataframe(status_table)
    # print(df1)
    # print(df2)

    # Write the updated dataframe to Excel
    write_to_excel(df1, df2, "Sheet7", f"{directory_Calc}/Calc_Worksheet.xlsx", write_df2_shifted)

    # Toggle the boolean value
    write_df2_shifted = not write_df2_shifted

# # Write the updated dataframe to Excel
# write_to_excel(df, "Sheet7", f"{directory_Calc}/Calc_Worksheet.xlsx")
# {Error reading tags from PLC at 172.102.1.109: failed to open a connection}
# {Error reading tags from PLC at 172.102.1.128: failed to open a connection}
# {Error reading tags from PLC at 172.102.1.132: failed to open a connection}
# {Error reading tags from PLC at 172.102.1.27: failed to open a connection}
# {2   172.102.1.111       0}
# {Packing machine 2 & Packing machine 6 & Mixer failed to open connection }
# { Depositor not connecting}

# plcdata(directory_Calc)
# plcdata(directory_Calc)

    # # Generate the status table
    # status_table = generate_status_table()
    # print(status_table)

    # # Update the tags in the dataframe using the status table
    # update_tags_in_dataframe(status_table)
    # print(df1)
    # print(df2)