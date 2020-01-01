import re
changed_tags1=dict()
f=open('MSA_POS_Tagger/PosLexicon_Pretraitement/hasDifferent.txt')
for line in f:
    arr=line.split(":")
    tag=re.sub(r' ','',arr[0])
    arr[1]=re.sub(r'\n','',arr[1])
    changed_tags1[tag]=arr[1].split()



def getNewTags(tag):
    try:
        return changed_tags1[tag]
    except KeyError:
        return [tag]


def newTags(s):
    concate=s.split("+")
    if(len(concate)==1):
        return '  '.join(t for t in getNewTags(s))
    if(len(concate)==2):
        tag1=concate[0]
        tag2=concate[1]
        tags=[]
        for t1 in getNewTags(tag1):
            for t2 in getNewTags(tag2):
                tags.append(t1+'+'+t2)

        return '  '.join(t for t in tags)
    if(len(concate)==3):
        tag1=concate[0]
        tag2=concate[1]
        tag3=concate[2]
        tags=[]
        for t1 in getNewTags(tag1):
            for t2 in getNewTags(tag2):
                for t3 in getNewTags(tag3):
                    tags.append(t1+'+'+t2+'+'+t3)
        return '  '.join(t for t in tags)
    if(len(concate)==4):
        tag1=concate[0]
        tag2=concate[1]
        tag3=concate[2]
        tag4=concate[3]
        tags=[]
        for t1 in getNewTags(tag1):
            for t2 in getNewTags(tag2):
                for t3 in getNewTags(tag3):
                    for t4 in getNewTags(tag4):
                        tags.append(t1+'+'+t2+'+'+t3+'+'+t4)
        return '  '.join(t for t in tags)
                
    
    


new_pos_lexicon=open("MSA_POS_Tagger/PosLexicon_Pretraitement/PosLexicon_new.txt","w")
pos=open('MSA_POS_Tagger/PosLexicon_Pretraitement/POSLexicon.txt', encoding='windows-1256')

for line in pos:
    splitted=line.split()
    
    if(len(splitted)>1):
        word=splitted[0]
        tags=splitted[1:]
        new_line=word+'  '
        for t in tags:
            new_line=new_line+' '+newTags(t)
        new_pos_lexicon.write(new_line+'\n')
      
        #break
print('ok')