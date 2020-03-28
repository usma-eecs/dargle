import sys
import csv
import threading
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# innie = sys.argv[1]
# outie = sys.argv[2]
# thread_num = int(sys.argv[3])
# header = sys.argv[4]

def line_count(innie):
    with open(innie) as f:
        for i, l in enumerate(f):
            pass
    f.close()
    print(i+1)
    return i+1

# TODO
def multi_thread():
    return 1

def process_links(innie,outie,header):
    # https://www.guru99.com/reading-and-writing-files-in-python.html
    infile = open(innie, 'r')
    outfile = open(outie, 'w+')

    # Read in CSV, skip header
    in_reader = csv.reader(infile,delimiter=',')
    out_writer = csv.writer(outfile)
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

    x = 0
    totallength = line_count(innie)

    # https://requests.readthedocs.io/en/master/user/quickstart/
    for row in in_reader:
        try:
            if (row[0][0:3] != 'http'):
                row[0] = 'http://' + row[0]

            site = row[0].rstrip('\n')
            hits = row[1]
            
            # Test code
            #print(site+" is the site, L25\n")
            r = session.get(site, allow_redirects=True, timeout=3, headers=headers)
            # Legacy:
            #rText = str(r.text)
            
            soup = BeautifulSoup(r.content,'html.parser')
            title = soup.title.string.encode("utf-8")

            # Test code
            # print(site+" is the site, L29\n")
            rStatus = str(r.status_code)
            timestamp = datetime.now()
            out_writer.writerow([site,rStatus,hits,timestamp.strftime("%m/%d/%Y %H:%M:%S"),title])

            print("Progress: {} out of {}".format(x,totallength))
            x+=1

        except Exception as e:
            #print(str(e))
            site = row[0].rstrip('\n')
            
            # Test code
            # print(site+" is the site, L36\n")
            rStatus = str(e.__class__.__name__)
            timestamp = datetime.now()
            out_writer.writerow([site,rStatus,hits,timestamp.strftime("%m/%d/%Y %H:%M:%S"),"N/A"])

            print("Progress: {} out of {}".format(x,totallength))
            x+=1

    infile.close()
    outfile.close()
    return outie

# process_links()
# line_count()
