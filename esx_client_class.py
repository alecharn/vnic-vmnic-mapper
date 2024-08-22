# docstring
"""
This module provides a class for interacting with VMware ESXi.
"""

#!/usr/bin/env python3

import ssl
import urllib3

from prettytable import PrettyTable
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


##############################################################################
#                             EsxClient class                                #
##############################################################################


class EsxClient:
    """
    A class representing a client for interacting with VMware ESXi.

    This class provides various methods.

    Attributes:
        host (str): The hostname or IP address of the ESXi host.
        user (str): The username for connecting to the ESXi host.
        pwd (str): The password for connecting to the ESXi host.
        context (ssl.SSLContext): The SSL context for the ESXi host connection.
        vswitch_vmnic_dic (dict): A dictionary to store vSwitch and vmnic information.
    """

    def __init__(self, host, user, pwd):
        self._host = host
        self._user = user
        self._pwd = pwd
        self._context = ssl._create_unverified_context()
        self.vswitch_vmnic_dic = {}

    def get_vswitch_vmnic_info(self):
        """
        Get the vSwitches and their associated vmnic information.

        This method connects to the ESXi host and retrieves the vSwitches and their associated vmnic information.
        It then prints a tabular view that presents for each vSwitch the vmnic device and MAC address.

        Args:
            None
        """
        # Connect to the ESXi host
        si = SmartConnect(
            host=self._host, user=self._user, pwd=self._pwd, sslContext=self._context
        )
        content = si.RetrieveContent()

        # Get the host system
        host_system = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.HostSystem], True
        ).view[0]

        # Iterate through the vSwitches and get the vmnic information
        for vswitch in host_system.config.network.vswitch:
            self.vswitch_vmnic_dic[vswitch.name] = {"vmnic": []}
            for pnic in vswitch.pnic:
                self.vswitch_vmnic_dic[vswitch.name]["vmnic"].append({"key": pnic})

            for pnic in host_system.config.network.pnic:
                for vmnic_key in self.vswitch_vmnic_dic[vswitch.name]["vmnic"]:
                    if pnic.key == vmnic_key["key"]:
                        vmnic_key["device"] = pnic.device
                        vmnic_key["mac_address"] = pnic.mac

        # Create a PrettyTable object
        table = PrettyTable()
        table.field_names = ["vSwitch", "vmnic", "vmnic MAC Address"]

        # Add data to the table
        for vswitch_name, vswitch_info in self.vswitch_vmnic_dic.items():
            for vmnic in vswitch_info["vmnic"]:
                table.add_row([vswitch_name, vmnic["device"], vmnic["mac_address"]])

        # Print the table
        print("-----------------------------------------------------------")
        print(f"vSwitch and vmnic of ESXi host *{self._host}*")
        print("-----------------------------------------------------------")
        print(table)
        print("\n")

        # Disconnect from the ESXi host
        Disconnect(si)


if __name__ == "__main__":
    pass
