"""
Napisz program, który zwraca pary bliźniaczych liczb pierwszych dla dużego zakresu.
Dwie liczby pierwsze są bliźniacze, jeśli ich różnica jest równa 2 Przykłady: 3 i 5, 5 i 7.
Wykorzystaj moduł multiprocessing, aby utworzyć kilka procesów, z których każdy będzie
przetwarzał różne fragmenty zakresu.
"""

import multiprocessing

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def find_primes(start, end):
    primes = []
    for num in range(start, end+1):
        if is_prime(num):
            primes.append(num)
    # return primes
    prime_pairs = []
    for prim_num in range(len(primes)-1):
        if primes[prim_num+1] - primes[prim_num] == 2:
            prime_pairs.append((primes[prim_num], primes[prim_num+1]))
    return prime_pairs

def main(START_RANGE, END_RANGE):
    NUM_OF_PROCESSES = 4
    CHUNK_SIZE = (END_RANGE - START_RANGE) // NUM_OF_PROCESSES
    
    pool = multiprocessing.Pool(NUM_OF_PROCESSES)
    ranges = [(i, min(i+CHUNK_SIZE, END_RANGE)) for i in range(START_RANGE, END_RANGE, CHUNK_SIZE)]
    print(ranges)
    results = pool.starmap(find_primes, ranges)
    pool.close()
    pool.join()
    
    combined_result = []  
    for result in results:
        combined_result.append(result)
    return combined_result
        
        
if __name__ == '__main__':
    START_RANGE = 1 
    END_RANGE = 1000
    primes_pair = main(START_RANGE, END_RANGE)
    print(f"Pary bliźniaczych liczb pierwszych dla zakresu: {START_RANGE} do {END_RANGE}:\n {primes_pair}")
    
    # result = find_primes(1, 1000)
    # print(result)
    