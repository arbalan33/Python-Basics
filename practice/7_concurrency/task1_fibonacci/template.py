import os
from random import randint
import multiprocessing
import threading
import queue
from pathlib import Path


OUTPUT_DIR = './practice/7_concurrency/task1_fibonacci/output'
RESULT_FILE = './practice/7_concurrency/task1_fibonacci/output/_result.csv'


def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n-1):
        f0, f1 = f1, f0 + f1
    return f1


def process_fib(n):
    '''Compute and store result in a file in the given directory'''
    result = fib(n)
    file = Path(OUTPUT_DIR) / f'{n}.txt'
    with file.open('w') as f:
        f.write(str(result))


def func1(array: list):
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        pool.map(process_fib, array)



def read_and_append(Q, result_file, lock):
    while True:
        filepath: Path = Q.get()
        if filepath is None:
            break
        with filepath.open() as file:
            result = file.read().strip()
            with lock:
                with open(result_file, 'a') as f:
                    f.write(f'{filepath.stem},{result}\n')
        Q.task_done()


def func2(result_file: str):
    Q = queue.Queue()
    lock = threading.Lock()
    thread_count = 10

    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=read_and_append, args=(Q, result_file, lock))
        thread.start()
        threads.append(thread)

    for filepath in Path(OUTPUT_DIR).glob("*.txt"):
        Q.put(filepath)

    # Close all the threads with a sentinel value
    for _ in range(thread_count):
        Q.put(None)

    
    for thread in threads:
        thread.join()


def get_input_nums(N=10):
    return [randint(1000, 100000) for _ in range(N)]


if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    N = 1_000

    import time
    start = time.perf_counter()
    func1(get_input_nums(N))
    print(f"Computed in {time.perf_counter() - start:.2f} seconds")

    start = time.perf_counter()
    func2(result_file=RESULT_FILE)
    print(f"Aggregated in {time.perf_counter() - start:.2f} seconds")

