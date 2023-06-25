# Vultr Firewall Auto-rules
Script to update Vultr's firewall rules for dynamic public IP addresses.
It uses the client's public IP and creates/updates rules according to the configuration file

The script tracks created rules in a file in order to clean them up during rotation.

## How-to
The script expects a mandatory positional argument to specify the configuration file:

```
╰─ ./vultr-fw.py vultr.config 
Rule for icmp created. Rule number: 2
Rule for ssh created. Rule number: 3
Rule for snmp created. Rule number: 4

```

## Files

### vultr.config.example

An example/template of the required configuration file

```
[vultr]
# Find the group ID in the firewall resources page
firewall_group_id = THE_FIREWALL_GROUP_ID

# Generate API key from account settings
api_key = YOUR_API_KEY

# Rename accordingly
tracking_filename = vultr.rules.example

[rules]
ports = {
        "service1": {"port": "8080", "protocol": "tcp"},
        "service2": {"port": "8666", "protocol": "udp"},
        "service3": {"port": "22222", "protocol": "tcp"},
        "service4": {"port": "10010", "protocol": "tcp"},
        "ssh": {"port": "22", "protocol": "tcp"}
    }
```
The rules section is a dictionary of rules that will be created in the firewall group. The keys should be explicit enough.

The service name is used in the rule's annotation. 

The script does not support custom source IP at the moment and will always use the client's public IP.


### vultr-fw.py

The firewall client script. The script expects the path to the configuration file as a mandatory positional argument.