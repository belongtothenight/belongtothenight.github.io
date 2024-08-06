import multiprocessing as mp
import time
import os

def new_process(required_iterable_item):
    time.sleep(1)
    print(f"Time: {time.time():.2f} | Process ID: {os.getpid()} | Process Name: {mp.current_process().name}")

if __name__ == '__main__':
    mp.freeze_support()
    cpu_count = 4 #os.cpu_count()
    with mp.Pool(processes=cpu_count) as p:
        p.map(func=new_process, iterable=range(cpu_count))
