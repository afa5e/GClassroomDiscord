f = open('discriminatedUsers.txt', 'r')
mutedList = list(map(lambda a:a.rstrip(),f))
f.close()

muted = {}
for item in mutedList:
    muted[item] = [0, 0]

print(muted)
