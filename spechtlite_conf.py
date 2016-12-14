#!/usr/bin/env python3
# coding=utf-8

import base64
import requests
import re
import io


def get_white_list():
    print('start to generate whitelist')
    whitelist_url = 'https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf'
    data = requests.get(whitelist_url)
    whitelist_path = './conf/whitelist'

    with open(whitelist_path, 'w') as f:
        for line in data.iter_lines():
            domain = re.findall(r'\w+\.\w+', line.decode('utf-8'))
            if len(domain) > 0:
                f.write('%s\n' % '\.'.join(domain[0].split('.')))
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
                    gfwlist_path.write('%s\n' % '\.'.join(domain[0].split('.')))
    print('gfwlist done!')

def get_ad_list():
    print('start to get rejectlist')
    rejectlist_url = 'https://raw.githubusercontent.com/BurpSuite/CloudGate-RuleList/master/Rule/REJECT'
    rejectlist_path = './conf/rejectlist'
    data = requests.get(rejectlist_url)
    
    with open(rejectlist_path, 'w') as f:
        for line in data.iter_lines():
            domain = line.split(',')[1]
            f.write('%s\n' % '\.'.join(domain.split('.')))
    print('rejectlist done!')

if __name__ == '__main__':
    #get_gfw_list()
    #get_white_list()
    get_ad_list()
