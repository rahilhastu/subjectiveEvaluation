from nltk.corpus import stopwords           
import math
import string

def freq(word, dict_k):#finds freq of a word in a sentence
    return dict_k[word]

    
def tf(freq, doc):#finds the normalised freq of a word in a sentence 
    count=0
    docc=doc.split()
    #print docc
    stpwds=stopwords.words("english")+list(string.punctuation)
    
    for item in docc:
        if item not in stpwds:
    #		print item
    		count+=1
    #print "****"
    #print count
    ans= freq/float(count)
    
    return ans    

def idf(allDocuments,word):

    numDocumentsWithThisTerm = 0
    for doc1 in allDocuments:
        doc1= doc1.split()
        #print doc1
        for term in doc1:
            if term==word:
                numDocumentsWithThisTerm = numDocumentsWithThisTerm + 1
                break
    if numDocumentsWithThisTerm > 0:
    	#print "idf:",1+math.log(len(allDocuments)/float(numDocumentsWithThisTerm),10)
        return 1+math.log(len(allDocuments)/float(numDocumentsWithThisTerm),10)	
    else:
        return 0
