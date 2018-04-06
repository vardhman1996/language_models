import nltk
from nltk import word_tokenize


s = "ওয়ান পিছের তুমি কতো গুল পর্ব দেখেছো?"
l = [i for i in s]
p = s.encode("utf-8")
print(l[0])


v = b'\x75'.decode("utf-8")
# print(v)


print(ord(l[0]))
print(chr(2451))