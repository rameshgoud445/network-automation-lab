from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# List of switch IPs
switch_ips = [
    "192.168.12.140",
    "192.168.12.141",
    "192.168.12.142"
]

# VLAN Details
vlan_1_id = 10
vlan_1_name = "USERS"

vlan_2_id = 20
vlan_2_name = "SERVERS"

for ip in switch_ips:
    print(f"\n🔧 Connecting to Switch {ip}")

    switch = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": "admin",
        "password": "cisco123",
        "secret": "cisco123",
        "global_delay_factor": 2,
        "fast_cli": False   # Important for EVE-NG stability
    }

    try:
        connection = ConnectHandler(**switch)

        # Enter enable mode
        connection.enable()
        print("✅ Connected Successfully")

        # VLAN configuration
        vlan_commands = [
            # VLAN 10
            f"vlan {vlan_1_id}",
            f"name {vlan_1_name}",
            "exit",

            # VLAN 20
            f"vlan {vlan_2_id}",
            f"name {vlan_2_name}",
            "exit",

            # Assign VLAN 10
            "interface Ethernet3/3",
            "switchport mode access",
            f"switchport access vlan {vlan_1_id}",
            "no shutdown",
            "exit",

            # Assign VLAN 20
            "interface Ethernet3/4",
            "switchport mode access",
            f"switchport access vlan {vlan_2_id}",
            "no shutdown",
            "end"
        ]

        # Send configuration
        output = connection.send_config_set(vlan_commands)
        print("\n📌 Configuration Output:\n")
        print(output)

        # Save config
        print("\n💾 Saving configuration...")
        save_output = connection.save_config()
        print(save_output)

        # Verify VLAN
        print("\n🔍 Verifying VLAN...")
        verify_output = connection.send_command("show vlan brief")
        print(verify_output)

        # Disconnect
        connection.disconnect()
        print(f"🔌 Disconnected from {ip}")

    except NetmikoTimeoutException:
        print(f"❌ Timeout while connecting to {ip}")

    except NetmikoAuthenticationException:
        print(f"❌ Authentication failed for {ip}")

    except Exception as e:
        print(f"❌ Error on {ip}: {str(e)}")