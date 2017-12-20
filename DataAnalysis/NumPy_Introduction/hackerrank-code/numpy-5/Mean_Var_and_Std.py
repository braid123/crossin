# Task
#
# You are given a 2-D array of size N X M.
# Your task is to find:
#
# The mean along axis 1
# The var along axis 0
# The std along axis None
#
# Input Format
#
# The first line contains the space separated values of N and M.
# The next N lines contains M space separated integers.
#
# Output Format
#
# First, print the mean.
# Second, print the var.
# Third, print the std.
#
# Sample Input
#
# 2 2
# 1 2
# 3 4
#
# Sample Output
#
# [ 1.5  3.5]
# [ 1.  1.]
# 1.11803398875

import numpy

arr = numpy.array([input().split() for _ in range(int(input().split()[0]))], int)

print(numpy.mean(arr, axis=1))
print(numpy.var(arr, axis=0))
print(numpy.std(arr))
