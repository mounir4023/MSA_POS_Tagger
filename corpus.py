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

"""
for s in sents[10:15]:
    print(s["tokens"])
    print("start: ",s["tokens"][0]," end: ",s["tokens"][-1])
    pass
print(" ")

for sent in sents[10:15]:
    #if sent["tokens"][-1] == ['؟']:
        #sent["tokens"] = reversed(sent["tokens"]) 
        #pass
    #else:
    #elif sent["tokens"][-1] == ['.']:
        sent["tokens"][:-1] = reversed(sent["tokens"][:-1]) 

for s in sents[10:15]:
    print(s["tokens"])
    print("start: ",s["tokens"][0]," end: ",s["tokens"][-1])
    pass
"""

for s in sents:
    if s["tokens"][-1] == '؟':
        print(s["tokens"])
        print("start: ",s["tokens"][0]," end: ",s["tokens"][-1])



"""
for s in sents:
    for t in s["tokens"]:
        if t == '' or t == ' ':
            print("\nempty char at: ",s["num"])
"""
