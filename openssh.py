#!/usr/bin/python3

""" Simple CGI to add an ip in a text file.

pyiptable read the file and open firewall.
"""

import cgi
import os
from ipaddress import IPv4Interface

STATUS_PATH = "/var/lib/opensshcgi/status"
NEWIP_PATH = "/var/lib/opensshcgi/newip"

def check_addr(addr):
    """ Return canonical address:
    192.168.0.1/32
    192.168.0.0/24
    """

    return IPv4Interface(addr).network.with_prefixlen

def main():
    print("""Content-Type: text/html


<!DOCTYPE HTML>
<html><head><meta charset="utf-8"><title>ssh page</title></head>
<body>""")

    form = cgi.FieldStorage()
    addr = form.getfirst("addr")

    if addr:
        try:
            addr = check_addr(addr)
            fp = open(NEWIP_PATH, 'w')
            fp.write("%s\n" % addr)
            fp.close()
            print("<p>add ip %s</p>" % addr)
        except:
            print("<p>invalid address %s</p>" % addr)

    try:
        with open(STATUS_PATH) as statusfile:
            print("<ul>")
            for line in statusfile.readlines():
                print("<li>%s</li>" % line)
            print("</ul>")
    except:
        pass

    print("""<form action="/cgi-bin/openssh.py" method="POST">
ip: <input type="text" name="addr" value="%s">
<input type="submit">
</form>
</body></html>
""" % cgi.escape(os.getenv("REMOTE_ADDR", "")))

if __name__ == "__main__":
    main()

