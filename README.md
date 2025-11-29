# qssh
Connect to multiple SSH destinations simultaneously. 

The yaml file lists your destinations (servers, network devices etc) in a DNS subdomain tree structure. It also allows you to – optionally – specify the username for each domain and sub domain.

The python file parses the yaml file, matches the destination pattern you entered and fire up tabs in a new iTerm2 window. You can then manage multiple devices individually by switching through the tabs, or all at once using iTerm2 broadcast feature (⌘ + ⇧ + I). Qssh do not store nor handles passwords. Usernames can be defined in the yaml file at all levels, with more specific ones overriding more generic ones. Username can also be optionally added in the CLI command, overriding the YAML file.

If =< 6 hosts are matches the tabs are shown side by side in the window. If >6 the tabs are stacked.

```
❯ qssh -h
usage: qssh.py [-h] [-d] [-m] pattern [username]

positional arguments:
  pattern           Quoted string that takes wildcards, e.g. 'server4*.domain.com'
  username          Optional username override

optional arguments:
  -h, --help        show this help message and exit
  -d, --debug       Print debug messages
  -m, --match-only  Only match YAML file, don't connect
```

### Example

```
❯ qssh "coreswi*"
[qssh] Loading hosts.yml...
[qssh] Loaded 301 hosts from YAML
[qssh] Matched 3 host(s):
[qssh]   → coreswi14.acme.domain.com (anakin)
[qssh]   → coreswi15.acme.domain.com (anakin)
[qssh]   → coreswi16.acme.domain.com (anakin)
[qssh] Sending commands to iTerm2...
[qssh] Done.
```
