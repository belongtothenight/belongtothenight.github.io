# Multiprocessing to Parrallel and Speed Up

This guide will show you how to enable multiprocessing to speed up your Python program.

## Problem

You have a Python program that takes a long time to run and is performing CPU-bound (math, data processing, etc.), none I/O-bound (network, disk, etc.) tasks. You want to speed up the program by making it work in parallel.

## Background

Note:

1. Not all libraries support multiprocessing.
2. This guide assumes you are familiar with Python and have a basic understanding of CPU and memory usage.
3. Tasks that are CPU-bound can be sped up by this.
4. Tasks that are I/O-bound can be sped up by using threading.
5. Tasks are independent of each other. (next task does not depend on the previous task's result)

The idea of **multi-processing** is to use multiple CPU-cores (1 core per process) to run multiple independent tasks at the same time. This is different from **multi-threading**, which uses multiple threads (1 core multiple tasks) to share CPU resources when independent tasks take a lot of time waiting for external triggers (network request, GPIO input, time) by idling.

Each newly created processes will have its own memory space without sharing memory with the parent process. Therefore, data sharing between processes and the parent process is not as easy as sharing data between threads. Methods like spawning with input argument, and `multiprocessing.Queue` can be used.

A example of using **multiprocessing** to speed up network package (pcap) processing can be found [in my GitHub](https://github.com/belongtothenight/ACN_Code/blob/main/hw1_traffic_pcap_parser/execute.py).

## Solution

### Step 1: Make Sure to have Sufficent Resources

1. CPU: The more cores you have, the more tasks you can run in parallel.
    - If you are using Windows, you can check Task Manager to see how many cores you have.
    - If you are using Linux, you can use tools like `htop`, `top`, or `echo $(nproc)` to see how many cores you have.
    - If you want to check with Python code, you can use the following code:
        ```python
        import os
        print(os.cpu_count())
        ```
2. Memory: Make sure you have enough memory to run multiple tasks at the same time. You can approximate the memory usage by multiplying the memory usage of one task by the number of tasks you want to run in parallel.
    - If you are using Windows, you can check Task Manager to see how much memory you have.
    - If you are using Linux, you can use tools like `htop`, `top`, or `free -h` to see how much memory you have.

### Step 2: Use the `multiprocessing` Library

- Using `multiprocessing.Pool`:
    ```python title="code" linenums="1" hl_lines="12-13"
    --8<-- "docs/HOW_TO/code/mp_pool.py"
    ```
    ```bash title="code output"
    --8<-- "docs/HOW_TO/log/mp_pool_output.log"
    ```
    This method is useful when you have a list of tasks (more than CPU core count) to run in parallel. The `Pool` class will automatically launch processes when a core is available.
- Using `multiprocessing.Process`:
    ```python title="code" linenums="1" hl_lines="12-15"
    --8<-- "docs/HOW_TO/code/mp_process.py"
    ```
    ```bash title="code output"
    --8<-- "docs/HOW_TO/log/mp_process_output.log"
    ```
    This method is useful when you want to manually control the number of processes to run in parallel. After each process is created, you can call `process.start()` to start the process and `process.join()` to wait for the process to finish.

Note:

1. `if __name__ == '__main__':` in line `8` is required to prevent infinite recursion when creating new processes. This is because the new processes will import the main module again, and the `if __name__ == '__main__':` block will prevent the new processes from running the code inside the block.
2. `multiprocessing.freeze_support()` in line `9` is recommended to be called after the `if __name__ == '__main__':` block to allow the program.
3. Format whatever process you want to run into a function for both methods. In this case, `new_process` in line `4` is the function that runs in parallel, can you can see they all stops at the same time instead of executing linearly.

### Step 3: Send Parent Process Data to Child Process

For the following example, we will only use `multiprocessing.Pool` method. It is interchangable with `multiprocessing.Process` method.

```python title="code" linenums="1" hl_lines="4 6-7 14-15 18"
--8<-- "docs/HOW_TO/code/mp_pool1.py"
```
```bash title="code output"
--8<-- "docs/HOW_TO/log/mp_pool1_output.log"
```

- Line `14-15`: Create a list of tuples containing different arguments for the function.
- Line `18`: Spawn a pool of processes with independent input arguments.
- Line `6`: Unpack the tuple to retrieve the arguments.

You can see from the output that the parent process sends different arguments to the child process, and the child process receives the arguments correctly and prints them out.

### Step 4: Return Child Process Data to Parent Process with `multiprocessing.Manager`

For the following example, we will only use `multiprocessing.Pool` method and use `multiprocessing.Manager().dict()` to create a shared memory space between the parent and child processes.

With this method, child processes can also read and write to the shared memory space, which is useful when different child processes are responsible for different tasks and need to share data with themselves.

```python title="code" linenums="1" hl_lines="8-10 15-16 20 24 26-27 29-33"
--8<-- "docs/HOW_TO/code/mp_pool2.py"
```
```bash title="code output"
--8<-- "docs/HOW_TO/log/mp_pool2_output.log"
```

- Line `15-16`: Use `multiprocessing.Manager().dict()` to create a shared dictionary between the parent and child processes. In this case, child processes write to the dictionary, and the parent process read from the dictionary, this process is bi-directional.
- Line `20`: Add the shared dictionary to the input arguments.
- Line `8`: Perform some kind of operation in the child process.
- Line `10`: Write the result to the shared dictionary with `idx_start` as the key. This helps to keep track of the order of the results.
- Line `24`: Read the shared dictionary populated by the child processes.
- Line `26-27`: Order the dictionary by key and print the result, since child processes write to the dictionary once they finish, the order of the dictionary is not guaranteed. Depending on your use case, this step is optional.
- Line `29-33`: Retrieve data from shared dictionary as a list and print the result.

### Step 5: Share Data Between Parent and Child Processes with `multiprocessing.Queue`

For the following example, we will only use `multiprocessing.Pool` method and use `multiprocessing.Queue()` to create a shared memory space between the parent and child processes.

With this method, child processes can also read and write to the shared memory space, which is useful when different child processes are responsible for different tasks and need to share data with themselves.

Before using this, you need to know that a queue is a First-In-First-Out (FIFO) data structure, which means that the first element added to the queue will be the first element removed from the queue. Following are the common method for queue

- `put()`: Add an item to the queue. (at the end, last one to be removed)
- `get()`: Remove and return an item from the queue. (from the front, the oldest one)


```python title="code" linenums="1" hl_lines="8 14 20-21 23 31 33-34 36-39"
--8<-- "docs/HOW_TO/code/mp_pool3.py"
```
```bash title="code output"
--8<-- "docs/HOW_TO/log/mp_pool3_output.log"
```

- Line `20-21`: Create a queue to let parent send data to child processes, and another queue to let child processes send data back to the parent.
- Line `23`: Spawn a pool of processes and expose the queues to the child processes. Note that these processes will be reused for different tasks.
- Line `31`: Put the data into the queue to send to the child processes. The data can be any Python object, I use a dictionary for this example.
- Line `8`: While the queue is not empty, get the data from the queue.
- Line `14`: After processing the data, put the result into another queue to send back to the parent process.
- Line `33-34`: Wait for all child processes to finish. Note that these processes are not terminated, and will execute till the end of the program. You can terminate them if you want.
- Line `36-39`: Get the result from the queue.

This method is useful when each child process requires relaively small amount of time to process or you do not have sufficient memory to store several copies of the data. Each child process will live until all data is processed and dynamically accepts new tasks passed by parent process.

## Reference

1. [https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing)
2. [https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool)
3. [https://docs.python.org/3/library/queue.html](https://docs.python.org/3/library/queue.html)
4. [https://stackoverflow.com/questions/44660676/python-using-multiprocessing](https://stackoverflow.com/questions/44660676/python-using-multiprocessing)
5. [https://stackoverflow.com/questions/17241663/filling-a-queue-and-managing-multiprocessing-in-python](https://stackoverflow.com/questions/17241663/filling-a-queue-and-managing-multiprocessing-in-python)
6. [https://stackoverflow.com/questions/11515944/how-to-use-multiprocessing-queue-in-python](https://stackoverflow.com/questions/11515944/how-to-use-multiprocessing-queue-in-python)
7. [https://stackoverflow.com/questions/1540822/dumping-a-multiprocessing-queue-into-a-list](https://stackoverflow.com/questions/1540822/dumping-a-multiprocessing-queue-into-a-list)

## Error Correction

If you find any mistakes in the document, please create an [Issue](https://github.com/belongtothenight/belongtothenight.github.io/issues) or a [Pull request](https://github.com/belongtothenight/belongtothenight.github.io/pulls) or leave a message in [Discussions](https://github.com/belongtothenight/belongtothenight.github.io/discussions) or send me a mail directly with the mail icon at the bottom right. Thank you!
