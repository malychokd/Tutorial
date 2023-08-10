import time
from multiprocessing import Pool, cpu_count

def factorize_number(n):
    factors = []
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors

def factorize(*numbers):
    result = []
    for number in numbers:
        result.append(factorize_number(number))
    return result

if __name__ == "__main__":
    # Перевірка роботи функції factorize
    a, b, c, d = factorize(128, 255, 99999, 10651060)

    #print(a)
    #print(b)
    #print(c)
    #print(d)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    # Вимірюємо час виконання синхронної версії
    start_time = time.time()
    factorize(128, 255, 99999, 10651060)
    end_time = time.time()
    elapsed_time_sync = end_time - start_time
    print(f"Час виконання синхронної версії: {elapsed_time_sync:.4f} секунд")

    # Вимірюємо час виконання паралельної версії
    num_cores = cpu_count()
    print(f"Кількість ядер процесора: {num_cores}")

    start_time = time.time()
    with Pool(num_cores) as p:
        p.map(factorize_number, [128, 255, 99999, 10651060])
    end_time = time.time()
    elapsed_time_parallel = end_time - start_time
    print(f"Час виконання паралельної версії: {elapsed_time_parallel:.4f} секунд")
