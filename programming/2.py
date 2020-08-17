n = int(input())


def find_rectangles(points, n):
    points_list = [*points]
    n_rect = 0
    for i in range(0, n):
        for j in range(i + 1, n):
            x1, y1 = points_list[i].split(' ')
            x2, y2 = points_list[j].split(' ')

            x1_y2 = ' '.join([x1, y2])
            x2_y1 = ' '.join([x2, y1])

            if (x1_y2 in points) and (x2_y1 in points) and (x1 != x2) and (y1 != y2):
                n_rect += 1
    print(int(n_rect / 2))


for i in range(0, n):
    n_points = int(input())
    points = {}

    for j in range(0, n_points):
        points[input()] = True

    find_rectangles(points, n_points)
