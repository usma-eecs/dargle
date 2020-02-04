import re # Regular expression library
import warc # warc3-wet. To read common crawl files.
from glob import glob # To find all files in specified directory
from multiprocessing import Pool, cpu_count # To utilize multiple processors to speed up the script
from subprocess import Popen, PIPE # Make the script universal
from sys import platform # Determine system
from collections import Counter # Self-Explanatory
from os import path # Import path to use the exists function for tracking

# Regex for onion pages and domains. Must be able to find with and without www, http://, and https://
onion_page_regex = r'(?:https?\:\/\/)?[a-zA-Z2-7]{16}\.onion?(?:\/([^/]*))?$'
# onion_domain_regex = r'(?:https?\:\/\/)?[a-zA-Z2-7]{16}\.onion'

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
def tracker(filename):
    with open('finished.txt', 'a+') as f:
        print(filename, file=f)

# Counter
def count_domains(filename):
    with open(filename, 'r') as f:
        with open("onion_counts.txt", 'w') as output:
            lines = [line.strip() for line in f]
            domain_counts = Counter(lines)
            for k,v in  domain_counts.items():
                output.write("{} {}\n".format(k,v))

# Find onions in data
def find_onions(filename):
    # onion_domain = re.compile(onion_domain_regex, re.IGNORECASE)
    onion_page = re.compile(onion_page_regex, re.IGNORECASE)
    with warc.open(filename) as f:
        with open("onions.txt", 'a+') as output:
            for record in f:
                url = str(record.header.get('WARC-Target-URI', None))
                # domain_match = onion_domain.search(url)
                page_match = onion_page.search(url)
                # if domain_match:
                    # match = domain_match.group(0)
                    # print(match, file=output)
                if page_match:
                    match = page_match.group(0)
                    print(match, file=output)
    tracker(filename)

if __name__ == "__main__":
    files = glob("*.warc.wet.gz")
    if path.exists('finished.txt'):
        used = [line.rstrip('\n') for line in open('finished.txt')]
        files = [f for f in files if f not in used]
    processors = os_processes()
    print("Searching for onions.........")
    pool = Pool(processors)
    pool.map(find_onions, files)
    pool.close()
    print("Now counting domains........")
    count_domains("onions.txt")
