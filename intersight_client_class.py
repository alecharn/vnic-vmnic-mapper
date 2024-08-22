# docstring
"""
This module defines IntersightClient class and methods to interact with Intersight API.
"""

#!/usr/bin/env python3

import datetime
import urllib3
import intersight

from prettytable import PrettyTable
from intersight.api import vnic_api, server_api

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


##############################################################################
#                          IntersightClient class                            #
##############################################################################


class IntersightClient:
    """
    A class representing a client for interacting with Cisco Intersight.

    This class provides various methods.

    Attributes:
        _intersight_key_id (str): The Intersight key ID.
        _intersight_secret_key_path (str): The path to the Intersight secret key.
        _intersight_url (str): The URL of the Cisco Intersight.
        _api_client (intersight.ApiClient): The Intersight API client.
        vnic_dic (dict): A dictionary to store the vNIC information.
    """

    def __init__(self, intersight_key_id, intersight_secret_key_path, intersight_url):

        self._intersight_key_id = intersight_key_id
        self._intersight_secret_key_path = intersight_secret_key_path
        self._intersight_url = intersight_url
        self._api_client = self.authenticate_and_assign_intersight_api_client()
        self.vnic_dic = {"vnic": []}

    def authenticate_and_assign_intersight_api_client(self):
        """
        Authenticate and assign the Intersight API client.

        This method authenticates with the Intersight API and assigns the API client.

        Args:
            None

        Returns:
            intersight.ApiClient: The Intersight API client.
        """

        intersight_key_id = self._intersight_key_id

        configuration = intersight.Configuration(
            host=self._intersight_url,
            signing_info=intersight.signing.HttpSigningConfiguration(
                key_id=intersight_key_id,
                private_key_path=self._intersight_secret_key_path,
                # For OpenAPI v2
                # signing_scheme=intersight.signing.SCHEME_RSA_SHA256,
                # For OpenAPI v3
                signing_scheme=intersight.signing.SCHEME_HS2019,
                # For OpenAPI v2
                # signing_algorithm=intersight.signing.ALGORITHM_RSASSA_PKCS1v15,
                # For OpenAPI v3
                signing_algorithm=intersight.signing.ALGORITHM_ECDSA_MODE_FIPS_186_3,
                signed_headers=[
                    intersight.signing.HEADER_REQUEST_TARGET,
                    intersight.signing.HEADER_CREATED,
                    intersight.signing.HEADER_EXPIRES,
                    intersight.signing.HEADER_HOST,
                    intersight.signing.HEADER_DATE,
                    intersight.signing.HEADER_DIGEST,
                    "Content-Type",
                    "User-Agent",
                ],
                signature_max_validity=datetime.timedelta(minutes=5),
            ),
        )

        configuration.discard_unknown_keys = True
        configuration.disabled_client_side_validations = "minimum"
        configuration.verify_ssl = False
        api_client = intersight.ApiClient(configuration)
        api_client.set_default_header("Content-Type", "application/json")

        return api_client

    def fetch_server_profile_moid_from_server_profile_name(self, server_profile_name):
        """
        Fetch the server profile MOID from the server profile name.

        This method connects to the Intersight API and retrieves the server profile MOID from the server profile name.

        Args:
            server_profile_name (str): The name of the server profile.

        Returns:
            str: The managed object ID of the server profile.

        Raises:
            None
        """

        api_instance = server_api.ServerApi(self._api_client)

        try:
            # Create a filter to get the server profile moid
            filter_str = f"Name eq '{server_profile_name}'"

            # Get the server profile moid
            server_profiles = api_instance.get_server_profile_list(filter=filter_str)

            # Return the server profile moid
            return server_profiles.results[0].moid

        except Exception as e:
            print("Exception when calling ServerApi->get_server_profiles: %s\n", e)

    def get_vnic_info(self, server_profile_moid):
        """
        Get the vnics associated with a server and print a tabular view of the vnics and their mac address.

        This method connects to the Intersight API and retrieves the vnics associated with a server.
        It then prints a tabular view that presents for each vnic their MAC address.

        Args:
            server_profile_moid (str): The managed object ID of the server profile.

        Returns:
            None

        Raises:
            None
        """
        api_instance = vnic_api.VnicApi(self._api_client)

        try:
            # Create a filter to get the vnics associated with the server moid
            filter_str = f"Profile.Moid eq '{server_profile_moid}'"

            # Get the vnics associated with the server
            vnics = api_instance.get_vnic_eth_if_list(filter=filter_str)

            # Create a PrettyTable object
            table = PrettyTable()
            table.field_names = ["vNIC", "Fabric Interconnect", "MAC Address"]

            # Add data to the table
            for vnic in vnics.results:
                self.vnic_dic["vnic"].append(
                    {
                        "name": vnic.name,
                        "mac_address": vnic.mac_address.lower(),
                        "fabric_interconnect": vnic.placement.switch_id,
                    }
                )
                table.add_row(
                    [vnic.name, vnic.placement.switch_id, vnic.mac_address.lower()]
                )

            # Print the table
            print("-----------------------------------------------------------")
            print(f"vNIC of UCS host with server profile *{server_profile_moid}*")
            print("-----------------------------------------------------------")
            print(table)
            print("\n")

        except Exception as e:
            print("Exception when calling VnicApi->get_vnics: %s\n", e)


if __name__ == "__main__":
    pass
