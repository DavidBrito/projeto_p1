from string import ascii_letters

st = "as@d ax1sd as.df"
vc = ""

for i in st:
    if i in ascii_letters:
        vc += i
    else:
        vc += " "

print (vc)
print (vc.split())
