import RSA
pt = "[1,2,3,4,5,6,7,8,9,0]"
print(pt)
ct = RSA.enc(pt)
print(ct)
rpt = RSA.dec(ct)
print(rpt)
