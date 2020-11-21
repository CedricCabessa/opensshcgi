#!/usr/bin/python3

""" add iptable rule for ssh
"""

import sys
import iptc


def create_rule(ipaddr):
    """Create a rule object. Iptables is not modified at this point.
    ipaddr is:
       192.168.0.1/32
       192.168.0.0/24
    """
    rule = iptc.Rule()
    rule.protocol = "tcp"
    rule.target = iptc.Target(rule, "ACCEPT")
    match = rule.create_match("tcp")
    match.dport = "22"
    rule.src = ipaddr

    return rule


def add_rule(rule):
    """Add a rule in the INPUT chain"""
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    chain.insert_rule(rule)


def rule_exists(rule):
    """Return true if a rule already exists in the INPUT chain"""
    table = iptc.Table(iptc.Table.FILTER)
    for chain in table.chains:
        if chain.name == "INPUT":
            for r in chain.rules:
                if r == rule:
                    return True
    return False


def getsources():
    """get all the sources allowed to use ssh"""
    sources = []
    table = iptc.Table(iptc.Table.FILTER)
    for chain in table.chains:
        if chain.name == "INPUT":
            for rule in chain.rules:
                for match in rule.matches:
                    if match.dport == "22":
                        sources.append(rule.src)
    return sources


if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as fp:
            for line in fp.readlines():
                line = line.strip()
                try:
                    rule = create_rule(line)
                except ValueError:
                    pass
                if not rule_exists(rule):
                    add_rule(rule)
        # truncate file (do not erase, cgi may not have write access on the
        # folder)
        with open(sys.argv[1], "w"):
            pass

        print("\n".join(getsources()))
