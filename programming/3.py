from decimal import Decimal
import math
from fractions import Fraction

n = int(input())


def get_E(points, h):
    denominator = 0
    numerator = 0
    for i in range(0, h):

        points_list = points[i].split(' ')

        for j in range(0, len(points_list)):
            numerator += int(points_list[j]) * math.comb(i, j)

        denominator += pow(2, i)

    answer = Fraction(numerator, denominator)

    print(answer)


for i in range(0, n):
    h = int(input())
    points = []

    for j in range(0, h):
        points.append(input())

    get_E(points, h)
