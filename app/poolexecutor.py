from typing import Callable, Set, Any

from time import time
from multiprocessing.pool import Pool, ThreadPool
from threading import Thread


class PoolExecutor(object):

    def __init__(self, num_workers):
        self.num_workers = num_workers

    def multiprocessing_pool(self, func: Callable, arguments_set: Set[Any]):
        pool_start_time = time()
        with Pool(self.num_workers) as pool:
            pool_start_time = time() - pool_start_time
            pool.map(func, arguments_set)
            pool_teardown_time = time()
        pool_teardown_time = time() - pool_teardown_time
        print(f'MP Pool creation of {self.num_workers} for {func.__name__} took {pool_start_time * 1000:.2f}ms,'
              f'teardown {pool_teardown_time * 1000:.2f}ms')

    def multiprocessing_threads(self, func: Callable, arguments_set: Set[Any]):
        pool_start_time = time()
        with ThreadPool(self.num_workers) as pool:
            pool_start_time = time() - pool_start_time
            pool.starmap(func, arguments_set)
            pool_teardown_time = time()
        pool_teardown_time = time() - pool_teardown_time
        print(f'ThreadPool creation of {self.num_workers} for {func.__name__} took {pool_start_time * 1000:.2f}ms,'
              f'teardown {pool_teardown_time * 1000:.2f}ms')

    @staticmethod
    def threading_threads(func: Callable, arguments_set: Set[Any]):
        threads = []
        for arguments in arguments_set:
            thread = Thread(target=func, args=(arguments, ))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
