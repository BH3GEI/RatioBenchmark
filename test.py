import time
import math
import random
import subprocess
import os

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def prime_check(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def matrix_multiply(n):
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    C = [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    return C

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def gcc_compile_test():
    test_code = """
    #include <stdio.h>
    #include <stdlib.h>
    
    int main() {
        int n = 1000000;
        int* arr = (int*)malloc(n * sizeof(int));
        for (int i = 0; i < n; i++) {
            arr[i] = rand();
        }
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (arr[i] > arr[j]) {
                    int temp = arr[i];
                    arr[i] = arr[j];
                    arr[j] = temp;
                }
            }
        }
        printf("%d\\n", arr[n/2]);
        free(arr);
        return 0;
    }
    """
    with open("test.c", "w") as f:
        f.write(test_code)
    
    start = time.time()
    subprocess.run(["gcc", "-O2", "test.c", "-o", "test"], check=True)
    compile_time = time.time() - start
    
    os.remove("test.c")
    if os.path.exists("test"):
        os.remove("test")
    
    return compile_time

def run_benchmark(scale=1):
    print(f"Starting benchmark (scale: {scale})...")
    
    # Fibonacci
    start = time.time()
    fib_result = fibonacci(30 * scale)
    fib_time = time.time() - start
    print(f"Fibonacci({30 * scale}) result: {fib_result}, Time: {fib_time:.15f} seconds")

    # Prime numbers
    start = time.time()
    prime_count = sum(1 for i in range(2, 10000 * scale) if prime_check(i))
    prime_time = time.time() - start
    print(f"Prime numbers up to {10000 * scale}: {prime_count}, Time: {prime_time:.15f} seconds")

    # Matrix multiplication
    start = time.time()
    matrix_result = matrix_multiply(100 * scale)
    matrix_time = time.time() - start
    print(f"{100 * scale}x{100 * scale} Matrix multiplication completed, Time: {matrix_time:.15f} seconds")

    # Quicksort
    arr = [random.randint(1, 1000000) for _ in range(100000 * scale)]
    start = time.time()
    sorted_arr = quicksort(arr)
    sort_time = time.time() - start
    print(f"Quicksort of {100000 * scale} elements completed, Time: {sort_time:.15f} seconds")

    # Floating point operations
    start = time.time()
    result = 0
    for _ in range(1000000 * scale):
        result += math.sin(random.random()) * math.cos(random.random())
    float_time = time.time() - start
    print(f"1000000 * {scale} floating point operations completed, Time: {float_time:.15f} seconds")

    # GCC Compile test
    try:
        gcc_time = gcc_compile_test()
        print(f"GCC compilation test completed, Time: {gcc_time:.15f} seconds")
    except Exception as e:
        print(f"GCC compilation test failed: {e}")
        gcc_time = None

    return fib_time, prime_time, matrix_time, sort_time, float_time, gcc_time

if __name__ == "__main__":
    num_runs = 5
    scale = 1
    all_results = []

    for i in range(num_runs):
        print(f"\nRun {i+1} of {num_runs}")
        results = run_benchmark(scale)
        all_results.append(results)
        print("\n")

    # Calculate and print average results
    avg_results = [sum(r) / num_runs for r in zip(*all_results) if all(r[i] is not None for i in range(num_runs))]
    
    print("Average results over 5 runs:")
    print(f"Fibonacci: {avg_results[0]:.15f} seconds")
    print(f"Prime numbers: {avg_results[1]:.15f} seconds")
    print(f"Matrix multiplication: {avg_results[2]:.15f} seconds")
    print(f"Quicksort: {avg_results[3]:.15f} seconds")
    print(f"Floating point operations: {avg_results[4]:.15f} seconds")
    if len(avg_results) > 5:
        print(f"GCC compilation: {avg_results[5]:.15f} seconds")

    # Calculate relative scores (lower is better)
    base_times = [0.133163404464722, 0.005249691009521, 0.066241168975830, 0.168012475967407, 0.186379480361938, 0.153760194778442]  # You can set these to the times from a reference machine
    relative_scores = [avg / base for avg, base in zip(avg_results, base_times)]
    
    print("\nRelative Scores (lower is better):")
    print(f"Fibonacci: {relative_scores[0]:.15f}")
    print(f"Prime numbers: {relative_scores[1]:.15f}")
    print(f"Matrix multiplication: {relative_scores[2]:.15f}")
    print(f"Quicksort: {relative_scores[3]:.15f}")
    print(f"Floating point operations: {relative_scores[4]:.15f}")
    if len(relative_scores) > 5:
        print(f"GCC compilation: {relative_scores[5]:.15f}")
    
    # Calculate composite score (geometric mean of relative scores)
    composite_score = math.pow(math.prod(relative_scores), 1/len(relative_scores))
    print(f"\nComposite Score: {composite_score:.15f} (lower is better)")

    # Calculate original composite score
    original_composite_score = 1 / math.prod(avg_results) * 1000000000
    print(f"Original Composite Score: {original_composite_score:.15f} (higher is better)")