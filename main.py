"""This module implements dinning philosophers problem.
 Token solution is implemented.
 """

__author__ = "Paljko Urbanek, Marian Šebeňa, Tomáš Vavro"
__email__ = "xurbanek@stuba.sk, mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print, Semaphore
from time import sleep

D = 10
H = 5
K = 2


class Shared:
    """Represent shared data for all threads."""

    def __init__(self):
        """Initialize an instance of Shared."""
        self.mutex = Mutex()
        self.servings = H
        self.full_pot = Semaphore(H)
        self.empty_pot = Semaphore(0)
        self.pot_full = False

        self.barrier1 = Semaphore(0)
        self.barrier2 = Semaphore(0)
        self.num_ready = 0
        self.num_eating = 0


def get_serving_from_pot(savage_id: int, shared):
    shared.servings -= 1
    print(f"Savage {savage_id} took the portion.")
    sleep(0.1)


def put_servings_in_pot(chef_id: int, shared):
    shared.servings += 1
    print(f"Chef {chef_id} I am cooking")
    sleep(0.1)


def savage(savage_id: int, shared):
    while True:
        # calling the chef when pot is empty
        shared.full_pot.wait()

        # gathering the savages
        shared.mutex.lock()
        shared.num_ready += 1
        print(f"Savage {savage_id}: came to eat. We are [{shared.num_ready}/{H}]")
        if shared.num_ready == H:
            print(f"Savage {savage_id}: all of us came :D. We can start to eat.")
            shared.barrier1.signal(H)
        shared.mutex.unlock()
        shared.barrier1.wait()

        shared.mutex.lock()
        if shared.servings != 0:
            shared.num_eating += 1
            get_serving_from_pot(savage_id, shared)
            print(f"Savage {savage_id}: I am eating! Portions left [{shared.servings}/{H}]")
            shared.mutex.unlock()
        if shared.servings == 0:
            shared.num_ready = 0
            shared.num_eating = 0
            print(f"Savage {savage_id}: Pot is empty. I will call the chef.")
            shared.empty_pot.signal(H)

        # wait for all savages to finish eating
        shared.barrier2.wait()

        shared.mutex.lock()
        shared.num_eating -= 1
        if shared.num_eating == 0:
            shared.barrier2.signal(D)
        shared.mutex.unlock()


def chef(chef_id: int, shared):
    while True:
        shared.empty_pot.wait()
        shared.mutex.lock()
        put_servings_in_pot(chef_id, shared)
        print(f"Chef {chef_id} has cooked the portion. [{shared.servings}/{H}]")
        shared.mutex.unlock()
        if shared.servings == H:
            print("Chefs finished the cooking process. Savages can eat.")
            shared.full_pot.signal(H)


def main():
    """Run main."""
    shared: Shared = Shared()
    savages: list[Thread] = [
        Thread(savage, i, shared) for i in range(D)
    ]
    chefs: list[Thread] = [
        Thread(chef, i, shared) for i in range(K)
    ]
    for s in savages:
        s.join()

    for c in chefs:
        c.join()


if __name__ == "__main__":
    main()
