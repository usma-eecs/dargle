import re
import warc # warc3-wet
# import pyspark
import glob
import time
import multiprocessing

# Regex for onion domain. Must be able to find with and without www, http://, and https://
# onion_regex = r'(?:https?://)?(?:www)?(\S*?\.onion)'
onion_regex = r'(?:https?\:\/\/)?[\w\-\.]+\.onion'

# Find onions in data
def find_onions(filename):
    onion = re.compile(onion_regex, re.IGNORECASE)
    with warc.open(filename) as f:
        for record in f:
            url = str(record.header.get('WARC-Target-URI', None))
            match = onion.search(url)
            if match:
                print(match.group(0))
            # if re.match(onion_regex, url, re.IGNORECASE):
                # print(url)
                
if __name__ == "__main__":
    files = glob.glob("*.warc.wet.gz")
    start = time.time()
    pool = multiprocessing.Pool()
    pool.map(find_onions, files)
    pool.close()
    end = time.time()
    print("Time Elapsed: ", end - start)
