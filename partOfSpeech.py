def partOfSpeech(pos):
	if pos == 'NN' or pos == 'NNS' or pos == 'NNP' or pos == 'NNPS':
		pos = 'N'
	elif pos == 'JJ' or pos == 'JJR' or pos == 'JJS':
		pos = 'A'
	elif pos == 'VB' or pos ==  'VBD' or pos == 'VBG' or pos == 'VBN' or pos ==  'VBP' or pos ==   'VBZ':
		pos = 'V'
	elif pos == 'RB'or pos ==  'RBR' or pos ==  'RBS':
		pos = 'R'
	return pos