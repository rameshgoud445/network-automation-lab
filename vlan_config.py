from netmiko import ConnectHandler

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
    }

    try:
        # Establish SSH connection
        connection = ConnectHandler(**switch)

        # Enter enable mode
        connection.enable()

        # VLAN configuration commands
        vlan_commands = [
            f"vlan {vlan_id}",
            f"name {vlan_name}",
            "exit"
        ]

        # Send configuration
        output = connection.send_config_set(vlan_commands)
        print("\nConfiguration Output:\n")
        print(output)

        # Save configuration
        save_output = connection.send_command("write memory")
        print(save_output)

        # Verify VLAN
        verify_output = connection.send_command("show vlan brief")
        print("\nVLAN Verification:\n")
        print(verify_output)

        # Close connection
        connection.disconnect()

        print(f"✅ VLAN {vlan_id} configured successfully on {ip}")

    except Exception as e:
        print(f"❌ Error on {ip}: {e}")
vlan_commands = [
    f"vlan {vlan_id}",
    f"name {vlan_name}",
    "exit",
    "interface e0/1",
    "switchport mode access",
    f"switchport access vlan {vlan_id}",
    "no shutdown"
]