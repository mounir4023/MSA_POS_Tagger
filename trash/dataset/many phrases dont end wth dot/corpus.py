import xml.etree.ElementTree as et
import xml.dom.minidom as md

from lxml import etree


root = etree.parse("corpus.xml")

for e in root.xpath("/CORPUS/Phrase"):

    if not (e[2].text.split(" ")[-1] == ".\n" and e[2].text.split(" ")[-1] == "\n" ):
        print("num phrase: ",e[0].text)
        #print("text: ",e[1].text)
        print("tokens: ",e[2].text)
        print("\nsplit: ", e[2].text.split(" "))
        #print("tags: ",e[3].text)
        #print(e[2].text.split(" "))



