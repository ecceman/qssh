#!/usr/bin/env python3
import yaml
import sys
import fnmatch
import os
import time
import argparse
import subprocess

hosts_file = '~/hosts.yml'
ssh_arguments = '-oKexAlgorithms=+diffie-hellman-group14-sha1 -oHostKeyAlgorithms=+ssh-rsa -oCiphers=+aes256-cbc'


def debug(msg):
    print(f"[qssh] {msg}")


def load_hosts(data):
    expanded = []
    default_username = args.username or data.get("username", "")
    domains = data.get("domains", {})

    def walk(domain_name, section, inherited_username):
        # Determine username for this section
        section_username = section.get("username", inherited_username)

        # hosts section
        for host in section.get("hosts", []):
            fqdn = f"{host}.{domain_name}"
            expanded.append({"raw": host, "fqdn": fqdn, "username": section_username})

        # subdomains section
        for sub, subdata in section.get("subdomains", {}).items():
            subdomain_fq = f"{sub}.{domain_name}"
            walk(subdomain_fq, subdata, section_username)

    for top_domain, section in domains.items():
        walk(top_domain, section, default_username)

    return expanded


def open_iterm(hosts):
    if not hosts:
        return

    apple_script = '''
    tell application "iTerm2"
        activate
        set newWindow to (create window with default profile)
    '''

    for idx, h in enumerate(hosts):
        hostname = h["fqdn"].split(".")[0]
        cmd = f"ssh {h['username']}@{h['fqdn']} {ssh_arguments}"

        if idx == 0:
            # First host: use the first tab in the new window
            apple_script += f'''
                tell current session of newWindow
                    set name to "{hostname}"
                    write text "{cmd}"
                end tell
            '''
        else:
            # Subsequent hosts: create a new tab in the new window
            apple_script += f'''
                tell newWindow
                    create tab with default profile
                    tell current session
                        set name to "{hostname}"
                        write text "{cmd}"
                    end tell
                end tell
            '''

    apple_script += "\nend tell"

    import subprocess
    subprocess.run(["osascript", "-e", apple_script])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", help="Quoted string that takes wildcards, e.g. 'server4*.domain.com'")
    parser.add_argument("username", nargs="?", help="Optional username override")
    parser.add_argument("-d", "--debug", help="Print debug messages", action="store_true")
    parser.add_argument("-m", "--match-only", help="Only match YAML file, don't connect", action="store_true")
    args = parser.parse_args()
    pattern = args.pattern

    debug("Loading hosts.yml...")

    if not os.path.exists(hosts_file):
        debug("ERROR: hosts.yml not found.")
        sys.exit(1)

    with open(hosts_file) as f:
        data = yaml.safe_load(f)

    all_hosts = load_hosts(data)

    debug(f"Loaded {len(all_hosts)} hosts from YAML")

    if args.debug:
        debug(f"Matching pattern: {pattern}")
        for h in all_hosts:
            debug(f"  - raw={h['raw']}  fqdn={h['fqdn']}  username={h['username']}")
        

    exact = [h for h in all_hosts if h["raw"].lower() == pattern.lower()]

    if len(exact) == 1:
        matched = exact
    else:
        partial = [h for h in all_hosts if pattern.lower() in h["raw"].lower()]
        if partial:
            matched = partial
        else:
            matched = [h for h in all_hosts if fnmatch.fnmatch(h["fqdn"], pattern)]

    # Eliminate duplicates that may have snuck into the yaml file, keep the last one found
    matched = list({d["fqdn"]: d for d in matched}.values())

    if not matched:
        debug("No hosts matched!")
        sys.exit(1)

    debug(f"Matched {len(matched)} host(s):")
    for m in matched:
        debug(f"  → {m['fqdn']} ({m['username']})")
        # Ping the device, to get ARP and possible session-NAT to wake up and not randomly brake SSH later on
        subprocess.run(
            ["ping", "-c", "1", "-W", "1", m['fqdn']],   # This is windows incompatible 👍
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if args.debug:
            debug(f"[qssh] Quick ping {m['fqdn']}")
        
        time.sleep(0.1)

    if not args.match_only:
        debug("Sending commands to iTerm2...")
        open_iterm(matched)
    else:
        debug("Match only, will not start iTerm sessions")

    debug("Done.")
