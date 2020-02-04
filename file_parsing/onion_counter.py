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
        with open("initial_counts.txt", 'a+') as output:
            for line in f:
                (site, onion) = line.split()
                file_onions.setdefault(onion, []).append(site)
            for k,v in file_onions.items():
                output.write("{} , {}\n".format(k, len(v)))

# Mid-Counter
def mid_onions(filename):
    init_mid_onions = []
    domains = []
    mid_onions = {}
    with open(filename, 'r') as f:
        with open("mid_counts.txt", 'a+') as output:
            for line in f:
                (onion, num) = line.replace(" ", "").split(',')
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
                output.write("{} , {}\n".format(k, v))

# Final Counter
def final_onions(filename):
    sorted_onions = []
    with open(filename, 'r') as f:
        unsorted_onions = [line.replace(" ", "") for line in f]
        with open("final_counts.txt", 'a+') as output:
            mid_onions = [u.rstrip().split(',') for u in unsorted_onions]
            sorted_onions = sorted(mid_onions, key=lambda x: int(x[1]), reverse=True)
            for x in sorted_onions:
                output.write("{} , {}\n".format(x[0], x[1]))

# Create the search file
def compile_onions():
    sorted_onions = []
    with open('final_counts.txt', 'r') as f:
        with open("onions.txt", 'a+') as output:
            for line in f:
                (onion, num) = line.replace(" ", "").split(',')
                output.write("{}\n".format(onion))

if __name__ == "__main__":
    files = glob("*.txt")
    processors = os_processes()
    print("Now counting onions........")
    pool = Pool(processors)
    pool.map(init_onions, files)
    pool.close()
    mid_onions('initial_counts.txt')
    final_onions('mid_counts.txt')
    compile_onions()