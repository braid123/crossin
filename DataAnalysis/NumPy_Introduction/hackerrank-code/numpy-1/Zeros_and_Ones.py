# Task
#
# You are given the shape of the array in the form of space-separated integers,
# each integer representing the size of different dimensions,
# your task is to print an array of the given shape and integer type using
# the tools numpy.zeros and numpy.ones.
#
# Input Format
#
# A single line containing the space-separated integers.
#
# Constraints
#
# 1 <= each integer <= 3
#
# Output Format
#
# First, print the array using the numpy.zeros tool and then print the array
# with the numpy.ones tool.
#
# Sample Input 0
#
# 3 3 3
# Sample Output 0
#
# [[[0 0 0]
#   [0 0 0]
#   [0 0 0]]
#
#  [[0 0 0]
#   [0 0 0]
#   [0 0 0]]
#
#  [[0 0 0]
#   [0 0 0]
#   [0 0 0]]]
# [[[1 1 1]
#   [1 1 1]
#   [1 1 1]]
#
#  [[1 1 1]
#   [1 1 1]
#   [1 1 1]]
#
#  [[1 1 1]
#   [1 1 1]
#   [1 1 1]]]
#
# Explanation 0
#
# Print the array built using numpy.zeros and numpy.ones tools and you get
# the result as shown.

import numpy

N = tuple([eval(i) for i in input().strip().split()])

print(numpy.zeros(N, dtype=int))
print(numpy.ones(N, dtype=int))
