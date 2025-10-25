s1,s2 = input().split('-')
l1 = s1.split(' ')
l2 = s2.split(' ')
dic = {'3':1,'4':2,'5':3,'6':4,'7':5,'8':6,'9':7,'10':8,'J':9,'Q':10,'K':11,'A':12,'2':13,'joker':14,'JOKER':15}

def isboom(l):
    if len(l) == 4:
…        print('joker JOKER')
    elif isboom(l1):
        print(s1)
    elif isboom(l2):
        print(s2)
    else:
        print('ERROR')
