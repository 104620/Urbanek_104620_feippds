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


Firstly we have imported all necessary libraries
```python
from fei.ppds import Mutex, Thread, Semaphore
from time import sleep
from random import randint
from fei.ppds import print
```


Secondly we have initialized all necessary patterns and variables that we will use
in relations with barber and customer. We have initialized customer and barber on Semaphore(0) so 
we can signal() and wait() these relations.
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

Thirdly we have implemented auxiliary functions for stimulation's process such as:
- getting haircut
- cutting hair
- growing hair
- trying again if waiting_room is full

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

Fourthly we implemented customer function. 
Where arguments are:
- i (number of customer)
- shared (class of shared mutex's, customer, barber,capacity)

First while is controlling the customers if waiting_room is full. While loop
ensures that customer will not go in to the room and will try again after some period of time.
Second condition is allows customer to enter the room. With incrementing the capacity of waiting_room.
Third condition enables to customer based on barber's availability that he can attend the chair or not.
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

Fifthly we have implemented barber function.
Arguments:
- shared (class of shared mutex's, customer, barber,capacity)

We have two rendezvous where customer is waiting for the barber to cut his hair where we
also used stimulation of this process and then combined process of customer leaving the room
and decrementation of capacity of waiting_room. 
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

Initialized global variables:
- C = Number of customers
- N = Size of waiting_room
```python
C: int = 5
N: int = 3
```

Last part is the principal of the parallel processing. Where we are defining threads and joining them in the end.
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

*In all of these processes where we have used mutex. We used is as lock that another thread can't
attend same process. This time for incrementation and decrementation capacity of waiting_room.
*Implemented code you can test with proper represented such as IDLE running the main.
Also, the code is generating output that works on basic principles of this problem. 

Resources:
- https://github.com/tj314/ppds-2023-cvicenia/blob/master/seminar3/mutex.py
- https://github.com/tj314/ppds-2023-cvicenia/blob/master/seminar3/barberShop.py
- https://en.wikipedia.org/wiki/Sleeping_barber_problem
- https://github.com/bragisig/python-sleeping-barber
- https://greenteapress.com/wp/semaphores/