import xml.etree.ElementTree as et
import xml.dom.minidom as md

from lxml import etree


root = etree.parse("corpus.xml")

for e in root.xpath("/CORPUS/Phrase")[:5]:
    print("num phrase: ",e[0].text)
    print("text: ",e[1].text)
    print("tokens: ",e[2].text)
    print("tags: ",e[3].text)


"""

from lxml import objectify

text = open("corpus.xml","r").read()
print(text)

root = objectify.fromstring(text)

print(root.subElement(root,"Text"))

for e in root:
"""
