import sys
def f(wait,stack,out):
    if not wait and not stack:
        res.append(' '.join(out))
    if wait:
        f(wait[1:],stack+[wait[0]],out)
    if stack:
        f(wait,stack[:-1],out+[stack[-1]])

n = input()
num = input().split(' ')
res = []
f(num,[],[])
for i in sorted(res):
    print(i)
