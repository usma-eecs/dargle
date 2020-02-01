from glob import glob # To find all files in specified directory
from multiprocessing import Pool, cpu_count # To utilize multiple processors to speed up the script
from subprocess import Popen, PIPE # Make the script universal
from sys import platform # Determine system
from operator import itemgetter # Retrieves the number out of the list to sort

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

# Counter
def count_onions(filename):
    file_onions = {}
    with open(filename, 'r') as f:
        with open("onion_counts.txt", 'a+') as output:
            for line in f:
                (site, onion) = line.split()
                file_onions.setdefault(onion, []).append(site)
            for k,v in file_onions.items():
                output.write("{} | {}\n".format(k, len(v)))

# Counter
def sort_onions(filename):
    unsorted_onions = []
    sorted_onions = []
    with open(filename, 'r') as f:
        for line in f:
            unsorted_onions.append(line)
        with open("sorted_onion_counts.txt", 'a+') as output:
            for u in unsorted_onions:
                sorted_onions.append(u.split('|'))
            sorted_onions = sorted(sorted_onions, key=itemgetter(1), reverse=True)
            for x in sorted_onions:
                output.write("{} | {}".format(x[0], x[1]))

if __name__ == "__main__":
    files = glob("*.txt")
    processors = os_processes()
    print("Now counting onions........")
    pool = Pool(processors)
    pool.map(count_onions, files)
    pool.close()
    sort_onions('onion_counts.txt')
