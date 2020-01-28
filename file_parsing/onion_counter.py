from glob import glob # To find all files in specified directory
from multiprocessing import Pool, cpu_count # To utilize multiple processors to speed up the script
from subprocess import Popen, PIPE # Make the script universal
from sys import platform # Determine system
from collections import Counter # Self-Explanatory

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
    with open(filename, 'r') as f:
        with open("onion_counts.txt", 'a+') as output:
            lines = [line.strip() for line in f]
            counts = Counter(lines)
            for k,v in counts.items():
                output.write("{} | {}\n".format(k, v))

if __name__ == "__main__":
    files = glob("*.txt")
    processors = os_processes()
    print("Now counting onions........")
    pool = Pool(processors)
    pool.map(count_onions, files)
    pool.close()
