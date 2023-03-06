# Urbanek_104620_feippds assignment 02
## Sleeping barber problem implementation

In this assignment we have implemented the sleeping barber problem in python.
This implementation helped us learn more about synchronization problem and problem-solving
with multiple threads. We have learned how to work with mutex, semaphore and we got
better understanding on how to work with multiple threads.

What is sleeping barker problem?

It is a classic synchronization problem with barber shop. This barber shop consists with
waiting room of size N and a barber chair. When a customer arrives there is control of 
integrity if room is full and if barber is free. If a barber is free(sleeping) customer can
wake him and barber can start to cut customer hair. This process is looped. 

```python
from fei.ppds import Mutex, Thread, Semaphore
from time import sleep
from random import randint
from fei.ppds import print
```

```python
class Shared(object):

    def __init__(self):
        # initialized variables of class shared
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)
```

```python
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
```

```python
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
```

```python
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
```

```python
C: int = 5
N: int = 3
```

```python
def main():
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()

if __name__ == "__main__":
    main()
```