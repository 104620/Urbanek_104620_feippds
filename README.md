# Urbanek_104620_feippds assignment 01
## Bakery Algorithm Implementation 

In this assignment we have implemented the lamport's bakery algorithm. It is algorithm discovered by Leslie Lamport.
He was a computer scientist, and he devoted most of his study to formal correctness of concurrent systems for improvement in safety
multiple threads processing.


Firstly we have imported all necessary libraries.

<img height="100" src="C:\Users\Palko\Desktop\Me\FAKULTET A INTERNAT\Ing\8. semester\8. semester Pako\PPDS\Zadania\01\Urbanek_104620_feippds\Import.png" width="300"/>


Secondly we have declared our global variables.
- Number of Threads as NUM_THREADS
- Array num[] - priority of process
- Array In[] - entering process


<img height="100" src="C:\Users\Palko\Desktop\Me\FAKULTET A INTERNAT\Ing\8. semester\8. semester Pako\PPDS\Zadania\01\Urbanek_104620_feippds\GlobalVar.png" width="300"/>


Third part is the main process where we have defined function that stimulates process.
Function have two arguments it's: tid and num_runs. You can see description in the picture.
We have declared atomic part for process count number. Then we have declared loop
that determines waiting position for threads. In the end we have executable critical section
and exit of the critical section.


<img height="500" src="C:\Users\Palko\Desktop\Me\FAKULTET A INTERNAT\Ing\8. semester\8. semester Pako\PPDS\Zadania\01\Urbanek_104620_feippds\Process.png" width="600"/>


Last part is the principal of the parallel processing. Where we are defining threads and joining them in the end.


<img height="100" src="C:\Users\Palko\Desktop\Me\FAKULTET A INTERNAT\Ing\8. semester\8. semester Pako\PPDS\Zadania\01\Urbanek_104620_feippds\Main.png" width="500"/>