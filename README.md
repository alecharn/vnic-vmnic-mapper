# vnic-vmnic-mapper

This repository contains a utility script for mapping UCS virtual network interface cards (vNIC) to ESXi physical NICs (vmnic) in Cisco UCS environments. ESXi physical NICs or physical adapters are used as uplinks of ESXi virtual switches. 

This script simplifies the process of mapping vNIC to vmnic, making it easier to manage network configurations.

## Installation and Usage

To use this script, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Populate the variables in `main.py` file.
4. Run the script using the command `python main.py`.

## Configuration

The `main.py` file contains the following configuration options:

- `ESXI_HOST` : The IP address of the ESXi host.
- `ESXI_USER`: The username for authenticating with the ESXi host.
- `ESXI_PASSWORD`: The password for authenticating with the ESXi host.
- `INTERSIGHT_URL` : The URL of Intersight SaaS or Appliance.
- `INTERSIGHT_KEY_ID` : The API Key ID of Intersight.
- `INTERSIGHT_SECRET_KEY_PATH` : The API Secret Key Path of Intersight.
- `SERVER_PROFILE`: The name of the Server Profile to map vNICs for.

You can populate these variables directly in the `main.py` file or you can define them in a `.env` file (that uses the `load_dotenv()` and `os.getenv()` function).

## Output

The script prints in the terminal a table showing the mappings of vNIC to vmnic for each ESXi vSwitch :

```
-----------------------------------------------------------
vNIC to vmnic mapping for vSwitch *vSwitch0*
-----------------------------------------------------------
+----------+--------+--------+-------------------+---------------------+
| vSwitch  |  vNIC  | vmnic  |    MAC Address    | Fabric Interconnect |
+----------+--------+--------+-------------------+---------------------+
| vSwitch0 | mgmt-b | vmnic1 | 00:a0:d7:42:00:02 |          B          |
| vSwitch0 | mgmt-A | vmnic0 | 00:a0:d7:42:00:01 |          A          |
+----------+--------+--------+-------------------+---------------------+
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
