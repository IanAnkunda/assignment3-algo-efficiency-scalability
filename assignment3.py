"""
Assignment 3: Algorithm Efficiency and Scalability

"""

import csv
import random
import sys
import time

sys.setrecursionlimit(1000000)


# --------
# Quick Sort Section
# -----

def random_pivot_quicksort(items):
    arr = items.copy()

    def sort(left, right):
        if left >= right:
            return

        pivot_index = random.randint(left, right)
        pivot = arr[pivot_index]

        low = left
        current = left
        high = right

        while current <= high:
            if arr[current] < pivot:
                arr[low], arr[current] = arr[current], arr[low]
                low += 1
                current += 1
            elif arr[current] > pivot:
                arr[current], arr[high] = arr[high], arr[current]
                high -= 1
            else:
                current += 1

        sort(left, low - 1)
        sort(high + 1, right)

    sort(0, len(arr) - 1)
    return arr


def first_pivot_quicksort(items):
    arr = items.copy()

    def sort(left, right):
        if left >= right:
            return

        pivot = arr[left]

        low = left
        current = left
        high = right

        while current <= high:
            if arr[current] < pivot:
                arr[low], arr[current] = arr[current], arr[low]
                low += 1
                current += 1
            elif arr[current] > pivot:
                arr[current], arr[high] = arr[high], arr[current]
                high -= 1
            else:
                current += 1

        sort(left, low - 1)
        sort(high + 1, right)

    sort(0, len(arr) - 1)
    return arr


def make_list(list_type, size):
    if list_type == "random":
        return [random.randint(0, size * 10) for _ in range(size)]

    if list_type == "sorted":
        return list(range(size))

    if list_type == "reverse":
        return list(range(size, 0, -1))

    if list_type == "repeated":
        return [random.randint(0, 20) for _ in range(size)]

    raise ValueError("Unknown list type")


def test_speed(sort_function, data, tries=3):
    times = []
    correct_answer = sorted(data)

    for _ in range(tries):
        start = time.perf_counter()
        result = sort_function(data)
        end = time.perf_counter()

        if result != correct_answer:
            raise Exception(sort_function.__name__ + " did not sort correctly")

        times.append(end - start)

    return sum(times) / len(times)


def run_sort_tests():
    random.seed(42)

    sizes = [500, 1000, 2000, 4000]
    list_types = ["random", "sorted", "reverse", "repeated"]

    methods = [
        ("Random Pivot Quick Sort", random_pivot_quicksort),
        ("First Pivot Quick Sort", first_pivot_quicksort),
    ]

    results = []

    for size in sizes:
        for list_type in list_types:
            data = make_list(list_type, size)

            for method_name, method in methods:
                avg_time = test_speed(method, data)

                results.append({
                    "Algorithm": method_name,
                    "List Type": list_type,
                    "Size": size,
                    "Average Time": round(avg_time, 6)
                })

    with open("benchmark_results.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    return results


# --------
# Hash Table
# --------

class HashTable:

    def __init__(self, start_size=8):
        self.buckets = [[] for _ in range(start_size)]
        self.count = 0
        self.max_load = 0.75
        self.min_load = 0.20

        self.prime = 1000003
        self.a = random.randint(1, self.prime - 1)
        self.b = random.randint(0, self.prime - 1)

    def load_factor(self):
        return self.count / len(self.buckets)

    def hash_key(self, key):
        return ((self.a * key + self.b) % self.prime) % len(self.buckets)

    def resize(self, new_size):
        old_items = []

        for bucket in self.buckets:
            for key, value in bucket:
                old_items.append((key, value))

        self.buckets = [[] for _ in range(max(8, new_size))]
        self.count = 0

        for key, value in old_items:
            self.insert(key, value)

    def insert(self, key, value):
        index = self.hash_key(key)
        bucket = self.buckets[index]

        for i in range(len(bucket)):
            old_key, old_value = bucket[i]

            if old_key == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.count += 1

        if self.load_factor() > self.max_load:
            self.resize(len(self.buckets) * 2)

    def search(self, key):
        index = self.hash_key(key)

        for stored_key, value in self.buckets[index]:
            if stored_key == key:
                return value

        return None

    def delete(self, key):
        index = self.hash_key(key)
        bucket = self.buckets[index]

        for i in range(len(bucket)):
            stored_key, value = bucket[i]

            if stored_key == key:
                bucket.pop(i)
                self.count -= 1

                if len(self.buckets) > 8 and self.load_factor() < self.min_load:
                    self.resize(len(self.buckets) // 2)

                return True

        return False

    def show_stats(self):
        chain_lengths = [len(bucket) for bucket in self.buckets]

        return {
            "items": self.count,
            "buckets": len(self.buckets),
            "load_factor": round(self.load_factor(), 3),
            "longest_chain": max(chain_lengths),
            "average_chain": round(sum(chain_lengths) / len(chain_lengths), 3)
        }


def hash_table_demo():
    """Small demo for insert, search, and delete."""
    table = HashTable()

    table.insert(101, "Alice")
    table.insert(205, "Brian")
    table.insert(309, "Cynthia")
    table.insert(413, "Daniel")

    print("Search key 205:", table.search(205))
    print("Delete key 205:", table.delete(205))
    print("Search key 205 again:", table.search(205))
    print("Hash table stats:", table.show_stats())


# -----------------------------
# Main Program
# -----------------------------

if __name__ == "__main__":
    print("Running quick sort tests...")

    results = run_sort_tests()

    print("\nSample benchmark results:")
    for row in results[:8]:
        print(row)

    print("\nResults ")

    print("\nRunning hash table demo...")
    hash_table_demo()