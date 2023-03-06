"""
Program implements problem of solving the sleeping barber problem
It represents different sequences of using mutex
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__authors__ = "Paljko Urbanek, Marián Šebeňa, Tomáš Vavro"
__email__ = "xurbanek@stuba.sk, mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Mutex, Thread, Semaphore
from time import sleep
from random import randint
from fei.ppds import print


class Shared(object):

    def __init__(self):
        # initialized variables of class shared
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    print(f"CUSTOMER {i} is getting a haircut...")
    sleep(randint(1, 10))


def cut_hair():
    print("\nBARBER is cutting hair...\n")
    sleep(randint(1, 10))


def balk(i):
    print(f"Room is full. Customer {i} left...")


def growing_hair(i):
    print(f"CUSTOMER {i} is growing hair...")
    sleep(randint(1, 10))
    print(f"CUSTOMER {i} has grown hair.")


def customer(i, shared):

    while True:
        # customer tries to enter full rom
        while shared.waiting_room >= N:
            balk(i)
            sleep(randint(1,10))

        # room is not full customer enters the room
        if shared.waiting_room < N:
            print(f"CUSTOMER {i} is in the room.")
            shared.mutex.lock()
            shared.waiting_room += 1
            shared.mutex.unlock()

        # barber is available, customer gets haircut
        if shared.barber:
            shared.customer.signal()
            shared.barber.wait()
            get_haircut(i)
            shared.customer_done.wait()
            shared.barber_done.signal()
            print(f"CUSTOMER {i} left the room.")
            growing_hair(i)


def barber(shared):

    while True:
        # rendezvous 1. Customer is waiting for barber to cut his hair
        shared.customer.wait()
        shared.barber.signal()
        cut_hair()
        shared.mutex.lock()
        shared.waiting_room -= 1
        shared.mutex.unlock()
        # rendezvous 1. Barber finished the cut. Customer is free to leave
        shared.customer_done.signal()
        shared.barber_done.wait()


def main():
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


C: int = 5
N: int = 3

if __name__ == "__main__":
    main()
