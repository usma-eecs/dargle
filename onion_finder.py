import re # Regular expression library
import warc # warc3-wet. To read common crawl files.
from glob import glob # To find all files in specified directory
from time import time # Self-Explanatory
from multiprocessing import Pool, cpu_count # To utilize multiple processors to speed up the script
from subprocess import Popen, PIPE # Make the script universal
from sys import platform # Determine system
from collections import Counter # Self-Explanatory

# Regex for onion domain. Must be able to find with and without www, http://, and https://
# onion_regex = r'(?:https?\:\/\/)?[\w\-\.]+\.onion'
onion_domain_regex = r'(?:https?\:\/\/)?[a-zA-Z2-7]{16}\.onion'#(?:\/([^/]*))?$'

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

# Tracker
def track_onions():
    pass

# Counter
def count_domains(filename):
    with open(filename, 'r') as f:
        with open("domain_counts.txt", 'w') as output:
            lines = [line.strip() for line in f]
            domain_counts = Counter(lines)
            for k,v in  domain_counts.items():
                output.write( "{} {}\n".format(k,v) )

# Find onions in data
def find_onions(filename):
    onion = re.compile(onion_domain_regex, re.IGNORECASE)
    with warc.open(filename) as f:
        with open("onion_domains.txt", 'a+') as output:
            for record in f:
                url = str(record.header.get('WARC-Target-URI', None))
                match = onion.search(url)
                if match:
                    domain = match.group(0)
                    print(domain, file=output)
                    # output.write(domain + '\n')

if __name__ == "__main__":
    files = glob("*.warc.wet.gz")
    processors = os_processes()
    print("Searching for onions.........")
    # start = time()
    pool = Pool(processors)
    pool.map(find_onions, files)
    pool.close()
    # end = time()
    # print("Time Elapsed: ", end - start)
    print("Now counting domains........")
    count_domains("onion_domains.txt")
