# Urbanek_104620_feippds assignment 04
## Dinning savages with 2 chefs problem

We have implemented solution for dinning savages problem with two cooking chefs. 
This implementation is working as follows. We have D numbers of savages that wants to eat
from the pot that is size of H. Also we have K number of cooks that fill up the pot when it is empty.
H number of savages approach the pot they eat. When pot is empty last that have eaten call the chefs. 
Chefs fill the pot and the other savages can come. Process is looped. 
###
Further, in documentation we have described more detailed the problem, implementation, 
necessary variables for understanding the implementation, the code, and we showed the program output.


### Solution
Firstly we have imported all necessary data structures that we will be using later in the code.
```python
from fei.ppds import Thread, Mutex, print, Semaphore
from time import sleep

```

We have declared global variables.
```python
D = 10 
H = 5
K = 2 
```
- D - number of savages  
- H - max number of portions stored in pot
- K - number of chefs 

###
Then we have shared class where we defined all necessary
variables such as barriers, mutex, servings for monitoring
the pot, number of ready savages and number of eating savages.
```python
class Shared:
    """Represent shared data for all threads."""

    def __init__(self):
        """Initialize an instance of Shared."""
        self.mutex = Mutex()
        self.servings = H
        self.full_pot = Semaphore(H)
        self.empty_pot = Semaphore(0)

        self.barrier1 = Semaphore(0)
        self.barrier2 = Semaphore(0)
        self.num_ready = 0
        self.num_eating = 0
```


We have created obligatory functions for stimulation cooking process
where we also decrement and increment. We have added the sleep(0.1) just to be
stimulation more real.

###
###
We used this for getting the portion from the pot so the savage can eat.
```python
def get_serving_from_pot(savage_id: int, shared):
    """Stimulate getting portion from the pot.
    Args:
        savage_id -- savage's id
        shared -- class instance of shared variable
    """
    shared.servings -= 1
    print(f"Savage {savage_id} took the portion.")
    sleep(0.1)
```

We used this in the chef() function where chef in the cooking process
is putting new portion to the pot. 
```python
def put_servings_in_pot(chef_id: int, shared):
    """Stimulate cooking process when chef put portion to the pot.
    Args:
        chef_id -- chef's id
        shared -- class instance of shared variable
    """
    shared.servings += 1
    print(f"Chef {chef_id} I am cooking")
    sleep(0.1)
```

###
In this part of implementation we have created savage() function that controls savage threads.
We implemented multiple synchronization models that we will describe it further in the documentation.
```python
def savage(savage_id: int, shared):
    """Run savage's code.
    Args:
        savage_id -- savage's id
        shared -- class instance of shared variable
    """
    while True:
        # waiting for the full pot
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

        # gathering savages for eating process
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
        shared.mutex.lock()
        shared.num_eating -= 1
        if shared.num_eating == 0:
            shared.barrier2.signal(D)
        shared.mutex.unlock()
        shared.barrier2.wait()

```

Fist synchronization model looks like this. 
```python
# gathering the savages
        shared.mutex.lock()
        shared.num_ready += 1
        print(f"Savage {savage_id}: came to eat. We are [{shared.num_ready}/{H}]")
        if shared.num_ready == H:
            print(f"Savage {savage_id}: all of us came :D. We can start to eat.")
            shared.barrier1.signal(H)
        shared.mutex.unlock()
        shared.barrier1.wait()
```
This part of synchronization model is ensuring that all savages all gathered before
they proceed to eating process. We used mutex for incrementing the number of ready savages
and then there is statement if already number isn't equal the defined number of portions. When it is
,we signal that they can proceed the number of portion times further to the eating process else wait for others.

Output looks like this:
```text
Savage 0: came to eat. We are [1/5]
Savage 1: came to eat. We are [2/5]
Savage 2: came to eat. We are [3/5]
Savage 3: came to eat. We are [4/5]
Savage 4: came to eat. We are [5/5]
Savage 4: all of us came :D. We can start to eat.
```

Second synchronization model looks like this.
```python
# gathering savages for eating process
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
```

This part of synchronization model ensures that all the savages that came can eat.
We used mutex to increment the number of the savages that are eating. If there is no portions left
all savages have ate and the last savage that have ate is signaling the H number of times to the chef that pot is empty and 
cooking process can be proceeded.

The output looks like this:
```text
Savage 4 took the portion.
Savage 4: I am eating! Portions left [4/5]
Savage 1 took the portion.
Savage 1: I am eating! Portions left [3/5]
Savage 0 took the portion.
Savage 0: I am eating! Portions left [2/5]
Savage 3 took the portion.
Savage 3: I am eating! Portions left [1/5]
Savage 2 took the portion.
Savage 2: I am eating! Portions left [0/5]
Savage 2: Pot is empty. I will call the chef.
```


The last part of synchronization model looks like this. 
```python
# wait for all savages to finish eating
        shared.mutex.lock()
        shared.num_eating -= 1
        if shared.num_eating == 0:
            shared.barrier2.signal(D)
        shared.mutex.unlock()
        shared.barrier2.wait()
```
In this part we created the second barrier that ensures that all savages
finish eating before any other would come. We used mutex for decrementing the
number of eating savages and when it is 0 it means that all savages have eaten their
meals, and we signal the barrier the D number of times that it can proceed further otherwise it will wait.

Output looks like this: 
```text
Chef 1 I am cooking
Chef 1 has cooked the portion. [1/5]
Chef 1 I am cooking
Chef 1 has cooked the portion. [2/5]
Chef 1 I am cooking
Chef 1 has cooked the portion. [3/5]
Chef 1 I am cooking
Chef 1 has cooked the portion. [4/5]
Chef 0 I am cooking
Chef 0 has cooked the portion. [5/5]
Chefs finished the cooking process. Savages can eat.
```
###
In this part we created the chef. Chef have 2 arguments described in the
code. The process is infinite loop where on the beginning he waits for the
signalization in the savage() function. That's the first synchronization model.
The second is the mutex which is synchronization tool which we used for incrementing the
pot size in the cooking process. Third is synchronization process that we used when chefs finished
the cooking process which is finished when the serving match the defined pot size.
The signal is called that pot is full and savages can begin the eating process.
```python
def chef(chef_id: int, shared):
    """Run chef's code.
    Args:
        chef_id -- chef's id
        shared -- class instance of shared variable
    """
    while True:
        shared.empty_pot.wait()
        shared.mutex.lock()
        put_servings_in_pot(chef_id, shared)
        print(f"Chef {chef_id} has cooked the portion. [{shared.servings}/{H}]")
        shared.mutex.unlock()
        if shared.servings == H:
            print("Chefs finished the cooking process. Savages can eat.")
            shared.full_pot.signal(H)
```

###
Last part is the principal of the parallel processing. Where we are defining threads and joining them in the end.
For the range of creating the threads for savages we have used global variable D
and for the range of creating the threads for chefs we have used variable K.
```python
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
```

###
At the end I would like just to describe the output in few words.
As we can see the program is giving us the output we have desired at the
beginning. First 5 savages come to eat to the pot. The last that came signalizes
that all of them came. The eating process starts. This process is not interrupted.
The last savage that ate last portion from the pot wakes up the chefs.
Chefs start the cooking process. This process is also not interrupted. Other 5 savages wait. 
When chefs finished the cooking process the last chef that cooked the last portion notify that he finished
another 5 savages can come to the pot. And this whole process is looped.

```text
Savage 0: came to eat. We are [1/5]
Savage 1: came to eat. We are [2/5]
Savage 2: came to eat. We are [3/5]
Savage 3: came to eat. We are [4/5]
Savage 4: came to eat. We are [5/5]
Savage 4: all of us came :D. We can start to eat.
Savage 4 took the portion.
Savage 4: I am eating! Portions left [4/5]
Savage 1 took the portion.
Savage 1: I am eating! Portions left [3/5]
Savage 0 took the portion.
Savage 0: I am eating! Portions left [2/5]
Savage 3 took the portion.
Savage 3: I am eating! Portions left [1/5]
Savage 2 took the portion.
Savage 2: I am eating! Portions left [0/5]
Savage 2: Pot is empty. I will call the chef.
Chef 1 I am cooking
Chef 1 has cooked the portion. [1/5]
Chef 1 I am cooking
Chef 1 has cooked the portion. [2/5]
Chef 1 I am cooking
Chef 1 has cooked the portion. [3/5]
Chef 1 I am cooking
Chef 1 has cooked the portion. [4/5]
Chef 0 I am cooking
Chef 0 has cooked the portion. [5/5]
Chefs finished the cooking process. Savages can eat.
Savage 3: came to eat. We are [1/5]
Savage 8: came to eat. We are [2/5]
Savage 1: came to eat. We are [3/5]
Savage 2: came to eat. We are [4/5]
Savage 4: came to eat. We are [5/5]
Savage 4: all of us came :D. We can start to eat.
Savage 4 took the portion.
Savage 4: I am eating! Portions left [4/5]
Savage 1 took the portion.
Savage 1: I am eating! Portions left [3/5]
Savage 3 took the portion.
Savage 3: I am eating! Portions left [2/5]
Savage 8 took the portion.
Savage 8: I am eating! Portions left [1/5]
Savage 2 took the portion.
Savage 2: I am eating! Portions left [0/5]
Savage 2: Pot is empty. I will call the chef.
Chef 0 I am cooking
Chef 0 has cooked the portion. [1/5]
Chef 0 I am cooking
Chef 0 has cooked the portion. [2/5]
Chef 0 I am cooking
Chef 0 has cooked the portion. [3/5]
Chef 0 I am cooking
Chef 0 has cooked the portion. [4/5]
Chef 1 I am cooking
Chef 1 has cooked the portion. [5/5]
Chefs finished the cooking process. Savages can eat.
Savage 1: came to eat. We are [1/5]
Savage 7: came to eat. We are [2/5]
Savage 9: came to eat. We are [3/5]
Savage 3: came to eat. We are [4/5]
Savage 5: came to eat. We are [5/5]
Savage 5: all of us came :D. We can start to eat.
Savage 5 took the portion.
Savage 5: I am eating! Portions left [4/5]
Savage 7 took the portion.
Savage 7: I am eating! Portions left [3/5]
Savage 1 took the portion.
Savage 1: I am eating! Portions left [2/5]
Savage 9 took the portion.
Savage 9: I am eating! Portions left [1/5]
Savage 3 took the portion.
Savage 3: I am eating! Portions left [0/5]
Savage 3: Pot is empty. I will call the chef.
...
```

Recourses:
* https://github.com/tj314/ppds-2023-cvicenia/blob/master/seminar3/bariera.py
* the pdf file that we got from teachers
* https://greenteapress.com/semaphores/LittleBookOfSemaphores.pdf
* https://chat.openai.com/
* https://stackoverflow.com/questions/70543411/dining-savages-problem-semaphores-and-mutexes