# -------- CS315 - Programming Assignment 1 --------
# -------------- SAMYAK PIYA (spi254) --------------

import math  # To make use of the floor function


def make_array(filename):
    file = open(filename, "r")
    lines = file.readlines()
    power_list = []

    lines.pop(0)  # Remove the column headers
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip("\n")
        lines[i] = lines[i].split(",")
        lines[i][1] = int(lines[i][1])
        power_list.append(lines[i][1])
    return power_list


# Variables to keep track of comparisons made in Insertion Sort
iSortComparisons = 0
mSortComparisons = 0
qSortComparisons = 0


# Function to print all the elements of an array
def print_array(array):
    print(f"The array elements after sorting are: [ ", end="")
    for i in range(len(array)):
        print(f"{array[i]} ", end="")
    print("]")


def print_runtime(filename, sort_algorithm, runtime):
    global iSortComparisons, mSortComparisons, qSortComparisons
    print(f"The runtime for sorting this array (converted from '{filename}') using {sort_algorithm} is {runtime}.")
    iSortComparisons, mSortComparisons, qSortComparisons = 0, 0, 0
    print()


# Insertion Sort
def insertion_sort(array):
    # Variable to keep track of comparisons made in Insertion Sort
    global iSortComparisons

    for j in range(1, len(array)):
        key = array[j]
        i = j - 1
        while i >= 0 and key < array[i]:
            iSortComparisons += 1  # a comparison was made every time this loop is entered
            array[i + 1] = array[i]
            i = i - 1
        iSortComparisons += 1  # because the loop runs 1 more time at the end
        array[i + 1] = key


# Merge Sort
def merge_sort(array, p, r):

    def merge(array, p, q, r):
        # Variable to keep track of comparisons made in Merge Sort
        global mSortComparisons

        m = q - p + 1  # length of the top sub-array
        n = r - q  # length of the bottom sub-array
        left_arr = []
        right_arr = []
        for i in range(m):
            left_arr.append( array[p+i])
        for j in range(n):
            right_arr.append(array[q+j+1])
        left_arr.append(100000)
        right_arr.append(100000)
        i = 0
        j = 0
        for k in range(p, r+1):
            mSortComparisons += 1  # A comparison is made only every time this loops is entered
            if left_arr[i] <= right_arr[j]:
                array[k] = left_arr[i]
                i = i + 1
            else:
                array[k] = right_arr[j]
                j = j + 1

    q = (p + r) / 2
    if p < r:
        q = math.floor(q)
        merge_sort(array, p, q)
        merge_sort(array, q+1, r)
        merge(array, p, q, r)


# Quick Sort
def quick_sort(array, p, r):

    def partition(array, p, r):
        global qSortComparisons

        pivot = array[r]
        i = p - 1
        for j in range(p, r):
            qSortComparisons += 1 # A comparison is made only every time this loops is entered
            if array[j] <= pivot:
                i = i + 1
                # exchange array[i] with array[j]
                temp = array[i]
                array[i] = array[j]
                array[j] = temp

        # exchange array[i+1] with array[r-1]
        temp = array[i+1]
        array[i+1] = array[r]
        array[r] = temp
        return i + 1

    if p < r:
        q = partition(array, p, r)
        quick_sort(array, p, q-1)
        quick_sort(array, q+1, r)


# # arr = [5, 2, 4, 7, 1, 3, 2, 6]
# # arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
# # arr = [10, 4, 6, 7, 2, 1, 3, 9, 8, 5]
# merge_sort(arr, 0, len(arr) - 1)
# print_array(arr)
# print(mSortComparisons)

# Convert the csv files into their required arrays
sorted_array_s = make_array("pokemonSortedSmall.csv")
reverse_array_s = make_array("pokemonReverseSortedSmall.csv")
random_array_s = make_array("pokemonRandomSmall.csv")

sorted_array_m = make_array("pokemonSortedMedium.csv")
reverse_array_m = make_array("pokemonReverseSortedMedium.csv")
random_array_m = make_array("pokemonRandomMedium.csv")

sorted_array_l = make_array("pokemonSortedLarge.csv")
reverse_array_l = make_array("pokemonReverseSortedLarge.csv")
random_array_l = make_array("pokemonRandomLarge.csv")

# Make a copy of the arrays for Insertion Sort
iSort_sorted_array_s = sorted_array_s.copy()
iSort_reverse_array_s = reverse_array_s.copy()
iSort_random_array_s = random_array_s.copy()

iSort_sorted_array_m = sorted_array_m.copy()
iSort_reverse_array_m = reverse_array_m.copy()
iSort_random_array_m = random_array_m.copy()

iSort_sorted_array_l = sorted_array_l.copy()
iSort_reverse_array_l = reverse_array_l.copy()
iSort_random_array_l = random_array_l.copy()

# Run Insertion Sort on the arrays
print("************************INSERTION SORT****************************", end="\n\n")
insertion_sort(iSort_sorted_array_s)
print_array(iSort_sorted_array_s)
print_runtime("pokemonSortedSmall.csv", "INSERTION SORT", iSortComparisons)

insertion_sort(iSort_reverse_array_s)
print_array(iSort_reverse_array_s)
print_runtime("pokemonReverseSortedSmall.csv", "INSERTION SORT", iSortComparisons)

insertion_sort(iSort_random_array_s)
print_array(iSort_random_array_s)
print_runtime("pokemonRandomSmall.csv", "INSERTION SORT", iSortComparisons)

insertion_sort(iSort_sorted_array_m)
print_array(iSort_sorted_array_m)
print_runtime("pokemonSortedMedium.csv", "INSERTION SORT", iSortComparisons)

insertion_sort(iSort_reverse_array_m)
print_array(iSort_reverse_array_m)
print_runtime("pokemonReverseSortedMedium.csv", "INSERTION SORT", iSortComparisons)

insertion_sort(iSort_random_array_m)
print_array(iSort_random_array_m)
print_runtime("pokemonRandomMedium.csv", "INSERTION SORT", iSortComparisons)

insertion_sort(iSort_sorted_array_l)
print_array(iSort_sorted_array_l)
print_runtime("pokemonSortedLarge.csv", "INSERTION SORT", iSortComparisons)

insertion_sort(iSort_reverse_array_l)
print_array(iSort_reverse_array_l)
print_runtime("pokemonReverseSortedLarge.csv", "INSERTION SORT", iSortComparisons)

insertion_sort(iSort_random_array_l)
print_array(iSort_random_array_l)
print_runtime("pokemonRandomLarge.csv", "INSERTION SORT", iSortComparisons)
# End of Insertion Sort


# Make a copy of the arrays for Merge Sort
mSort_sorted_array_s = sorted_array_s.copy()
mSort_reverse_array_s = reverse_array_s.copy()
mSort_random_array_s = random_array_s.copy()
mSort_sorted_array_m = sorted_array_m.copy()
mSort_reverse_array_m = reverse_array_m.copy()
mSort_random_array_m = random_array_m.copy()
mSort_sorted_array_l = sorted_array_l.copy()
mSort_reverse_array_l = reverse_array_l.copy()
mSort_random_array_l = random_array_l.copy()

# Run Merge Sort on the arrays
print("****************************MERGE SORT****************************", end="\n\n")
merge_sort(mSort_sorted_array_s, 0, len(mSort_sorted_array_s) - 1)
print_array(mSort_sorted_array_s)
print_runtime("pokemonSortedSmall.csv", "MERGE SORT", mSortComparisons)

merge_sort(mSort_reverse_array_s, 0, len(mSort_reverse_array_s) - 1)
print_array(mSort_reverse_array_s)
print_runtime("pokemonReverseSortedSmall.csv", "MERGE SORT", mSortComparisons)

merge_sort(mSort_random_array_s, 0, len(mSort_random_array_s) - 1)
print_array(mSort_random_array_s)
print_runtime("pokemonRandomSmall.csv", "MERGE SORT", mSortComparisons)

merge_sort(mSort_sorted_array_m, 0, len(mSort_sorted_array_m) - 1)
print_array(mSort_sorted_array_m)
print_runtime("pokemonSortedMedium.csv", "MERGE SORT", mSortComparisons)

merge_sort(mSort_reverse_array_m, 0, len(mSort_reverse_array_m) - 1)
print_array(mSort_reverse_array_m)
print_runtime("pokemonReverseSortedMedium.csv", "MERGE SORT", mSortComparisons)

merge_sort(mSort_random_array_m, 0, len(mSort_random_array_m) - 1)
print_array(mSort_random_array_m)
print_runtime("pokemonRandomMedium.csv", "MERGE SORT", mSortComparisons)

merge_sort(mSort_sorted_array_l, 0, len(mSort_sorted_array_l) - 1)
print_array(mSort_sorted_array_l)
print_runtime("pokemonSortedLarge.csv", "MERGE SORT", mSortComparisons)

merge_sort(mSort_reverse_array_l, 0, len(mSort_reverse_array_l) - 1)
print_array(mSort_reverse_array_l)
print_runtime("pokemonReverseSortedLarge.csv", "MERGE SORT", mSortComparisons)

merge_sort(mSort_random_array_l, 0, len(mSort_random_array_l) - 1)
print_array(mSort_random_array_l)
print_runtime("pokemonRandomLarge.csv", "MERGE SORT", mSortComparisons)
# End of Merge Sort

# Make a copy of the arrays for Quick Sort
qSort_sorted_array_s = sorted_array_s.copy()
qSort_reverse_array_s = reverse_array_s.copy()
qSort_random_array_s = random_array_s.copy()
qSort_sorted_array_m = sorted_array_m.copy()
qSort_reverse_array_m = reverse_array_m.copy()
qSort_random_array_m = random_array_m.copy()
qSort_sorted_array_l = sorted_array_l.copy()
qSort_reverse_array_l = reverse_array_l.copy()
qSort_random_array_l = random_array_l.copy()

# Run Quick Sort on the arrays
print("****************************QUICK SORT****************************", end="\n\n")
quick_sort(qSort_sorted_array_s, 0, len(qSort_sorted_array_s) - 1)
print_array(qSort_sorted_array_s)
print_runtime("pokemonSortedSmall.csv", "QUICK SORT", qSortComparisons)

quick_sort(qSort_reverse_array_s, 0, len(qSort_reverse_array_s) - 1)
print_array(qSort_reverse_array_s)
print_runtime("pokemonReverseSortedSmall.csv", "QUICK SORT", qSortComparisons)

quick_sort(qSort_random_array_s, 0, len(qSort_random_array_s) - 1)
print_array(qSort_random_array_s)
print_runtime("pokemonRandomSmall.csv", "QUICK SORT", qSortComparisons)

quick_sort(qSort_sorted_array_m, 0, len(qSort_sorted_array_m) - 1)
print_array(qSort_sorted_array_m)
print_runtime("pokemonSortedMedium.csv", "QUICK SORT", qSortComparisons)

quick_sort(qSort_reverse_array_m, 0, len(qSort_reverse_array_m) - 1)
print_array(qSort_reverse_array_m)
print_runtime("pokemonReverseSortedMedium.csv", "QUICK SORT", qSortComparisons)

quick_sort(qSort_random_array_m, 0, len(qSort_random_array_m) - 1)
print_array(qSort_random_array_m)
print_runtime("pokemonRandomMedium.csv", "QUICK SORT", qSortComparisons)

quick_sort(qSort_sorted_array_l, 0, len(qSort_sorted_array_l) - 1)
print_array(qSort_sorted_array_l)
print_runtime("pokemonSortedLarge.csv", "QUICK SORT", qSortComparisons)

quick_sort(qSort_reverse_array_l, 0, len(qSort_reverse_array_l) - 1)
print_array(qSort_reverse_array_l)
print_runtime("pokemonReverseSortedLarge.csv", "QUICK SORT", qSortComparisons)

quick_sort(qSort_random_array_l, 0, len(qSort_random_array_l) - 1)
print_array(qSort_random_array_l)
print_runtime("pokemonRandomLarge.csv", "QUICK SORT", qSortComparisons)
print("******************************************************************")
# End of Quick Sort
