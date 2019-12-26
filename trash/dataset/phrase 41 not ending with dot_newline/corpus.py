import xml.etree.ElementTree as et
import xml.dom.minidom as md

from lxml import etree


root = etree.parse("corpus.xml")

for e in root.xpath("/CORPUS/Phrase")[:100]:

    if e[2].text.split(" ")[-1] != ".\n":
        print("num phrase: ",e[0].text)
    #print(e[2].text.split(" "))

    """
    print("text: ",e[1].text)
    print("tokens: ",e[2].text)
    print("tags: ",e[3].text)
    """


