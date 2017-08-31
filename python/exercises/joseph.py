def joseph(n, k):

    queue = list(range(1, n+1))
    print("initial:", queue, "count:", k)
    print("===================================")
    index = 0
    nLeft = len(queue)
    while nLeft > 1:
        index = (index + k - 1) % nLeft
        killed = queue.pop(index)
        nLeft = len(queue)
        print("killed =", killed)
        print("left =", queue, ", current index =", index)
        print("===================================")

    print("survived:", queue[0])

joseph(10, 9)
