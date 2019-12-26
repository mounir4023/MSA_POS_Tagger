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


for s in sents:
    for t in s["tokens"]:
        if t == '' or t == ' ':
            print("\nempty char at: ",s["num"])

"""
for s in sents:
    empty = False
    for t in s["tokens"]:
        if re.match(r'\s+',t):
            empty = True
            print("VOID  num ",s["num"],"token:" ,t)
        elif not re.match("\w+|[.؟]",t):
            empty = True
            print("NO_ALPHA num ",s["num"],"token:" ,t)
        elif t == '':
            empty = True
            print("EMPTY num ",s["num"],"token:" ,t)

    if empty == True:
        print(s["tokens"],"\n")
        """

#print(sents[356]["tokens"][0]=='')
#print(re.match(r'\s+',sents[356]["tokens"][0]))

"""
for e in root.xpath("/CORPUS/Phrase"):
    if not (e[2].text.split(" ")[-1] == ".\n" and e[2].text.split(" ")[-1] == "\n" ):
        print("num phrase: ",e[0].text)
        #print("text: ",e[1].text)
        print("tokens: ",e[2].text)
        print("\nsplit: ", e[2].text.split(" "))
        #print("tags: ",e[3].text)
        #print(e[2].text.split(" "))
"""
