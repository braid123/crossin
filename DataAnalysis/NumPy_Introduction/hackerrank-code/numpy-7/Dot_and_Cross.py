# Task
#
# You are given two arrays A and B. Both have dimensions of N X N.
# Your task is to compute their matrix product.
#
# Input Format
#
# The first line contains the integer N.
# The next N lines contains N space separated integers of array A.
# The following N lines contains N space separated integers of array B.
#
# Output Format
#
# Print the matrix multiplication of A and B.
#
# Sample Input
#
# 2
# 1 2
# 3 4
# 1 2
# 3 4
#
# Sample Output
#
# [[ 7 10]
#  [15 22]]

import numpy

n = int(input())
arr1 = numpy.array([input().split() for _ in range(n)], dtype=int)
arr2 = numpy.array([input().split() for _ in range(n)], dtype=int)

print(numpy.dot(arr1, arr2))
