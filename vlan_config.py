from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# List of switch IPs
switch_ips = [
    "192.168.12.140",
    "192.168.12.141",
    "192.168.12.142"
]

# VLAN Details
vlan_id = 10
vlan_name = "USERS"

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
            f"vlan {vlan_id}",
            f"name {vlan_name}",
            "exit",
            "interface Ethernet3/3",   # FIXED INTERFACE NAME
            "switchport mode access",
            f"switchport access vlan {vlan_id}",
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