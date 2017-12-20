# Task
#
# You are given a square matrix A with dimensions N X N. Your task is to find the determinant.
#
# Input Format
#
# The first line contains the integer N.
# The next N lines contains the N space separated elements of array A.
#
# Output Format
#
# Print the determinant of A.
#
# Sample Input
#
# 2
# 1.1 1.1
# 1.1 1.1
#
# Sample Output
#
# 0.0

import numpy

n = int(input())
arr = numpy.array([input().split() for _ in range(n)], dtype=float)

print(numpy.linalg.det(arr))
