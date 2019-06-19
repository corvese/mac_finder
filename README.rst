MAC Address Finder
==================
Searches multiple Cisco switches to find the access port a MAC address resides on (ignores trunk ports)

Why?
----

Often times you must find where a certain device is plugged into on a network that is
comprised of many switches. Doing this manually via a terminal can take quite a bit of time.

Usage
-----

``cisco_mac_finder.py`` will search IP addresses inputted in a textfile named ``switches.txt`` for a MAC address. 
Username, password and MAC addresses are submitted as user input when ``cisco_mac_finder.py`` is initialized

Place one switch IP address per line in ``switches.txt``. Make sure it is in the same directory as
``cisco_mac_finder.py``

If a MAC address is found, information will be outputed into the terminal:

EXAMPLE:

::

    MAC ADDRESS: 906c.ace1.41bd
    DEVICE IP: 10.0.20.113
    PORT: Gi0/0









