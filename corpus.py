from lxml import etree
import re


root = etree.parse("corpus.xml")
sents = [ ]

for s in root.xpath("/CORPUS/Phrase"):
    tokens = re.sub(r'\s+',' ',s[2].text)
    tags = re.sub(r'\s+',' ',s[3].text)
    sents.append({
            'num':s[0].text,
            'raw':s[1].text,
            'tokens':tokens.split(" "),
            'tags':tags.split(" "),
        })

for s in sents:
    for t in s["tokens"]:
        if t == '' or t == ' ':
            s["tokens"].remove(t)
    for t in s["tags"]:
        if t == '' or t == ' ':
            s["tags"].remove(t)

for s in sents:
    if len(s["tokens"]) != len(s["tags"]) -1 :
        print(s["num"])

print(sents[892]["raw"])
print(sents[892]["tokens"])
print(sents[892]["tags"])

"""
s = sents[20]
print(s["tags"])

for t in s["tokens"]:
    print(t)
print("\n",s["tokens"],"\n")

s["tokens"][0:0] = ['<START>']

for t in s["tokens"]:
    print(t)
print("\n",s["tokens"],"\n")
"""
