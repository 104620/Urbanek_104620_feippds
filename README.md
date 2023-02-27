# Urbanek_104620_feippds assignment 01
## Bakery Algorithm Implementation 

In this assignment we have implemented the lamport's bakery algorithm. It is algorithm discovered by Leslie Lamport.
He was a computer scientist, and he devoted most of his study to formal correctness of concurrent systems for improvement in safety
multiple threads processing. 


What is bakery algorithm?
- Bakery algorithm is algorithm  which is intended to improve the safety in the usage of shared resources among multiple threads by means of mutual exclusion. 

What it is good for?
- Bakery algorithm is good for providing solution for one process accessing the critical section at a time.
This ensures consistency of the performed processes. Also, this solution works for N processes that can
access critical section.

Firstly we have imported all necessary libraries.

```python

from fei.ppds import Thread
from time import sleep

```
Secondly we have declared our global variables.

```python

NUM_THREADS: int = 5
num: [] = [0] * NUM_THREADS
In: [] = [0] * NUM_THREADS

```
- Number of Threads as NUM_THREADS
- Array num[] - priority of process
- Array In[] - entering process


Third part is the main process where we have defined function that stimulates process.
Function have two arguments it's: tid and num_runs. You can see description in the picture.
We have declared atomic part for process count number. Then we have declared loop
that determines waiting position for threads. In the end we have executable critical section
and exit of the critical section.


```python
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

        # loop that determines waiting position of threads on behalf of two conditions
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
```

Last part is the principal of the parallel processing. Where we are defining threads and joining them in the end.


```python
if __name__ == '__main__':
    DEFAULT_NUM_RUNS = 10
    threads = [Thread(process, i, DEFAULT_NUM_RUNS) for i in range(NUM_THREADS)]
    [t.join() for t in threads]
```