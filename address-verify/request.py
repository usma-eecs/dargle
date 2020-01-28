import requests

# https://www.guru99.com/reading-and-writing-files-in-python.html
outie = open('output.txt', 'w+')
innie = open('input.txt', 'r')

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
        site = line.rstrip('\n')
        r = session.get(site, allow_redirects=True, timeout=120, headers=headers)
        # Legacy:
        #rText = str(r.text)
        rStatus = str(r.status_code)
        outie.write(site+": "+rStatus+"\n\n")

    except Exception as e:
        print(str(e))
        site = line.rstrip('\n')
        rStatus = str(e)
        outie.write(site+": "+rStatus+"\n\n")

innie.close()
outie.close()
