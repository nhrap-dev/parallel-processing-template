import os
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import sys
from time import time
from random import randint


class Workers:
    """Intializes a class of workers for parallel processing or thread pooling \n
    Keyword Arguments:
        func: method -- any method that takes a list as it's single argument
        iterables: list -- a list of arguments to be mapped to func
        asyncronous: Boolean -- when True runs the operation in parallel; when False runs the operation in thread pool
    """
    def __init__(self, func, iterables, asyncronous=True):
        t0 = time()
        if len(sys.argv) >= 2:
            cpus = int(sys.argv[2])
        else:
            cpus = os.cpu_count()
        workloadInterval = round(len(iterables) / cpus)
        location = 0
        workloads = []
        if asyncronous:
            with Pool() as executor: # async - fastest on large datasets
                for idx in range(cpus):
                    if idx < cpus - 1:
                        workload = iterables[location:location + workloadInterval]
                        location += workloadInterval
                    else:
                        workload = iterables[location:]
                    workloads.append(workload)
                executor.map(func, workloads)
        else:
            with ThreadPoolExecutor() as executor: # sequential - fastest on small datasets
                for idx in range(cpus):
                    if idx < cpus - 1:
                        workload = iterables[location:location + workloadInterval]
                        location += workloadInterval
                    else:
                        workload = iterables[location:]
                    workloads.append(workload)
                executor.map(func, workloads)
        print('Total elapsed time: ' + str(time() - t0))


def work(iterables):
    """do something"""
    for iterable in iterables:
        try:
            sum(iterable)
        except:
            iterable + 1

def baseline(func, iterables):
    """Runs work without parallel processing or thread pooling to get a baseline execution speed"""
    t0 = time()
    func(iterables)
    print('Baseline time: ' + str(time() - t0))


if __name__=='__main__':
    sampleDatasetSize = 5000000
    iterables = [randint(0, 1000) for x in range(0, sampleDatasetSize)] # example with one argument
    # iterables = [(randint(0, 1000), randint(0, 1000)) for x in range(0, sampleDatasetSize)] # example with two arguments; use Pool.starmap
    if len(sys.argv) > 1 and sys.argv[1] == 'baseline':
        baseline(work, iterables)
    else:
        if sys.argv[1] == 'sync':
            Workers(work, iterables, asyncronous=False)
        elif sys.argv[1] == 'async':
            Workers(work, iterables, asyncronous=True)
        else:
            scriptname = os.path.basename(__file__)
            print("""
                ERROR: Unable to understand system argument.\n Try one of the following: \n  
                  python {s} sync <workers:int> \n  
                  python {s} async <workers:int> \n  
                  python {s} baseline
                """.format(s=scriptname))
