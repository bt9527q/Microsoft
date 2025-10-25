s = input()
t = input()
flag = 1
for i in s:
    if i not in t:
        flag = 0
        break
if flag:
    print('true')
