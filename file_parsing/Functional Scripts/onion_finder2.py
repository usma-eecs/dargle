import re # Regular expression library
import gzip
from io import BufferedReader
import csv
from glob import glob # To find all files in specified directory
from multiprocessing import Pool, cpu_count # To utilize multiple processors to speed up the script
from subprocess import Popen, PIPE # Make the script universal
from sys import platform # Determine system
from os.path import splitext # Used in tracking
from time import time

# Regex for onions 
# onion_regex = r'(?:https?\:\/\/)?[a-zA-Z2-7]{16}\.onion?(?:\/([^/]*))?'
onion_regex = r'(?:[a-zA-Z2-7]{16}|[a-zA-Z2-7]{56})\.onion'
onion = re.compile(onion_regex, re.IGNORECASE)

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
    global onion
    global count
    gz = gzip.open(filename, 'rb')
    header = ''
    skip = 0
    for i in gz:
        if skip == 18:
            if i.decode("utf8") == "\r\n":
                break
            else:
                header += i.decode('utf8')
        else:
            skip += 1
    url = re.search(r'WARC-Target-URI: (.+)\r\n', header).group(1)
    f = BufferedReader(gz)
    for line in f:
        domain = re.search(onion, line.decode('utf8'))
        if domain:
            print(f'{domain.group(0)}  {url}')
    gz.close()

if __name__ == "__main__":
    start = time()
    files = glob("*.warc.wet.gz")
    processors = os_processes()
    print("Searching for onions.........")
    # for f in files:
        # find_onions(f)
    pool = Pool(processors)
    pool.map(find_onions, files)
    pool.close()
    end = time()
    print("Time Elapsed: ", end - start)
