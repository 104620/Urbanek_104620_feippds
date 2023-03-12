"""This module implements dinning philosophers problem.
 Left-Rightly solution is implemented.
 """

__author__ = "Paljko Urbanek, Tomáš Vavro"
__email__ = "xurbanek@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Semaphore, Mutex, print
from time import sleep

NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 10  # number of repetitions of think-eat cycle of philosophers


class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]
        self.tokens = [Mutex() for _ in range(NUM_PHILOSOPHERS)]
        # first token
        self.tokens[0].lock()


def think(i: int):
    """Simulate thinking.
    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(0.1)
    print(f"Philosopher {i} finished thinking!")
    sleep(0.1)


def eat(i: int):
    """Simulate eating.
    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is eating!")
    sleep(0.1)
    print(f"Philosopher {i} finished eating!")
    sleep(0.1)


def philosopher(i: int, shared: Shared):
    """Run philosopher's code.
    Args:
        i -- philosopher's id
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        think(i)
        # lock token for current philosopher
        shared.tokens[i].lock()
        shared.tokens[(i + 1) % NUM_PHILOSOPHERS].lock()
        # get forks
        shared.forks[i].lock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
        eat(i)
        shared.forks[i].unlock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
        # pass the token
        shared.tokens[i].unlock()
        shared.tokens[(i + 1) % NUM_PHILOSOPHERS].unlock()


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