# Task
#
# You are given a 2-D array with dimensions N X M.
# Your task is to perform the min function over axis 1 and then find the max of that.
#
# Input Format
#
# The first line of input contains the space separated values of N and M.
# The next N lines contains M space separated integers.
#
# Output Format
#
# Compute the min along axis 1 and then print the max of that result.
#
# Sample Input
#
# 4 2
# 2 5
# 3 7
# 1 3
# 4 0
#
# Sample Output
#
# 3
# Explanation
#
# The min along axis 1 = [2, 3, 1, 0]
# The max of [2, 3, 1, 0] = 3

import numpy

arr = numpy.array([input().split() for _ in range(int(input().split()[0]))], int)
print(numpy.max(numpy.min(arr, axis=1)))
