# parallel-processing-template

A template for parallel processing and thread pooling in Python.

## To Use

The script can be executed from a terminal in the following ways:

* __baseline__ Runs the script without parallel processing or thread pooling to return a baseline execution speed. This is fastest on very small datasets.

    `python workers.py baseline`

* __parallel__ Runs the script asyncronously using parallel processing. It's suggested to specify the number of workers. This is fastest on very large datasets.

    `python workers.py parallel <workers:int>`

* __thread__ Runs the script sequentially using thread pooling. It's suggested to specify the number of workers. This is fastest on medium sized datasets.

    `python workers.py thread <workers:int>`

## Implementing Your Own Methods

To adapt this template to your own methods, you will need to update the iterables and the work method. See `example.py`

**iterables**

``` python
if __name__=='__main__':
    sampleDatasetSize = 1000000
    iterables = [randint(0, 1000) for x in range(0, sampleDatasetSize)] # <-- change this to whatever you want to process
```

**work method**

``` python
def work(iterables):
    for iterable in iterables:
        """do something""" # <-- your code here
```

The Workers class can also be imported and initialized with methods other than work. Following the Workers class docstring, it can use any method that takes one list argument:

``` python
class Workers:
    """Intializes a class of workers for parallel processing or thread pooling \n
    Keyword Arguments:
        func: method -- any method that takes a list as it's single argument
        iterables: list -- a list of arguments to be mapped to func
        asyncronous: Boolean -- when True runs the operation in parallel; when False runs the operation in thread pool
    """
    def __init__(self, func, iterables, asyncronous=True):
        ...
```

## Speed Testing

To test the speed and determine the best processing operation, update the sampleDatasetSize to determine the speed:

``` python
if __name__=='__main__':
    sampleDatasetSize = 5000000
```

Baseline will be fastest will small sample dataset sizes around 100,000. Thread pooling will be fastest with medium sample dataset sizes around 2,000,000. Parallel processing will be fastest with datasets even larger datasets.

Changing the number of workers can dramatically change processing times. It's suggested to experiment to determine the optimal number of workers for the task. The default is the number of CPUs on your computer. For parallel processing, optimal speeds are found increasing the number of workers commensurate with the dataset size. Each worker takes resources to spawn, so too many workers will decrease processing speeds.

Experiment!

``` cmd
python workers.py baseline
python workers.py thread
python workers.py parallel

python workers.py thread 8
python workers.py parallel 8

python workers.py thread 20
python workers.py parallel 20

python workers.py thread 50
python workers.py parallel 50

python workers.py thread 80
python workers.py parallel 80
```
