import re

file = open("Items.html", "r")
f2 = open("temp.wow", "w")
for i in range(1319):
    try:
        s = file.readline()
    except:
        if i != 1177:
            print(i)
            raise
    f2.write(re.sub(r"<(?:\"[^\"]*\"['\"]*|'[^']*'['\"]*|[^'\">])+>", "", s))
file.close()
f2.close()

'''

file = open("temp.wow", "r")
f2 = open("Effects.wow", "w")
for i in range(101):
    f2.write(file.readline())
    for j in range(14):
        file.readline()

'''