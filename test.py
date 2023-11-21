from typing import BinaryIO
import pickle


f : BinaryIO
l : list

f = open("data.dat","rb")

l = pickle.load(f)

for i in range(len(l)):
    print(l[i].name,l[i].score,l[i].nbGame)
print(len(l))
f.close()