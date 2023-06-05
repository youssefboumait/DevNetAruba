from netmiko import ConnectHandler
import getpass
from colorama import Fore
import re
import time

t = time.process_time()
user = input("type your user name : ")
password = getpass.getpass()
switchlist = []
data = []

# Validate VLAN ID
vlan_id = input("Enter VLAN ID: ")
try:
    vlan_id = int(vlan_id)
    if 1 <= vlan_id <= 4094:
        print("Valid VLAN ID.")
    else:
        print("Invalid VLAN ID. VLAN ID should be a number between 1 and 4094.")
        exit()
except ValueError:
    print("Invalid input. VLAN ID should be a number.")
    exit()

# Validate VLAN name
vlan_name = input("Enter the VLAN name: ")
if len(vlan_name) < 32:
    print("Valid input.")
else:
    print("Invalid input. The string should have fewer than 32 characters.")
    exit()

# Open the file where the list of switches is and add all the IPs to a list
try:
    with open("D:/SOLARWINDS_IPs.txt") as f:
        switchlist = f.readlines()
except FileNotFoundError:
    print("File 'SOLARWINDS_IPs.txt' not found.")
    exit()

data = []

# Iterate over each IP address in the switch list
for x in switchlist:
    try:
        print(f"connecting to switch {x} ............ \n")
        # Connect to the switch
        arubaswitch = {
            "device_type": "aruba_osswitch",
            "ip": x.strip(),  # Remove leading/trailing whitespace and newline characters
            "username": user,
            "password": password,
        }
        net_connect = ConnectHandler(**arubaswitch)

        # Get output of the command "show trunks"
        value = "show trunks"
        output = net_connect.send_command(value)
        output = output.splitlines()

        # Get TRK groups from the output
        for line in output:
            pattern = r"\d{1}/\d{1}/\d{2}|lag\d{1}"
            ports = re.findall(pattern, output)

        # Remove duplicates from data
        data = list(dict.fromkeys(data))

        # Create the VLAN and give it a name
        vlan_conf = [
            'conf t',
            f' vlan {vlan_id}',
            f'vlan  {vlan_name}',
            'exit'
        ]
        net_connect.send_config_set(vlan_conf)

        # Tag the TRK groups with the newly created VLAN
        for TRK in ports:
            config_TRK = [
                'conf t',
                f'vlan {vlan_id}',
                f'tagged {TRK}',
                'exit'
            ]
            net_connect.send_config_set(config_TRK)

        # Retrieve and print the tagged ports for the VLAN
        tagged_ports = net_connect.send_command(f"show vlan {vlan_id}")
        print(colorama.Fore.LIGHTYELLOW_EX + f"Tagged ports by VLAN {vlan_id} are:\n")
        print(
            f"********************************tagged ports by vlan {vlan_name}******************************************* \n")
        print(colorama.Fore.WHITE + tagged_ports)

        net_connect.disconnect()

    except Exception as e:
        print(f"Error occurred while configuring switch with IP {x}: {str(e)}")

    elapsed_time = time.process_time() - t
    print(f"it took {elapsed_time} to finish the operation")
