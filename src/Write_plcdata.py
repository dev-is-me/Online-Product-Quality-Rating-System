import pandas as pd
import subprocess
from openpyxl.utils.dataframe import dataframe_to_rows
from pycomm3 import LogixDriver

from directory import directory_Calc




        # "IP Address": "172.102.1.116", "Device Name": "Oven", "Tag Names": [
        # "HMI_Z1.PV.Temperature", "HMI_Z2.PV.Temperature", "HMI_Z3.PV.Temperature", 
        # "HMI_Z4.PV.Temperature",
        # "Recipe_Running.Zone[1].TopButtom_Heat_Setp", "Recipe_Running.Zone[1].Bottom_Heat_Setp",
        # "Recipe_Running.Zone[2].TopButtom_Heat_Setp", "Recipe_Running.Zone[2].Bottom_Heat_Setp",
        # "Recipe_Running.Zone[3].TopButtom_Heat_Setp", "Recipe_Running.Zone[3].Bottom_Heat_Setp",
        # "Recipe_Running.Zone[4].TopButtom_Heat_Setp", "Recipe_Running.Zone[4].Bottom_Heat_Setp"


# Function to ping an IP address
def ping_ip(ip_address):
    try:
        response = subprocess.run(["ping", "-c", "1", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return response.returncode == 0
    except Exception as e:
        print(f"Error pinging {ip_address}: {e}")
        return False

# Function to write multiple values to a PLC tag
def write_multiple_values(plc_ip, tag_name, values, plc_slot=0):
    try:
        with LogixDriver(plc_ip, plc_slot) as plc:
            # Writing the list of values to the tag
            result = plc.write((tag_name, values))
            if result and result.error is None:
                print(f"Successfully wrote values {values} to tag '{tag_name}' on PLC {plc_ip}")
            else:
                print(f"Failed to write values to tag '{tag_name}'. Error: {result.error}")
    except Exception as e:
        print(f"Error writing to PLC at {plc_ip}: {e}")


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
def main():

    tag_names=["HMI_Z1.PV.Temperature"]
    plc_ip="172.102.1.116"
    tag_value=capture_tag_values(plc_ip, tag_names)
    print(tag_value)
    write_multiple_values(plc_ip, tag_names, [100])
