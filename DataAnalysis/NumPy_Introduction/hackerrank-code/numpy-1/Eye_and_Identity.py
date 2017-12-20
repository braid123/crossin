# Task
#
# Your task is to print an array of size N X M with its main diagonal elements
# as 's and 's everywhere else.
#
# Input Format
#
# A single line containing the space separated values of N and M.
# N denotes the rows.
# M denotes the columns.
#
# Output Format
#
# Print the desired N X M array.
#
# Sample Input
#
# 3 3
# Sample Output
#
# [[ 1.  0.  0.]
#  [ 0.  1.  0.]
#  [ 0.  0.  1.]]

import numpy

x, y = [eval(i) for i in input().strip().split()]
print(numpy.eye(x, y))
