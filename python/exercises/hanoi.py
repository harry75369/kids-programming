def solve(n, src_pod, dst_pod, help_pod):
    if n == 1:
        print("moving a disk from %s to %s" % (src_pod, dst_pod))
    else:
        print("moving a disk from %s to %s" % (src_pod, help_pod))
        solve(n-1, src_pod, dst_pod, help_pod)
        print("moving a disk from %s to %s" % (help_pod, dst_pod))

print(solve(3, 'A', 'C', 'B'))
