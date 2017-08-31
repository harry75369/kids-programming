def bubble_sort(a):
    for i in range(len(a)):
        for j in range(i+1, len(a))[::-1]:
            if a[j-1] > a[j]:
                t = a[j-1]
                a[j-1] = a[j]
                a[j] = t
    return a

print(bubble_sort([3,1,4,1,5,9,2,6]))
