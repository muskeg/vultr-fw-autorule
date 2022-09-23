#!/usr/bin/python3


import sys
if sys.version_info[0] == 2:
    from ConfigParser import RawConfigParser
if sys.version_info[0] >= 3:
    from configparser import RawConfigParser
import requests
import json
from datetime import datetime


# read configuration file
config_file_name = sys.argv[1] or "vultr.config"
config = RawConfigParser()
config.read(config_file_name)

# Parse config
firewall_groupid = config.get("vultr", "firewall_groupid")
api_key = config.get("vultr", "api_key")
filename = config.get("vultr", "tracking_filename")
ports_list = json.loads(config.get("rules", "ports"))

ip = requests.get('https://api.ipify.org').text
vultr_create_api = "https://api.vultr.com/v2/firewalls/" + firewall_groupid + "/rules"
vultr_delete_base ="https://api.vultr.com/v2/firewalls/" + firewall_groupid + "/rules/"

headers = {'Authorization': 'Bearer ' + api_key}

fw_rules = open(filename, 'r')
rules_list = fw_rules.readlines()

for rule_number in rules_list:
    r = requests.delete(vultr_delete_base + rule_number.strip(), headers=headers)
fw_rules.close()


fw_rules = open(filename, 'w')
for desc, port in ports_list.items():
    data_create = {
        'souce': '',
        'ip_type': 'v4',
        'protocol':  port['protocol'],
        'subnet': ip,
        'subnet_size': '32',
        'port': port['port'],
        'notes': 'auto ' + desc + ' rule'
    }

    r = requests.post(vultr_create_api, json=data_create, headers=headers)
    result = json.loads(r.content)
    if r.status_code == 201:

        print("Rule for " + desc + " created. Rule number: " + str(result['firewall_rule']['id']))
        fw_rules.write(str(result['firewall_rule']['id']) + "\n")
    else:
        print(r.content)

fw_rules.close()
