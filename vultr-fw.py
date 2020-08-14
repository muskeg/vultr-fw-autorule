#!/usr/bin/python3
import sys
import requests
import json
from datetime import datetime


ip = requests.get('https://api.ipify.org').text
vultr_create = "https://api.vultr.com/v1/firewall/rule_create"
vultr_delete ="https://api.vultr.com/v1/firewall/rule_delete"
existing_rule = 1
firewall_groupid = 'THE_FIREWALLGROUPID (as seen in the firewall page url)'
api_key = 'YOUR_API_KEY'
filename = 'PATH/TO/A/FILE/TO/KEEP/TRACK/OF/CREATED_RULES'
ports_list = {
    'jenkins': {'port': '8080', 'protocol': 'tcp'},
    'k3s-flannel': {'port': '8472', 'protocol': 'udp'},
    'k3s-kubelet': {'port': '10250', 'protocol': 'tcp'},
    'cockpit': {'port': '9090', 'protocol': 'tcp'},
    'ssh': {'port': '22', 'protocol': 'tcp'}
}



headers = {'API-Key': api_key}

fw_rules = open(filename, 'r')
rules_list = fw_rules.readlines()

for rule_number in rules_list:
    data_delete = {
        'FIREWALLGROUPID': firewall_groupid,
        'rulenumber': rule_number.strip()
    }
    r = requests.post(vultr_delete, data=data_delete, headers=headers)
fw_rules.close()


fw_rules = open(filename, 'w')
for desc, port in ports_list.items():
    #print(desc + ': ' + port['port'] + ' - ' + port['protocol'])
    data_create = {
        'FIREWALLGROUPID': firewall_groupid,
        'direction': 'in',
        'ip_type': 'v4',
        'protocol':  port['protocol'],
        'subnet': ip,
        'subnet_size': '32',
        'port': port['port'],
        'notes': 'auto ' + desc + ' rule'
    }

    r = requests.post(vultr_create, data=data_create, headers=headers)
    if '412' not in str(r):
        result = json.loads(r.content)
        print("Rule for " + desc + " created. Rule number: " + str(result['rulenumber']))
        fw_rules.write(str(result['rulenumber']) + "\n")
    else:
        print(r.content)

fw_rules.close()
