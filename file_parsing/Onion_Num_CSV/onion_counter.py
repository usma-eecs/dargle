import csv # Output and input format
from urllib.parse import urlparse # Find domain
from glob import glob # To find all files in specified directory
from multiprocessing import Pool, cpu_count # To utilize multiple processors to speed up the script
from subprocess import Popen, PIPE # Make the script universal
from sys import platform # Determine system

# Parse out domains onions were found on
domain_regex = r'[a-zA-Z0-9][a-zA-Z0-9-]{1,}[a-zA-Z0-9](\.[a-zA-Z]{2,})+'

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
def init_onions(filename):
    file_onions = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f, quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True)
        next(reader)
        with open("initial_counts.csv", 'a+', newline='') as output:
            writer = csv.writer(output)
            for line in reader:
                site = line[0]
                onion_url = line[1]
                onion = urlparse("http://"+onion_url).netloc
                file_onions.setdefault(onion, []).append(site)
            for k,v in file_onions.items():
                writer.writerow([k, len(v)])

# Mid-Counter
def mid_onions(filename):
    init_mid_onions = []
    domains = []
    mid_onions = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        with open("mid_counts.csv", 'a+', newline='') as output:
            writer = csv.writer(output)
            for line in reader:
                onion = line[0]
                num = line[1]
                if onion not in domains:
                    domains.append(onion)
                init_mid_onions.append([onion, num])
            for d in domains:
                count = 0
                for p in init_mid_onions:
                    if d == p[0]:
                        count += int(p[1].rstrip())
                    else:
                        continue
                mid_onions[d] = count
            for k,v in mid_onions.items():
                writer.writerow([k,v])

# Final Counter
def final_onions(filename):
    sorted_onions = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        sorted_onions = sorted(reader, key=lambda x: int(x[1]), reverse=True)
        with open("final_counts.csv", 'a+', newline='') as output:
            writer = csv.writer(output)
            # writer.writerow(["Onion", "Frequency"])
            for x in sorted_onions:
                writer.writerow([x[0], x[1]])


# Create the search file
def compile_onions():
    sorted_onions = []
    with open('final_counts.csv', 'r') as f:
        with open("onions.csv", 'a+') as output:
            for line in f:
                onion = line.split(',')[0]
                output.write("{}\n".format(onion))

if __name__ == "__main__":
    files = glob("*.csv")
    processors = os_processes()
    print("Initial Onion Count........")
    pool = Pool(processors)
    pool.map(init_onions, files)
    pool.close()
    print("Mid Onion Count........")
    mid_onions('initial_counts.csv')
    print("Final Onion Count........")
    final_onions('mid_counts.csv')
    print("Compiling Onions........")
    compile_onions()