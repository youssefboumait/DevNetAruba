import multiprocessing
from functools import partial
import colorama
from netmiko import ConnectHandler
import getpass
from colorama import Fore
import re
import time

def configure_switch(switch_ip, user, password, vlan_id, vlan_name):
 try:
print(f"Connecting to switch {switch_ip}...\n")
    # Connect to the switch
    arubaswitch = {
        "device_type": "aruba_osswitch",
        "ip": switch_ip.strip(),
        "username": user,
        "password": password,
    }
    net_connect = ConnectHandler(**arubaswitch)

    # Get output of the command "show trunks"
    value = "show trunks"
    output = net_connect.send_command(value)
    with open("D:/output.txt", "a") as f:
        print(output, file=f)

    try:
        with open("D:/output.txt") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File 'D:/output.txt' not found.")



    # Get TRK groups from the output
    for line in lines:
        match = re.search(r'(\S+)\s+LACP', line)
        if match:
            data.append(match.group(1))

    # Remove duplicates from data
    data = list(dict.fromkeys(data))

    # Create the VLAN and give it a name
    vlan_conf = [
        'conf t',
        f'vlan {vlan_id}',
        f'name {vlan_name}',
        'exit'
    ]
    net_connect.send_config_set(vlan_conf)

    # Tag the TRK groups with the newly created VLAN
    for TRK in data:
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
    print(f"********************************tagged ports by VLAN {vlan_name}***********************************\n")
    print(colorama.Fore.WHITE + tagged_ports)
    net_connect.disconnect()

  except Exception as e:
    print(f"Error occurred while configuring switch with IP {switch_ip}: {str(e)}")



if name == "main":
t = time.process_time()
# do some stuff
user = input("Type your username: ")
password = getpass.getpass()

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
switchlist = []
try:
    with open("D:/SOLARWINDS_IPs.txt") as f:
        switchlist = f.readlines()
except FileNotFoundError:
    print("File 'SOLARWINDS_IPs.txt' not found.")
    exit()

# Create a partial function with fixed arguments for configure_switch
partial_configure_switch = partial(configure_switch, user=user, password=password, vlan_id=vlan_id, vlan_name=vlan_name)

# Use multiprocessing Pool to process switches in parallel
with multiprocessing.Pool() as pool:
    pool.map(partial_configure_switch, switchlist)

elapsed_time = time.process_time() - t
print(f"It took {elapsed_time} to finish the operation")
