import sys
import csv
import threading
import requests


innie = sys.argv[1]
outie = sys.argv[2]
thread_num = int(sys.argv[3])
header = sys.argv[4]

def line_count():
    with open(innie) as f:
        for i, l in enumerate(f):
            pass
    f.close()
    print(i+1)
    return i+1

def multi_thread():
    return 1

def process_links():
    # https://www.guru99.com/reading-and-writing-files-in-python.html
    infile = open(innie, 'r')
    outfile = open(outie, 'w+')

    # Read in CSV, skip header
    in_reader = csv.reader(infile,delimiter=',')
    if header == 'true':
        next(in_reader,None)

    # socks proxies
    session = requests.session()
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'

    # headers to throw off scent
    headers = {}
    headers['User-agent'] = "HotJava/1.1.2 FCS"

    # https://requests.readthedocs.io/en/master/user/quickstart/
    for row in in_reader:
        try:
            if (row[0][0:3] != 'http'):
                row[0] = 'http://' + row[0]

            site = row[0].rstrip('\n')
            
            # Test code
            #print(site+" is the site, L25\n")
            r = session.get(site, allow_redirects=True, timeout=10, headers=headers)
            # Legacy:
            #rText = str(r.text)
            
            # Test code
            # print(site+" is the site, L29\n")
            rStatus = str(r.status_code)
            outfile.write(site+","+rStatus+"\n\n")

        except Exception as e:
            #print(str(e))
            site = row[0].rstrip('\n')
            
            # Test code
            # print(site+" is the site, L36\n")
            rStatus = str(e.__class__.__name__)
            outfile.write(site+","+rStatus+"\n\n")

    infile.close()
    outfile.close()

process_links()
line_count()
