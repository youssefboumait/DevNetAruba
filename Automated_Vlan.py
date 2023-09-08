import multiprocessing
from functools import partial
import colorama
from netmiko import ConnectHandler
import getpass
import re
import time
import os


def find_type(switch_ip, user, password, vlan_id, vlan_name):
    print(f"Connecting to switch to find its type: {switch_ip}...\n")
    try:
        # Connect to the switch
        arubaswitch = {
            "device_type": "aruba_osswitch",
            "ip": switch_ip.strip(),
            "username": user,
            "password": password,
        }
        net_connect = ConnectHandler(**arubaswitch)

        # Get output of the command "show version"
        value = "show version"
        output = net_connect.send_command(value)

        # Look for "ArubaOS-CX" in the output
        pattern = r"ArubaOS-CX"
        matches = re.findall(pattern, output)

        if matches:
            configure_cx_switch(switch_ip, user, password, vlan_id, vlan_name)
        else:
            configure_switch(switch_ip, user, password, vlan_id, vlan_name)

    except Exception as e:
        print(f"Error occurred while configuring switch with IP {switch_ip}: {str(e)}")


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
        output.splitlines()

        # Get TRK groups from the output
        data = []
        for line in output:
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
            net_connect.save_config()

        # Retrieve and print the tagged ports for the VLAN
        tagged_ports = net_connect.send_command(f"show vlan {vlan_id}")
        print(colorama.Fore.LIGHTYELLOW_EX + f"Tagged ports by VLAN {vlan_id} are:\n")
        print(f"********************************tagged ports by VLAN {vlan_name}***********************************\n")
        print(colorama.Fore.WHITE + tagged_ports)

        net_connect.disconnect()

    except Exception as e:
        print(f"Error occurred while configuring switch with IP {switch_ip}: {str(e)}")


def configure_cx_switch(switch_ip, user, password, vlan_id, vlan_name):
    try:
        print(f"it's a CX switch {switch_ip} executing the operation ...\n")

        # Connect to the switch
        arubaswitch = {
            "device_type": "aruba_osswitch",
            "ip": switch_ip.strip(),
            "username": user,
            "password": password,
        }
        net_connect = ConnectHandler(**arubaswitch)
        # Create the VLAN and give it a name
        vlan_conf = [
            'conf t',
            f'vlan {vlan_id}',
            f'name {vlan_name}',
            'exit'
        ]
        net_connect.send_config_set(vlan_conf)
        net_connect.save_config()

        # Retrieve and print the tagged ports for the VLAN

        tagged_ports = net_connect.send_command(f"show vlan {vlan_id}")
        print(f"********************************tagged ports by VLAN {vlan_name}***********************************\n")
        print(colorama.Fore.WHITE + tagged_ports)

        net_connect.disconnect()

    except Exception as e:
        print(f"Error occurred while configuring switch with IP {switch_ip}: {str(e)}")


if __name__ == "__main__":
    t = time.process_time()
    # do some stuff

    banner = """

  █████╗ ██████╗ ██╗   ██╗██████╗  █████╗     ██████╗ ███████╗██╗   ██╗    ███╗   ██╗███████╗████████╗
██╔══██╗██╔══██╗██║   ██║██╔══██╗██╔══██╗    ██╔══██╗██╔════╝██║   ██║    ████╗  ██║██╔════╝╚══██╔══╝
███████║██████╔╝██║   ██║██████╔╝███████║    ██║  ██║█████╗  ██║   ██║    ██╔██╗ ██║█████╗     ██║   
██╔══██║██╔══██╗██║   ██║██╔══██╗██╔══██║    ██║  ██║██╔══╝  ╚██╗ ██╔╝    ██║╚██╗██║██╔══╝     ██║   
██║  ██║██║  ██║╚██████╔╝██████╔╝██║  ██║    ██████╔╝███████╗ ╚████╔╝     ██║ ╚████║███████╗   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═════╝ ╚══════╝  ╚═══╝      ╚═╝  ╚═══╝╚══════╝   ╚═╝   


' \n

by Youssef BOUMAIT \n

    """
    print(banner, "\n")

    while True:
        user = input("Type your username: ")
        if user.strip():  # Check if the input is not empty after removing leading/trailing whitespace
            break
        else:
            print("Invalid input. Please enter a non-empty username.")

    password = getpass.getpass()

    while True:
        path = input("Enter the path of the TXT file without the \"\" : ")
        if os.path.exists(path):
            break
        else:
            print("Invalid path. Please enter a valid directory path.")

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
        with open(f"{path}") as f:
            lines = f.readlines()
            switchlist = [line.strip() for line in lines if line.strip()]
    except FileNotFoundError:
        print(f"File '{path}' not found.")
        exit()

    # Create a partial function with fixed arguments for configure_switch
    partial_configure_switch = partial(find_type, user=user, password=password, vlan_id=vlan_id,
                                       vlan_name=vlan_name)

    # Use multiprocessing Pool to process switches in parallel
    with multiprocessing.Pool() as pool:
        pool.map(partial_configure_switch, switchlist)

    # counting elapsed time during the execution

    elapsed_time = time.process_time() - t
    print(f"it took {elapsed_time} to finish the operation")
