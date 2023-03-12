# Urbanek_104620_feippds assignment 03
## Dinning philosophers problem

We have implemented multiple solutions for dinning philosophers problem such as waiter, left-rightly and token solution.
We have described the code of each one of them and at the end we compared each solution.


### Waiter Solution
Firstly we have imported all necessary data structures that we will be using later in the code.
```python
from fei.ppds import Thread, Mutex, print
from time import sleep
```

We have declared global variables such as:
* number of philosophers
* number of repetitions of think-eat cycle of philosophers
```python
NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 10 
```

We created Shared class and implemented all forks as Mutex() that will be "between" philosophers.
And regarding this solution we have created shared waiter that is also Mutex().
```python
class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]
        self.waiter = Mutex()
```

think() function is a stimulation of thinking process.
```python
def think(i: int):
    """Simulate thinking.
    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(0.1)
    print(f"Philosopher {i} finished thinking!")
    sleep(0.1)
```

eat() function is a stimulation of eating process.
```python
def eat(i: int):
    """Simulate eating.
    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is eating!")
    sleep(0.1)
    print(f"Philosopher {i} finished eating!")
    sleep(0.1)
```

The main philosophy of this solution(pun intended :D). We do it in the cycle of range NUM_RUNS.
Firstly we call the function for stimulating the thinking process. Then we lock the waiter who ensures that only one philosopher at the time
eats. Then the philosopher lock the right and left fork we call the stimulating process for eating philosopher unlock the forks
and waiter is then free to serve other philosopher.
Because of the waiter if more than 1 philosopher tries to eat at the same time. First philosopher that locks the waiter eats first and rest of the
philosophers wait for waiter to "serve" them.
```python
def philosopher(i: int, shared: Shared):
    """Run philosopher's code.
    Args:
        i -- philosopher's id
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        think(i)
        # get forks
        shared.waiter.lock()
        shared.forks[i].lock()
        shared.forks[(i+1) % NUM_PHILOSOPHERS].lock()
        eat(i)
        shared.forks[i].unlock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
        shared.waiter.unlock()
```

Last part is the principal of the parallel processing. Where we are defining threads and joining them in the end.
```python
def main():
    """Run main."""
    shared: Shared = Shared()
    philosophers: list[Thread] = [
        Thread(philosopher, i, shared) for i in range(NUM_PHILOSOPHERS)
    ]
    for p in philosophers:
        p.join()


if __name__ == "__main__":
    main()
```

* Because mostly of the code is the same in each solution I will describe only the part that is different.
### Lefty-Rightly Solution

Because we are implementing the left-right solution we don't need the waiter so we have changed the implementation according to it.
```python
class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]
```

The main difference is that we don't have waiter that allows the philosopher to take the forks and that he can eat.
We verified forks by index of philosophers and so we have make philosophers left-handed and right-handed. Every even philosopher
will pick up the right fork first and every odd philosopher will pick up the left fork first.
```python
def philosopher(i: int, shared: Shared):
    """Run philosopher's code.
    Args:
        i -- philosopher's id
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        think(i)
        # philosopher pick the right fork first
        if i % 2 ==0:
            shared.forks[i].lock()
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
        # philosopher pick the left fork first
        else:
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
            shared.forks[i].lock()

        # get forks
        eat(i)
        if i % 2 == 0:
            shared.forks[i].unlock()
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
        else:
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
            shared.forks[i].unlock()
```
### Token Solution

Last solution we have implemented tokens in the range of number of philosophers. So each philosopher have token.
We locked the first token to ensure the correct number of available tokens for philosophers. 
```python
class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]
        self.tokens = [Mutex() for _ in range(NUM_PHILOSOPHERS)]
        # first token
        self.tokens[0].lock()
```

Firstly we have implemented solution without to ask if philosopher is right-handed or left-handed. But we have got deadlock
because there was a case that two adjacent philosophers locked themselves. So we have implemented the right-left solution because
each eating philosopher needs two tokens for each fork to be able to eat.
```python
def philosopher(i: int, shared: Shared):
    """Run philosopher's code.
    Args:
        i -- philosopher's id
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        think(i)
        # lock token for current philosopher
        # right
        if i % 2 == 0:
            shared.tokens[i].lock()
            shared.tokens[(i + 1) % NUM_PHILOSOPHERS].lock()
        # left
        else:
            shared.tokens[(i + 1) % NUM_PHILOSOPHERS].lock()
            shared.tokens[i].lock()
        # get forks
        shared.forks[i].lock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
        eat(i)
        shared.forks[i].unlock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
        # pass the token
        shared.tokens[i].unlock()
        shared.tokens[(i + 1) % NUM_PHILOSOPHERS].unlock()

```

* At last, I will answer the request from the presentation and compare the implemented solutions with waiter solution.
  - The first solution is waiter solution that has one "person"(waiter) as the control unit. This ensures that only
  one philosopher at the time can eat. 
  - The second solution is left-rightly solution that separated the philosophers to even and odd based on their number.
  This solution ensures that under zero circumstances can't adjacent philosophers can pick forks at the same time. Prevents
  deadlock.
  - The third solution is token solution. This solution is giving to philosophers tokens on which circumstances they can pick up
  the forks if they have certain number of tokens. Prevents deadlock because solution ensures that adjacent philosophers can't
  pick forks at the same time.

### Summary
Based on what we learned we can say that token solution is the only solution where philosophers manage their own allocations.
So solution is more flexible. But because of that left-rightly and token solution is more complex to implement than waiter
that uses one authority to manage allocations. 

Recourses:
* https://pages.mtu.edu/~shene/NSF-3/e-Book/MUTEX/TM-example-left-right.html#:~:text=If%20philosopher%20P%20has%20his,will%20put%20down%20both%20chopsticks.
* https://www.ecb.torontomu.ca/~courses/coe518/Labs/lab4/lisi.edu-dining-Philosopherecture8.pdf
* https://en.wikipedia.org/wiki/Dining_philosophers_problem
* https://github.com/tj314/ppds-2023-cvicenia/tree/master/seminar4