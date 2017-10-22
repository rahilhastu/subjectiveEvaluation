import math
import sqlite3
import combined
import studentAnswer

def fun():
	# connect = sqlite3.connect('synonym.db')
	# print "Hello"
	# curSynonym = connect.cursor()
	
	
	combined.com()
	studentAnswer.stu()
	
	conq = sqlite3.connect('table_new2.db') #connection to connect to database
	con = sqlite3.connect('table_new1.db')
	curStudent = conq.cursor()
	curOriginal = con.cursor()

	def getContents():
	    curStudent.execute("Select Words,Q_Num,Line_No,POS,TfIdf from StudentAnswers")
	    curOriginal.execute("Select Q_Num,Ans_Num,POS,TfIdf,Similar,Words from OriginalAnswers")
	    words_Student= curStudent.fetchall()
	    words_Original= curOriginal.fetchall()
	    return words_Original,words_Student

	def getInfo(values,selectedWordsTfIdfValue,wordsSelected,studentTfIdfValues):
		questionNumber,answerNum = 0,0
		for studentAns in xrange(len(content_Student)):
			word = content_Student[studentAns][0] #a word from student answer list
			questionNumber = content_Student[studentAns][1]-1
			studentTfIdfValues[questionNumber].append(content_Student[studentAns][4])
			for originalAns in xrange(len(content_Original)):
				if content_Student[studentAns][1]==content_Original[originalAns][0]: #if same question number
						answerNum = content_Original[originalAns][1]-1
						if word in content_Original[originalAns][4] and content_Student[studentAns][3]==content_Original[originalAns][2]: #if pos is same and word is in similar of Original answer
							values[answerNum].append(content_Original[originalAns][3]*content_Student[studentAns][4])
							if content_Original[originalAns][5] not in wordsSelected[content_Original[originalAns][1]-1]:
								wordsSelected[answerNum].append(content_Original[originalAns][5])
								selectedWordsTfIdfValue[answerNum].append(content_Original[originalAns][3])

	content_Original,content_Student = getContents()
	totalAnsInOriginal = content_Original[-1][1]
	totalAnsInStudent = content_Student[-1][1]

	values = []
	wordsSelected = []
	selectedWordsTfIdfValue=[]
	studentTfIdfValues =[]

	for i in xrange(totalAnsInStudent):
		studentTfIdfValues.append([])
	for i in xrange(totalAnsInOriginal):
		values.append([]),wordsSelected.append([]),selectedWordsTfIdfValue.append([])

	getInfo(values,selectedWordsTfIdfValue,wordsSelected,studentTfIdfValues)
	denominator=[]

	for k in xrange(len(studentTfIdfValues)):
		denoTotal=0
		for i in xrange(len(studentTfIdfValues[k])):
			j=studentTfIdfValues[k][i]**2
			denoTotal+=j
		denominator.append(math.sqrt(denoTotal))

	mod=[]
	for k in xrange(len(selectedWordsTfIdfValue)):
		total=0
		for i in xrange(len(selectedWordsTfIdfValue[k])):
			j=selectedWordsTfIdfValue[k][i]**2
			total+=j
		mod.append(math.sqrt(total))

	numerator=[]
	for k in xrange(len(values)):
		ttl=0
		for i in xrange(len(values[k])):
			ttl+=values[k][i]
		numerator.append(ttl)

	j=0
	first= 0
	a=[]
	for i in xrange(len(selectedWordsTfIdfValue)):
		try:
			percentage = (float(numerator[i]/(mod[i]*denominator[first])))*100
			if j==2:
				first+=1		
				j=-1
			a.append(percentage)
			j=j+1
		except:
			if j==2:
				first+=1
				j=-1
			a.append(0)
			j=j+1

	result=[]
	i=0

	while i<len(a):
	  result.append(a[i:i+3])
	  i+=3
	file = open('result.txt','w')
	j,k=0,0
	for j in xrange(len(result)):
		ans=[]
		score=[]
		l=0
		final=0.0
		for k in result[j]:
			if k>=100:
				final=100.0
				break
			elif k>90 and k<100:
				ans.append(k)
			else:
				l+=1
				score.append(k)

		if final==100.0:
			print "your result is:",final
		elif len(ans)>0:
			for i in ans:
				final+=i
			final = final/len(ans)
			print "your result is:",final
		else:
			final = max(score)
			try:
				print "your result is:",final
			except:
				final = 0
				print "your result is: 0"

		file.write("your score for "+str(j+1)+" answer is : " +str(final)+'\n')