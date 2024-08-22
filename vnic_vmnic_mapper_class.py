# docstring
"""
This module defines VnicVmnicMapperClient class and methods to map vNIC to vmnic.

"""

#!/usr/bin/env python3

from prettytable import PrettyTable

from esx_client_class import EsxClient
from intersight_client_class import IntersightClient


##############################################################################
#                        VnicVmnicMapperClient class                         #
##############################################################################


class VnicVmnicMapperClient:
    """
    A class representing a client for mapping UCS virtual interfaces vNIC to ESXi physical adapters vmnic.

    This class provides various methods.

    Attributes:
        esx_client_instance (EsxClient): An instance of the EsxClient class.
        intersight_client_instance (IntersightClient): An instance of the IntersightClient class.
        vnic_vmnic_mapping_dic (dict): A dictionary to store the mapping of vNIC to vmnic.
    """

    def __init__(self, esx_client_instance, intersight_client_instance):
        if not isinstance(esx_client_instance, EsxClient):
            raise TypeError("esx_client_instance must be an instance of EsxClient")
        if not isinstance(intersight_client_instance, IntersightClient):
            raise TypeError(
                "intersight_client_instance must be an instance of IntersightClient"
            )
        self.esx_client_instance = esx_client_instance
        self.intersight_client_instance = intersight_client_instance
        self.vnic_vmnic_mapping_dic = {}

    def map_vnic_vmnic(self):
        """
        Maps vNIC to vmnic.

        This method maps vNIC to vmnic by comparing the MAC addresses of the vNIC and vmnic.
        It then prints a tabular view that presents the mapping of vNIC to vmnic.

        Args:
            None
        """
        for vswitch in self.esx_client_instance.vswitch_vmnic_dic.keys():
            self.vnic_vmnic_mapping_dic[vswitch] = {"vmnic": []}
            for vmnic in self.esx_client_instance.vswitch_vmnic_dic[vswitch]["vmnic"]:
                matching_vnics = [
                    vnic
                    for vnic in self.intersight_client_instance.vnic_dic["vnic"]
                    if vmnic["mac_address"] == vnic["mac_address"]
                ]
                self.vnic_vmnic_mapping_dic[vswitch]["vmnic"].extend(
                    {
                        "device": vmnic["device"],
                        "mac_address": vmnic["mac_address"],
                        "vnic": vnic["name"],
                        "fabric_interconnect": vnic["fabric_interconnect"],
                    }
                    for vnic in matching_vnics
                )

        # Create a PrettyTable object
        for vswitch_key, vswitch_value in self.vnic_vmnic_mapping_dic.items():
            table = PrettyTable()
            table.field_names = [
                "vSwitch",
                "vNIC",
                "vmnic",
                "MAC Address",
                "Fabric Interconnect",
            ]

            # Add data to the table
            for vmnic in self.vnic_vmnic_mapping_dic[vswitch_key]["vmnic"]:
                table.add_row(
                    [
                        vswitch_key,
                        vmnic["vnic"],
                        vmnic["device"],
                        vmnic["mac_address"],
                        vmnic["fabric_interconnect"],
                    ]
                )

            # Print the table
            print("-----------------------------------------------------------")
            print(f"vNIC to vmnic mapping for vSwitch *{vswitch_key}*")
            print("-----------------------------------------------------------")
            print(table)
            print("\n")


if __name__ == "__main__":
    pass
