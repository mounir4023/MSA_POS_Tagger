from lxml import etree
import re


root = etree.parse("corpus.xml")
sents = [ ]

for s in root.xpath("/CORPUS/Phrase"):
    tokens = re.sub(r'\s+',' ',s[2].text)
    sents.append({
            'num':s[0].text,
            'raw':s[1].text,
            'tokens':tokens.split(" "),
            'tags':s[3].text,
        })

for s in sents:
    for t in s["tokens"]:
        if t == '' or t == ' ':
            s["tokens"].remove(t)

