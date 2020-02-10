import sys
import requests

# https://www.guru99.com/reading-and-writing-files-in-python.html
innie = open(sys.argv[1], 'r')
outie = open(sys.argv[2], 'w+')

# socks proxies
session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

# headers to throw off scent
headers = {}
headers['User-agent'] = "HotJava/1.1.2 FCS"

# https://requests.readthedocs.io/en/master/user/quickstart/
for line in innie:
    try:
        if (line[0:3] != 'http'):
            line = 'http://' + line

        site = line.rstrip('\n')
        print(site+" is the site, L25\n")
        r = session.get(site, allow_redirects=True, timeout=120, headers=headers)
        # Legacy:
        #rText = str(r.text)
        print(site+" is the site, L29\n")
        rStatus = str(r.status_code)
        outie.write(site+": "+rStatus+"\n\n")

    except Exception as e:
        #print(str(e))
        site = line.rstrip('\n')
        print(site+" is the site, L36\n")
        rStatus = str(e.__class__.__name__)
        outie.write(site+": "+rStatus+"\n\n")

innie.close()
outie.close()
