# Network Automation Project Documentation

## Introduction
This documentation provides an overview and usage instructions for the Network Automation project. The project focuses on automating the creation of VLANs and tagging of trunk interfaces in Aruba switches. By leveraging the power of automation, it aims to streamline network configuration and reduce manual efforts.

## Requirements
To run the Network Automation project, ensure that the following requirements are met:

- Python 3.x installed on the system.
- The required Python packages: `multiprocessing`, `functools`, `colorama`, `netmiko`.
  - You can install the dependencies using the following command: `pip install -r requirements.txt`
- Access to Aruba switches with appropriate credentials.

## Usage
1. Clone the project repository from GitHub using the following command:
   ```
   git clone [repository_link]
   ```

2. Install the project dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

3. Import the necessary modules and libraries into your Python script:
   ```python
   import multiprocessing
   from functools import partial
   import colorama
   from netmiko import ConnectHandler
   import getpass
   import re
   import time
   import os
   ```

4. Define the `configure_switch` function in your script. This function handles the automation process for each switch. It takes the following parameters:
   - `switch_ip`: IP address of the Aruba switch.
   - `user`: Username for accessing the switch.
   - `password`: Password for accessing the switch.
   - `vlan_id`: VLAN ID to be created and tagged.
   - `vlan_name`: Name for the VLAN.

   ```python
   def configure_switch(switch_ip, user, password, vlan_id, vlan_name):
       # Implementation of switch configuration automation
   ```

5. Customize the implementation of the `configure_switch` function according to your network requirements. The function establishes a connection to the switch, retrieves relevant information, creates the VLAN, tags trunk interfaces, and retrieves tagged ports information.

6. At the end of your script, within the `if __name__ == "__main__":` block, set up the necessary inputs and execute the automation process.
   ```python
   if __name__ == "__main__":
       # Setup and execute automation process
   ```

7. Run the script using the Python interpreter, and follow the prompts to provide the required inputs during execution.

## Example Usage
To illustrate the usage of the Network Automation project, here's an example of a script:

```python
import multiprocessing
from functools import partial
import colorama
from netmiko import ConnectHandler
import getpass
import re
import time
import os

# Function definitions and script implementation...

if __name__ == "__main__":
    # Prompt for user inputs
    user = input("Type your username: ")
    password = getpass.getpass()
    path = input("Enter the path of the TXT file without the '': ")
    vlan_id = input("Enter VLAN ID: ")
    vlan_name = input("Enter the VLAN name: ")

    # Switch list retrieval from file...

    # Create a partial function with fixed arguments for configure_switch
    partial_configure_switch = partial(configure_switch, user=user, password=password, vlan_id=vlan_id,
                                       vlan_name=vlan_name)

    # Use multiprocessing Pool to process switches in parallel
    with multiprocessing.Pool() as pool:
        pool.map(partial_configure_switch, switchlist)

    # Additional processing and output...

    elapsed_time = time.process_time() - t
    print(f"it took {elapsed_time} to finish the operation")
```

Ensure that the script file and the

 TXT file containing the list of switches are in the same directory.

## Conclusion
The Network Automation project simplifies the configuration of VLANs and trunk interfaces in Aruba switches. By automating these processes, it reduces manual effort, improves efficiency, and helps maintain a consistent network setup. Feel free to explore and customize the project according to your specific network requirements.
