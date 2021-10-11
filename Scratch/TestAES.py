import AES, string, random
pt = ''.join([random.choice(string.ascii_letters) for _ in range(16)]).encode()
print(pt.decode())
ct = AES.enc(pt, AES.keys)
print(''.join([chr(_) for _ in ct]))
rpt = AES.dec(ct, AES.keys)
print(''.join([chr(_) for _ in rpt]))
