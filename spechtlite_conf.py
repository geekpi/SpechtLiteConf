#!/usr/bin/env python3
# coding=utf-8

import base64
import requests
import re
import io


def surge_to_specht(domain_type, domain_url):
    if domain_type == 'DOMAIN-KEYWORD':
        return '%s\n' % '\.'.join(domain_url.split('.'))
    elif domain_type == 'DOMAIN-SUFFIX':
        return '%s$\n' % '\.'.join(domain_url.split('.'))
    elif domain_type == 'DOMAIN':
        #todo
        return '%s$\n' % '\.'.join(domain_url.split('.'))
   

def get_white_list():
    print('start to generate whitelist')
    whitelist_url = 'https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf'
    data = requests.get(whitelist_url)
    whitelist_path = './conf/whitelist'

    with open(whitelist_path, 'w') as f:
        for line in data.iter_lines():
            domain = re.findall(r'\w+\.\w+', line.decode('utf-8'))
            if len(domain) > 0:
                f.write(surge_to_specht('DOMAIN-SUFFIX', domain[0]))
    print('whitelist done!')


def get_gfw_list():
    print('start to generate gfwlist')
    gfwlist_url = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
    gfwlist_path = './conf/gfwlist'

    comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    data = requests.get(gfwlist_url).text
    content = base64.b64decode(data)
    
    with open(gfwlist_path, 'w') as gfwlist_path:
        for line in io.StringIO(content.decode('utf-8')).readlines():
            if re.findall(comment_pattern, line):
                continue
            else:
                domain = re.findall(domain_pattern, line)
                if domain:
                    if line.startswith('||') or line.startswith('|'):
                        gfwlist_path.write(surge_to_specht('DOMAIN-SUFFIX', domain[0]))
                    else:
                        gfwlist_path.write(surge_to_specht('DOMAIN-KEYWORD', domain[0]))
    print('gfwlist done!')

def get_reject_list():
    print('start to get rejectlist')
    rejectlist_url = 'https://raw.githubusercontent.com/BurpSuite/CloudGate-RuleList/master/Rule/REJECT'
    rejectlist_path = './conf/rejectlist'
    data = requests.get(rejectlist_url)
    
    with open(rejectlist_path, 'w') as f:
        for line in data.iter_lines():
            domain = line.decode('utf-8').split(',')
            if len(domain) > 1:
                f.write(surge_to_specht(domain[0], domain[1]))
    print('rejectlist done!')

if __name__ == '__main__':
    get_gfw_list()
    get_white_list()
    get_reject_list()
