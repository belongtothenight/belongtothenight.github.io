import multiprocessing as mp
import time
import collections

def new_process(input_data):
    time.sleep(1)
    idx_start, idx_end, return_dict = input_data
    calculation_result = idx_start + idx_end
    print(f"Time: {time.time():.2f} | Start: {idx_start} | End: {idx_end} | Result: {calculation_result}")
    return_dict[idx_start] = calculation_result

if __name__ == '__main__':
    mp.freeze_support()
    cpu_count = 4 #os.cpu_count()
    manager = mp.Manager()
    return_dict = manager.dict()

    # Create a list of input data
    increment = 1
    input_data = [(i*increment, (i+1)*increment, return_dict) for i in range(cpu_count)]

    with mp.Pool(processes=cpu_count) as p:
        p.map(func=new_process, iterable=input_data)
    print(f"Return Dict: {return_dict}")

    return_dict = collections.OrderedDict(sorted(return_dict.items()))
    print(f"Ordered Dict: {return_dict}")

    final_arr = []
    for key, value in return_dict.items():
        #print(f"Key: {key} / Value: {value}")
        final_arr.append(value)
    print(f"Final Array: {final_arr}")
