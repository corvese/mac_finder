from netmiko import ConnectHandler
import getpass
import re

username = input("Username: ")
password = getpass.getpass("Password: ")
mac_address = input("Enter the MAC address you want to find (e.g a4f3.5f32.38fa - ALL IN LOWER CASE): ")
print('Searching...')

switches = open('switches.txt', 'r')
list_of_switches = switches.readlines()

def connect_to_switch(switch, username, password):
    """Connects to a switch and creates an SSH session to send commands to
    
    params
    switch = switch ip (str)
    username = switch login username (str)
    password = switch login password (str)

    returns: switch ssh session (class)
    """
    switch =  ConnectHandler(ip=switch, device_type='cisco_ios', username=username, password=password)
    return switch

def find_mac_address_and_port(switch_session, mac_address):
    """Searched the MAC address table to see if the MAC address is present on the device
    
    Params:
    switch_session = switch ssh session(object)
    mac_address = MAC address to find (str)

    Returns: MAC address and port found on (str)"""
    local_regex = '(\s*\w*)\s*(\w{4}.\w{4}.\w{4})\s*(\w*)\s*(.*)'
    mac_table = switch_session.send_command('show mac address-table')
    list = mac_table.splitlines()
    for line in list:
        if mac_address in line:
            mac_address = re.search(local_regex, line).group(2)
            port = re.search(local_regex, line).group(4)
    return mac_address, port

def validate_switchport(switch_session, switch_ip, mac_address, port):
    """Checks if the MAC address found was found on an access port and not a trunk

    params:
    switch_session = switch ssh session(object)
    switch_ip = ip address of switch (str)
    mac_address = MAC address to find (str)
    port = Port MAC address was found on (str)

    returns: Prints if switch found or not (bool)    """
    interface_status = switch_session.send_command('show interface status')
    switch_session.close()
    list = interface_status.splitlines()
    for line in list:
        if port in line and 'trunk' not in line:
            print("""
            MAC ADDRESS: {0}
            DEVICE IP: {1}
            PORT: {2}""".format(mac_address, switch_ip, port))
    
for switch_ip in list_of_switches:
    switch_session = connect_to_switch(switch_ip, username, password)
    mac_address_output = find_mac_address_and_port(switch_session, mac_address)
    validate_switchport(switch_session, switch_ip, mac_address_output[0], mac_address_output[1])

print('Search completed')

