import re
import warc # warc3-wet
from glob import glob
from time import time
from multiprocessing import Pool, cpu_count
from subprocess import Popen, PIPE
from sys import platform
from collections import Counter

# Regex for onion domain. Must be able to find with and without www, http://, and https://
# onion_regex = r'(?:https?://)?(?:www)?(\S*?\.onion)'
onion_regex = r'(?:https?\:\/\/)?[\w\-\.]+\.onion'

# Determine OS and number of processes to use
def os_processes():
    MAX_PROCESSES = 0
    if platform == "linux" or platform == "linux2":
        # linux
        bashCommand = "nproc"
        process = Popen(bashCommand.split(), stdout=PIPE)
        output, error = process.communicate()
        MAX_PROCESSES = int(output.decode().strip())
    elif platform == "darwin":
        # OS X
        bashCommand = "nproc"
        process = Popen(bashCommand.split(), stdout=PIPE)
        output, error = process.communicate()
        MAX_PROCESSES = int(output.decode().strip())
    elif platform == "win32":
        # Windows
        MAX_PROCESSES = cpu_count()
    return MAX_PROCESSES


# Find onions in data
def find_onions(filename):
    onion = re.compile(onion_regex, re.IGNORECASE)
    with warc.open(filename) as f:
        with open("onions.txt", 'a') as output:
            for record in f:
                url = str(record.header.get('WARC-Target-URI', None))
                match = onion.search(url)
                if match:
                    print(match.group(0))
                    output.write(match.group(0))
                # if re.match(onion_regex, url, re.IGNORECASE):
                    # print(url)

if __name__ == "__main__":
    files = glob("*.warc.wet.gz")
    processors = os_processes()
    start = time()
    pool = Pool(processors)
    pool.map(find_onions, files)
    pool.close()
    end = time()
    print("Time Elapsed: ", end - start)
