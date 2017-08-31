def reverse(s):
    rs = ''
    for i in range(len(s)):
        rs = s[i] + rs
    return rs

print(reverse('Hello'))
