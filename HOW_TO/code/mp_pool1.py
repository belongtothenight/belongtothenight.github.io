import multiprocessing as mp
import time

def new_process(input_data):
    time.sleep(1)
    idx_start, idx_end = input_data
    print(f"Time: {time.time():.2f} | Start: {idx_start} | End: {idx_end}")

if __name__ == '__main__':
    mp.freeze_support()
    cpu_count = 4 #os.cpu_count()

    # Create a list of input data
    increment = 1
    input_data = [(i*increment, (i+1)*increment) for i in range(cpu_count)]

    with mp.Pool(processes=cpu_count) as p:
        p.map(func=new_process, iterable=input_data)
