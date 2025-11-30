# qssh
Connect to multiple SSH destinations simultaneously. 

The yaml file lists your destinations (servers, network devices etc) in a DNS subdomain tree structure. It also allows you to – optionally – specify the username for each domain and sub domain.

The python file parses the yaml file, matches the destination pattern you entered and fire up tabs in a new iTerm2 window. You can then manage multiple devices individually by switching through the tabs, or all at once using iTerm2 broadcast feature (⌘ + ⇧ + I). Qssh do not store nor handles passwords. Usernames can be defined in the yaml file at all levels, with more specific ones overriding more generic ones. Username can also be optionally added in the CLI command, overriding the YAML file.

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
❯ qssh "someswi*"
[qssh] Loading hosts.yml...
[qssh] Loaded 297 hosts from YAML
[qssh] Matched 13 host(s):
[qssh]   → someswi21.mydomain.com (anakin)
[qssh]   → someswi20.mydomain.com (anakin)
[qssh]   → someswi22.mydomain.com (anakin)
[qssh]   → someswi19.mydomain.com (anakin)
[qssh]   → someswi13.mydomain.com (anakin)
[qssh]   → someswi12.mydomain.com (anakin)
[qssh]   → someswi15.mydomain.com (anakin)
[qssh]   → someswi14.mydomain.com (anakin)
[qssh]   → someswi16.mydomain.com (anakin)
[qssh]   → someswi18.mydomain.com (anakin)
[qssh]   → someswi17.mydomain.com (anakin)
[qssh]   → someswi11.mydomain.com (anakin)
[qssh]   → someswi01.mydomain.com (anakin)
[qssh] Sending commands to iTerm2...
[qssh] Done.
```
![alt text](https://github.com/ecceman/qssh/blob/main/qssh-screenshot.png)

Some iTerm2 settings you might want to consider:
- General → Window: Adjust window when changing font size
- Appearance → General: Tab bar location = Left
- Appearance → Tabs: Show tab numbers
- Appearance → Tabs: Tbas have close buttons
- Appearance → Tabs: Show activity indicator
- Appearance → Tabs: Show new-output indicator
- Profiles → Default → General: Title = Name
- Profiles → Default → Text: Font = MesloLGS NF
- Profiles → Default → Terminal: Flash visual bell
- Profiles → Default → Advanced → Triggers: Use for regex-match output and get syntax highlighing
