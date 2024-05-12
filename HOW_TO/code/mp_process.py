import multiprocessing as mp
import time
import os

def new_process(process_id):
    time.sleep(1)
    print(f"Time: {time.time():.2f} | Process ID: {os.getpid()} | Process Name: {mp.current_process().name}")

if __name__ == '__main__':
    mp.freeze_support()
    cpu_count = 4 #os.cpu_count()
    for i in range(cpu_count):
        p = mp.Process(target=new_process, args=(i,))
        p.start() # Control when the process starts
        # p.join() # Halts the main process until the child process is done
