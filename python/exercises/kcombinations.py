def k_combinations(k, s):
    n = len(s)
    if 0 <= k and k <= n:
        if k == 0:
            return [set()]
        elif k == n:
            return [s]
        else:
            a = list(s)[0]
            b = s.difference({a})
            x = k_combinations(k, b)
            y = k_combinations(k-1, b)
            return x + [i.union({a}) for i in y]
    else:
        return []

print(k_combinations(1, {4, 5, 6}))
print(k_combinations(10, {4, 5, 6}))
print(k_combinations(2, {0, 1, 2}))
print(k_combinations(3, {0, 1, 2, 3, 4}))
