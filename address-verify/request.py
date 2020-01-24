import requests

# https://www.guru99.com/reading-and-writing-files-in-python.html
outie = open('output.txt', 'w+')
innie = open('input.txt', 'r')

# https://requests.readthedocs.io/en/master/user/quickstart/
for line in innie:
    try:
        site = line.rstrip('\n')
        r = requests.get(site, allow_redirects=True, timeout=10)
        # Legacy:
        #rText = str(r.text)
        rStatus = str(r.status_code)
        outie.write(site+": "+rStatus+"\n")

    except Exception as e:
        print(str(e))
        site = line.rstrip('\n')
        rStatus = "404"
        outie.write(site+": "+rStatus+"\n")

innie.close()
outie.close()
