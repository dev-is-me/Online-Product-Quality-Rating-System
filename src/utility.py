import socket
import os
from pycomm3 import LogixDriver
import subprocess

# Function to scan the network and check IP statuses
def scan_network(prefix):
    ip_status = []
    for i in range(1, 255):
        ip = f"{prefix}.{i}"
        response = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.PIPE)
        status = 1 if response.returncode == 0 else 0
        ip_status.append((ip, status))
    return ip_status

# Function to list tag names for a given IP address
def list_tags(plc_ip, plc_slot=0):
    tag_names = []
    try:
        with LogixDriver(plc_ip, plc_slot) as plc:
            tag_list = plc.get_tag_list()
            tag_names = [tag['tag_name'] for tag in tag_list]
    except Exception as e:
        print(f"Error connecting to PLC at {plc_ip}: {e}")
    return tag_names

# Function to capture data for input tag names
def capture_tag_values(plc_ip, tag_names, plc_slot=0):
    tag_values = []
    try:
        with LogixDriver(plc_ip, plc_slot) as plc:
            for tag in tag_names:
                value = plc.read(tag)
                tag_values.append((tag, value))
    except Exception as e:
        print(f"Error reading tags from PLC at {plc_ip}: {e}")
    return tag_values

# Main code to use the above functions
def main():
    network_prefix = "172.102.1"
    print("Scanning network...")
    ip_status_list = scan_network(network_prefix)
    
    print("\nIP Address\tStatus")
    for ip, status in ip_status_list:
        print(f"{ip}\t{status}")
    
    for ip, status in ip_status_list:
        if status == 1:
            print(f"\nListing tags for IP: {ip}")
            tags = list_tags(ip)
            print("\nTag Names:")
            for tag in tags:
                print(tag)

            # For demonstration, we'll just capture and print values of a few tags
            selected_tags = tags[:5]  # Select the first 5 tags for capturing values
            print(f"\nCapturing values for selected tags at IP: {ip}")
            tag_values = capture_tag_values(ip, selected_tags)
            
            print("\nTag Name\tValue")
            for tag, value in tag_values:
                print(f"{tag}\t{value}")

print("PDS: \n",list_tags("172.102.1.126"))