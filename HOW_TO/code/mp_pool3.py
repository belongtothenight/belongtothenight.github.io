import multiprocessing as mp
import time
import os

def worker_main(input_queue, output_queue):
    print(f"Time: {time.time():.2f} | Process ID: {os.getpid()} | working")
    while True:
        item = input_queue.get()
        print(f"Time: {time.time():.2f} | Process ID: {os.getpid()} | Received: {item}")
        time.sleep(1) # simulate a "long" operation
        calculation_result = item["idx_start"] + item["idx_end"]
        item["result"] = calculation_result
        item["status"] = "done"
        output_queue.put(item)
        print(f"Time: {time.time():.2f} | Process ID: {os.getpid()} | Result: {calculation_result}")

if __name__ == '__main__':
    mp.freeze_support()
    cpu_count = 4 #os.cpu_count()
    input_queue = mp.Queue()
    output_queue = mp.Queue()

    the_pool = mp.Pool(processes=cpu_count, initializer=worker_main, initargs=(input_queue, output_queue))

    increment = 1
    for i in range(cpu_count*2):
        data = {}
        data["status"] = "new"
        data["idx_start"] = i
        data["idx_end"] = (i+1)*increment
        input_queue.put(data)

    while (output_queue.qsize() < cpu_count*2):
        time.sleep(1)

    results = []
    while not output_queue.empty():
        item = output_queue.get()
        results.append(item)
    print(f"Time: {time.time():.2f} | Results: {results}")
