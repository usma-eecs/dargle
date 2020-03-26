import re # Regular expression library
import warc # warc3-wet. To read common crawl files.
import csv # Output and input format
from glob import glob # To find all files in specified directory
from multiprocessing import Pool, cpu_count # To utilize multiple processors to speed up the script
from subprocess import Popen, PIPE # Make the script universal
from sys import platform # Determine system
from os.path import splitext # Used in tracking

# Regex for onions 
# onion_regex = r'([a-zA-Z2-7]{16}|[a-zA-Z2-7]{56})\.onion?(?:\/([^/ \\\s]*))?'
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

# Redefine findall
def findall(pattern, string):
    while True:
        match = re.search(pattern, string)
        if not match:
            break
        yield match.group(0)
        string = string[match.end():]

# Find onions in data
def find_onions(filename):
    global onion
    file_onions = {}
    with warc.open(filename) as f:
        with open("{}.csv".format(filename.strip(".warc.wet.gz")), 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(["Site", "Onion"])
            for record in f:
                url = str(record.header.get('WARC-Target-URI', None))
                data = str(record.payload.read())
                url_match = findall(onion, url)
                payload_match = findall(onion, data)
                if url_match:
                    onions = list(url_match)
                    for o in onions:
                        writer.writerow([url, o])
                if payload_match:
                    onions = list(payload_match)
                    for o in onions:
                        writer.writerow([url, o])

if __name__ == "__main__":
    files = glob("*.warc.wet.gz")
    completed = glob("*.csv")
    completed = [splitext(c)[0] for c in completed]
    if completed:
        files = [f for f in files if f.strip(".warc.wet.gz") not in completed]
    if len(files) == 0:
        print("All Common Crawl Files have been searched!")
    else:
        processors = os_processes()
        print("Searching for onions.........")
        pool = Pool(processors)
        pool.map(find_onions, files)
        pool.close()
