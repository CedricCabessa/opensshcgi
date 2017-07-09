# OpensshCgi

Allow ssh access from a specific IP or IP range through a simple cgi page

## FAQ
### Why?

A ssh port is often subject to scan / attack from the wild internet. You can use
fail2ban to block attackers, but I've observed the same IP trying again after
the jail period.

A safer solution is to whitelist the IP you want to allow. The issue is to setup
this list of IPs.

That is the purpose of this script. You can dynamically add one or more IP to
your whitelist.

### Is that a replacement of fail2ban?

No. You are encouraged to continue using fail2ban.

This tool will reduce the attack surface of fail2ban and the spam in your log.

### Who can add IP in the whitelist?

You should protect this script with an apache authentication.

### Is that security through obscurity?

It is an additional layer to access your ssh port.

Continue to protect your ssh keys and use proven tools like fail2ban.

### IPv6?

Lol

## Architecture

The cgi script will write a file with the IP or IP range to allow.

Every 15min a cron script (running as root) read the file and call iptables to
allow the IPs.

The cron script also generate a status file with the list of allowed IP to be
read by the cgi script.

By design, the whitelist is not saved on reboot.

## Installation

### Requirement

[python-iptables](https://pypi.python.org/pypi/python-iptables)

### Deploy cgi

Copy openssh.py in `/usr/lib/cgi-bin/`

You should protect the access to the cgi with a password. For apache, add the
following:

```
<location /cgi-bin/openssh.py>
	  AuthName "openssh cgi access"
          AuthType Basic
          AuthBasicProvider file
          AuthUserFile /usr/lib/cgi-bin/openssh-htpasswd
          Require user openssh
</location>
```

Create the password file:

```
htpasswd -c /usr/lib/cgi-bin/openssh-htpasswd openssh
```

Then reload apache

Create a folder where the cgi can write:

```
mkdir /var/lib/opensshcgi
touch /var/lib/opensshcgi/newip
chown -R www-data:www-data /var/lib/opensshcgi
```

copy pyiptable.py in `/usr/local/bin`

copy cron/sshcgi in `/etc/cron.d/`
