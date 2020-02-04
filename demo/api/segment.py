import os

source = os.path.abspath(".")+"/api/source.txt"
out = os.path.abspath(".")+"/api/out.txt"

cmd = "perl -w < "+source+" > "+out

print(os.path.abspath("."))
print(source)
print(out)

os.system(cmd)
