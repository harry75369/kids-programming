a = [[1,[[2]]],3,[4,[5,6]]]

def flatten(lst):
    if len(lst) == 0:
        return []
    x = lst[0]
    y = lst[1:]
    if type(x) is not list:
        return [x] + flatten(y)
    else:
        return flatten(x) + flatten(y)

print(flatten(a))
