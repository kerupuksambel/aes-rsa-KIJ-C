import RSA
pt = "Testing for RSA!"
print(pt)
ct = RSA.enc(pt)
print(ct)
rpt = RSA.dec(ct)
print(rpt)
