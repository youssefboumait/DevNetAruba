from netmiko import ConnectHandler
import getpass
from colorama import Fore

if print(data['output']) == test_unreachable['output']:
    print("Network is unreachable")
else:
    packet_loss = data["statistics"]
    list = packet_loss.split(",")
    print(list[2])



switch_list = ["192.168.131.140","192.168.131.141","192.168.131.142"]
user = input("type the username : ")
password = getpass.getpass()

for x in switch_list:

  arubaswitch = {
   "device_type" : "aruba_osswitch",
   "ip":x,
   "username": user,
   "password": password,

               }
  net_connect = ConnectHandler(**arubaswitch)
  output = net_connect.send_command ("sh ip int br | inc up ")
  uptime = net_connect.send_command ("sh system")
  name = net_connect.send_command("sh hostname")
  print(Fore.BLUE + f"+++++++++++++++++ switch :{name} +++++++++++++++++++++")
  print(Fore.RED + output, "\n")
  print(Fore.LIGHTGREEN_EX + uptime)

















