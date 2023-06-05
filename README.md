# DevNetAruba


   ```markdown
   This script automates the VLAN configuration on Aruba switches. It connects to a list of switches, creates a new VLAN with a specified VLAN ID and name, and configures the tagged ports for the VLAN.

   **Prerequisites:**
   -any aruba switch beside CX ( i will add them soon )
   - Python 3.x
   - Required Python libraries: `colorama`, `netmiko`
   - Input file: `anything.txt` (containing a list of IP addresses of the switches)

   Please make sure to have the necessary dependencies installed and provide the switch IP addresses in the input file before running the script.
   ```

   ```markdown
   **Script Steps:**
   - Prompt the user to enter their username and password.
   - Validate the VLAN ID and name entered by the user.
   - Read the list of switch IP addresses from the input file.
   - Connect to each switch, retrieve the output of the "show trunks" command, and extract the TRK groups.
   - Create the specified VLAN on each switch and give it a name.
   - Tag the TRK groups with the newly created VLAN.
   - Retrieve and print the tagged ports for the VLAN on each switch.
   ```



   ```markdown
   ## Running the Script

   1. Ensure that the required Python libraries (`colorama`, `netmiko`) are installed. You can install them using `pip`:

      ```shell
      pip install colorama netmiko
      ```

   2. Prepare the input file with the list of switch IP addresses. Each IP address should be on a separate line.

   3. Run the script using Python:

      ```shell
      python script.py
      ```

   4. Follow the prompts to provide your username, password,path, VLAN ID, and VLAN name.

   Please note that the script may take some time to execute, depending on the number of switches and network conditions. Ensure that the user running the script has the necessary permissions and network connectivity to the switches.
   ```

