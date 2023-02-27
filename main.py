"""This module contains an implementation of bakery algorithm.

Bakery algorithm  ensures that processes execute a critical section of code one at a time. A process trying to
execute that code chooses a number it believes to be higher than the numbers chosen by other such processes..
"""

__author__ = "Paljko Urbanek"
__email__ = "xurbanek@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread
from time import sleep

NUM_THREADS: int = 5
num: [] = [0] * NUM_THREADS
In: [] = [0] * NUM_THREADS
"""Global variables.
    NUM_THREADS     -- number of entered threads
    num             -- array of numbers of processes "priority" length of NUM_THREADS
    In              -- array of boolean values of processes who wants to enter critical section
"""


def process(tid: int, num_runs: int):
    """Simulates a process.
    Arguments:
        tid      -- thread id
        num_runs -- number of executions of the critical section
    """
    global num, In

    for _ in range(num_runs):
        i: int = tid
        # process wants to enter critical section
        In[i] = 1
        # atomic part
        num[i] = 1 + max(num)
        In[i] = 0

        # wait for other processes to finish their execution of critical section
        for j in range(NUM_THREADS):
            while In[i] == 1:
                continue
            while num[i] != 0 and (num[j], j) < (num[i], i):
                continue
        # execute critical section
        print(f"Process {tid} runs a complicated computation!")
        sleep(1)

        # exit critical section
        num[i] = 0


if __name__ == '__main__':
    DEFAULT_NUM_RUNS = 10
    threads = [Thread(process, i, DEFAULT_NUM_RUNS) for i in range(NUM_THREADS)]
    [t.join() for t in threads]
