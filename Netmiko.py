from netmiko import ConnectHandler
import getpass
from colorama import Fore

switch_list = ["192.168.131.210"]
user = "admin"
password = "admin"

for x in switch_list:
    arubaswitch = {
        "device_type": "aruba_osswitch",
        "ip": x,
        "username": user,
        "password": password,

    }
net_connect = ConnectHandler(**arubaswitch)
output = net_connect.send_command("sh ip int br | inc up ")
uptime = net_connect.send_command("sh system")
name = net_connect.send_command("sh hostname")
trunk_interfaces = net_connect.send_command("sh interface trunk")
print(Fore.BLUE + f"+++++++++++++++++ switch :{name} +++++++++++++++++++++")
print(Fore.RED + output, "\n")
print(Fore.LIGHTGREEN_EX + uptime, "\n")
print(Fore.CYAN + trunk_interfaces)
