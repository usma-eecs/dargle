import csv # Output and input format
import tldextract
from urllib.parse import urlparse # Find domain
from glob import glob # To find all files in specified directory
from multiprocessing import Pool, cpu_count # To utilize multiple processors to speed up the script
from subprocess import Popen, PIPE # Make the script universal
from sys import platform # Determine system
from collections import defaultdict

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

# Initial Counter
def init_sites(filename):
    file_onions = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f, quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True)
        next(reader)
        with open("initialized_site_data.csv", 'a+', newline='') as output:
            writer = csv.writer(output)
            for line in reader:
                url = line[0].lower()
                extracted = tldextract.extract(url)
                site = "{}.{}".format(extracted.domain, extracted.suffix)
                onion_url = line[1].lower()
                onion = urlparse("http://"+onion_url).netloc
                file_onions.setdefault(site, []).append(onion)
            for k,v in file_onions.items():
                writer.writerow([k, v,])#''.join(list(set(v)))])

# Mid-Counter
def mid_sites(filename):
    mid_sites = defaultdict(set)
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        with open("initial_site_counts.csv", 'a+', newline='') as output:
            writer = csv.writer(output)
            for line in reader:
                site = line[0]
                onion = line[1]
                mid_sites[site].add(onion)
            for k,v in mid_sites.items():
                writer.writerow([k,len(v)])

# Final Counter
def final_sites(filename):
    sorted_sites = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        sorted_sites = sorted(reader, key=lambda x: int(x[1]), reverse=True)
        with open("final_sites_counts.csv", 'a+', newline='') as output:
            writer = csv.writer(output)
            for x in sorted_sites:
                writer.writerow([x[0], x[1]])

if __name__ == "__main__":
    files = glob("*.csv")
    processors = os_processes()
    print("Initializing Sites........")
    pool = Pool(processors)
    pool.map(init_sites, files)
    pool.close()
    print("Initial Site Count........")
    mid_sites('initialized_site_data.csv')
    print("Final Site Count........")
    final_sites('initial_site_counts.csv')
