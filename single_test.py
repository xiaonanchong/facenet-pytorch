import general_test
e, l = general_test.embedding('liuchun.txt')
print(e, l)
print(len(e))

for i in range(3):
  for t in range(3):
    d = (e[i]-e[t]).norm().item()
    print(d, end = '	')
  print('\n')

