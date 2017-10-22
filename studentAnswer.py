import nltk
from nltk.corpus import stopwords           
from nltk.tokenize import word_tokenize 
from collections import Counter
import re
import sqlite3
import math
import string
from itertools import chain
# import semanticSimilar
import calculationFile as cf
import partOfSpeech

def stu():
    sent1 = open('studentAns.txt', 'rb').readlines()#creates a list in which each element is one line of the file 
    con = sqlite3.connect('table_new2.db') #connection to connect to database
    con.text_factory = str
    curStudent = con.cursor() #variable to execute statements 
    curStudent.execute('DROP TABLE IF EXISTS StudentAnswers;') #Deletes any other existing table of the same name to avoid overwriting of tables
    print sent1
    curStudent.execute('CREATE TABLE StudentAnswers(Words TEXT , Q_Num INT , Line_No INT UNSIGNED , POS TEXT DEFAULT NULL, Freq INT ,NormalisedTf INT,IDft FLOAT,TfIdf FLOAT);') #creates table with given coloumns
    sent = []
    for i in xrange(int(sent1[-1][0])):
        sent.append([])
    i=1
    with open('studentAns.txt') as f:   #opens the file in ''
        content = f.readline()      #reading the first line of the text file
        while content:  #reads every line in the file 
            content = content.lower()
            qNo = int(content[0])
            
            for s in xrange(len(sent1)):
                if int(sent1[s][0])==qNo and sent1[s] not in sent[qNo-1]:
                    sent[qNo-1].append(sent1[s])
            # print sent
            content = content.replace(content[0],'')
            
            stop_words = set(stopwords.words("english")) #setting stop_words set as ENGLISH LANGUAGE.

            words = word_tokenize(content)  #list of tokenized words in the example
            
            filtered_sentence = []
            
            k = dict(Counter(words)) #returns dictionary key:value is of the form word:freq
            a = nltk.pos_tag(words) #returns a tuple of form[(word,pos),(word,pos)]
            x=0
            similar=[]
            content_as_a_list=content.split()
            for w in words:
                if w in stop_words:
                    x += 1
                else:   #removing stop words
                    if w not in filtered_sentence:
                        filtered_sentence.append(w) #tokenized stop word free list
                 
                        pos = partOfSpeech.partOfSpeech(a[x][1])       
                        # pos,similar = semanticSimilar.semanticSimilarity(w,a[x][1],content)

                        # if isinstance(similar,str): #statement for adding word to Similar coloumn where "-"
                        #     similar = similar.split(" ")

                        # similarr= ' , '.join(similar)
                    # print similarr
                        fre=c=tff=idff=t=cs=0
                        curStudent.execute('INSERT INTO StudentAnswers(Words , Q_Num , Line_No , POS , Freq) VALUES (?,?,?,?,?);',(w,qNo,i,pos,k[w]))
                        # curStudent.execute('select Similar from StudentAnswers where Words=?;',(w,))
                        # synonyms=curStudent.fetchall()[-1]
                        # listt=synonyms[0].split(' , ')

                        # for syn in listt:
                        #     if (syn in content_as_a_list )and (w!=syn):
                        #         k[w]+=content_as_a_list.count(syn)

                        fre=cf.freq(w,k)   
                        tff=cf.tf(fre,content)
                        idff=cf.idf(sent[qNo-1],w)
                        t=tff*idff
                        curStudent.execute('UPDATE StudentAnswers SET Freq=?,NormalisedTf=?,IDft=?,TfIdf=? where Words=? and Line_No=?;',(fre,tff,idff,t,w,i))
                    
                        x +=1 
                        count = 1
                        con.commit()                
                    else:
                        x+=1
            
            i += 1  
            count = 1
                    
            content = f.readline() #increments to next line in text file
            print 'contentupdated'
            con.commit()  
    print '**'
    data = curStudent.fetchall()
    con.close()

