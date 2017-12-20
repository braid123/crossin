# Task
#
# You are given two arrays (A & B) of dimensions NXM.
# Your task is to perform the following operations:
#
# Add (A + B)
# Subtract (A - B)
# Multiply (A * B)
# Divide (A / B)
# Mod (A % B)
# Power (A ** B)
#
# Input Format
#
# The first line contains two space separated integers, N and M.
# The next N lines contains M space separated integers of array A.
# The following N lines contains M space separated integers of array B.
#
# Output Format
#
# Print the result of each operation in the given order under Task.
#
# Sample Input
#
# 1 4
# 1 2 3 4
# 5 6 7 8
#
# Sample Output
#
# [[ 6  8 10 12]]
# [[-4 -4 -4 -4]]
# [[ 5 12 21 32]]
# [[0 0 0 0]]
# [[1 2 3 4]]
# [[    1    64  2187 65536]]
# Use // for division in Python 3.

import numpy

x, y = [eval(i) for i in input().strip().split()]
arr1 = numpy.array([input().split() for _ in range(x)], dtype=int).reshape(x, y)
arr2 = numpy.array([input().split() for _ in range(x)], dtype=int).reshape(x, y)

print(arr1 + arr2)
print(arr1 - arr2)
print(arr1 * arr2)
print(arr1 // arr2)
print(arr1 % arr2)
print(arr1 ** arr2)
