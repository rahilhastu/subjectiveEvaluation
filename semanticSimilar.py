from PyDictionary import PyDictionary

dictionary=PyDictionary()

def semanticSimilarity(word,content):
	
	answer = dictionary.synonym(word)
        if answer == [] or answer == None:
            return word
	else:
            if word not in answer:
                answer.append(word)
		
        return answer