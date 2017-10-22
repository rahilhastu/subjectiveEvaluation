import nltk
from nltk.corpus import stopwords           
from nltk.tokenize import word_tokenize 
from collections import Counter
import re
import sqlite3
import math
import string
from itertools import chain
import semanticSimilar
import calculationFile as cf
import partOfSpeech

def com():
    sent1 = open('answers.txt', 'rb').readlines()#creates a list in which each element is one line of the file
    con = sqlite3.connect('table_new1.db') #connection to connect to database
    con.text_factory = str
    cur = con.cursor() #variable to execute statements 
    cur.execute('DROP TABLE IF EXISTS OriginalAnswers;') #Deletes any other existing table of the same name to avoid overwriting of tables

    cur.execute('CREATE TABLE OriginalAnswers(Words TEXT , Q_Num INT , Ans_Num INT UNSIGNED , POS TEXT DEFAULT NULL, Freq INT ,NormalisedTf INT,IDft FLOAT,TfIdf FLOAT, Similar STRING);') #creates table with given coloumns
    sent = []
    
    con2 = sqlite3.connect('table_new3.db')
    cur2 = con2.cursor()
    cur2.execute('CREATE TABLE if not EXISTS pydict(words TEXT , posspeech TEXT , similar STRING);')

    cur2.execute("SELECT words,posspeech,similar from pydict")
    already_similar = cur2.fetchall()
    # print already_similar
    for i in xrange(int(sent1[-1][0])):
        sent.append([])
    i=1
    with open('answers.txt') as f:   #opens the file in ''
        content = f.readline()      #reading the first line of the text file
        while content:  #reads every line in the file 
            content = content.lower()
            qNo = int(content[0])
            
            for s in xrange(len(sent1)):
                if int(sent1[s][0])==qNo and sent1[s] not in sent[qNo-1]:
                    sent[qNo-1].append(sent1[s])
            # print len(sent[qNo-1])
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
                        pos = partOfSpeech.partOfSpeech(a[x][1])
                        filtered_sentence.append(w) #tokenized stop word free list
                        flag=0
                        if already_similar:
                            for row in xrange(len(already_similar)):
                                if w == already_similar[row][0] and pos == already_similar[row][1]:
                                    similarr=already_similar[row][2] 
                                    flag=1
                                    break
                            if flag==0:                                
                                similar = semanticSimilar.semanticSimilarity(w,content)
                                similarr= ' , '.join(similar)
                                cur2.execute('INSERT INTO pydict(words ,posspeech ,similar) VALUES (?,?,?);',(w,pos,similarr))
                                break
                            # print '------'
                            cur.execute('INSERT INTO OriginalAnswers(Words , Q_Num , Ans_Num , POS , Freq,Similar) VALUES (?,?,?,?,?,?);',(w,qNo,i,pos,k[w],similarr))
                        else:
                            similar = semanticSimilar.semanticSimilarity(w,content)
                            similarr= ' , '.join(similar)
                            cur2.execute('INSERT INTO pydict(words ,posspeech ,similar) VALUES (?,?,?);',(w,pos,similarr))
                            # print '------------'
                            cur.execute('INSERT INTO OriginalAnswers(Words , Q_Num , Ans_Num , POS , Freq,Similar) VALUES (?,?,?,?,?,?);',(w,qNo,i,pos,k[w],similarr))

                        fre=c=tff=idff=t=cs=0
                        cur.execute('select Similar from OriginalAnswers where Words=?;',(w,))
                        
                        synonyms=list(cur.fetchall()[-1])
                        # print synonyms
                        listt=synonyms[0].split(' , ')
                        
                        '''for syn in listt:
                            if (syn in content_as_a_list )and (w!=syn):
                                k[w]+=content_as_a_list.count(syn)
                        '''
                        fre=cf.freq(w,k)
                           
                        tff=cf.tf(fre,content)
                        idff=cf.idf(sent[qNo-1],w)
                        t=tff*idff
                        
                        cur.execute('UPDATE OriginalAnswers SET Freq=?,NormalisedTf=?,IDft=?,TfIdf=? where Words=? and Ans_Num=?;',(fre,tff,idff,t,w,i))
                    
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
            con2.commit()
    print '**'
    data = cur.fetchall()
    data2 = cur2.fetchall()
    con.close()     
    con2.close()
    # ------------------------------------------------------------------------------------#