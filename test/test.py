z=['1','2']
print(z)

exit()
z={'as':1, 'vc':3}
if z:
    print('q')
#z.append('2')
for i in z.keys():
    print(z[i])

print(z.keys())
exit()
a=z.pop()
for i in z:
    a+='\\u001e'+i
print(z)
print(a)