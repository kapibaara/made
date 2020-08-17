n = int(input())

for i in range(0, n):
    number = int(input())

    if number == 1:
        print(3)
        continue
    if number == 2:
        print(5)
        continue

    k = 5
    exp = 0
    number = number - 2
    cycle_len = 2

    while number > 0:
        k = k + pow(2, exp)

        exp += 1

        if cycle_len == exp:
            k += 1
            exp = 0
            cycle_len = cycle_len + 1

        number -= 1

    print(k % 35184372089371)




