"""This module implements dinning philosophers problem.
 Left-Rightly solution is implemented.
 """

__author__ = "Paljko Urbanek, Tomáš Vavro"
__email__ = "xurbanek@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print
from time import sleep

NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 10  # number of repetitions of think-eat cycle of philosophers


class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]


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