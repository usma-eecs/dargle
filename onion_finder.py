import re
import warc # warc3-wet
# import pyspark
import glob
import time
import threading

# Regex for onion domain. Must be able to find with and without www, http://, and https://
# onion_regex = r'(?:https?://)?(?:www)?(\S*?\.onion)'
onion_regex = r'(?:https?\:\/\/)?[\w\-\.]+\.onion'

# Find onions in data
def find_onions(filename):
    # wet_file = unzip(filename)
    onion = re.compile(onion_regex, re.IGNORECASE)
    with warc.open(filename) as f:
        for record in f:
            url = str(record.header.get('WARC-Target-URI', None))
            match = onion.search(url)
            if match:
                print(match.group(0))
            # if re.match(onion_regex, url, re.IGNORECASE):
                # print(url)

files = glob.glob("*.warc.wet.gz")
start = time.time()
while not files:

# for warcfile in glob.glob("*.warc.wet.gz"):
#     find_onions(warcfile)
end = time.time()
print("Time Elapsed: ", end - start)