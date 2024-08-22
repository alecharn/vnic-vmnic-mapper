# docstring
"""
This script performs the mapping of vNICs to corresponding vmnic in a VMware ESXi host using Intersight API.

Usage:
- Ensure that the necessary environment variables are set in the parameters section of the main file or in an environment file.
- Run the script to perform the vNIC to vmnic mapping.
"""

#!/usr/bin/env python3

import os

from dotenv import load_dotenv

from esx_client_class import EsxClient
from intersight_client_class import IntersightClient
from vnic_vmnic_mapper_class import VnicVmnicMapperClient


###############################################################################
#                               Parameters                                    #
###############################################################################

# .ENV.MAIN
load_dotenv()
MAIN_ENV_PATH = os.getenv("MAIN_ENV_PATH")
load_dotenv(MAIN_ENV_PATH)

# ESXi Host
ESXI_HOST = "10.10.10.101"
ESXI_USER = os.getenv("ESXI_USER")
ESXI_PASSWORD = os.getenv("ESXI_PASSWORD")

# Intersight
INTERSIGHT_URL = "https://intersight.com"
INTERSIGHT_KEY_ID = os.getenv("INTERSIGHT_KEY_ID")
INTERSIGHT_SECRET_KEY_PATH = os.getenv("INTERSIGHT_SECRET_KEY_PATH")

# UCS Server Profile
SERVER_PROFILE = "ESX-demo-alecharn-1"


###############################################################################
#                                   Main                                      #
###############################################################################

if __name__ == "__main__":
    # Create an instance of the EsxClient class
    esx_client_instance = EsxClient(host=ESXI_HOST, user=ESXI_USER, pwd=ESXI_PASSWORD)
    esx_client_instance.get_vswitch_vmnic_info()

    # Create an instance of the IntersightClient class
    intersight_client_instance = IntersightClient(
        intersight_key_id=INTERSIGHT_KEY_ID,
        intersight_secret_key_path=INTERSIGHT_SECRET_KEY_PATH,
        intersight_url=INTERSIGHT_URL,
    )
    intersight_client_instance.get_vnic_info(
        server_profile_moid=intersight_client_instance.fetch_server_profile_moid_from_server_profile_name(
            server_profile_name=SERVER_PROFILE
        )
    )

    # Create an instance of the VnicVmnicMapperClient class
    vnic_vmnic_mapper_instance = VnicVmnicMapperClient(
        esx_client_instance, intersight_client_instance
    )
    vnic_vmnic_mapper_instance.map_vnic_vmnic()
