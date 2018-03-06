import pandas
import numpy.matlib
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import math

context=['username', 'ssn', 'password', 'email', 'name', 'city', 'dob', 'weather']
context_flag_score=[3,5,5,3,3,4,5,1]

sentences=['What is your name?', 
			'What is your username?',
			'What is your last password?',
			'What is your email?',
			'What is your middle name?',
			'Where do you live?',
			'Which city do you live in?',
			'What is your dob?',
			'What is your age?',
			'How are you doing?',
			'Thank you.',
			'Tell me your ssn?',
			'Would you like me to reset your password?',
			'Can you tell me your username?',
			'No problem! I can reset it for you.',
			'How do you spell your last name?',
			'Which city were you born in?',
			'Tell me your last password.',
			'Could you tell me your dob?'
			'How is the weather today?',
			]
			

english_stopwords=stopwords.words('english')

words=[]
tokenizer=RegexpTokenizer('[\w]+')
for sentence in sentences:
	tokenized_words=tokenizer.tokenize(sentence)
	for word in tokenized_words:
		word=word.lower()
		if word not in english_stopwords and word not in words:
			words.append(word)

print words

df=pandas.DataFrame(numpy.matlib.zeros((len(words),len(context))),columns=context, index=words)

print df

for word in words:
	for sentence in sentences:
		if word in tokenizer.tokenize(sentence.lower()):
			for context_word in context:
				if context_word.lower() in sentence:
					df.at[word,context_word]+=1
print df

#Calculate Probabilities
total_count=0.0
for i in range(len(words)):
	for j in range(len(context)):
		print words[i]
		print context[j]
		print df.at[words[i],context[j]]
		print df.iloc[0,0]
		total_count+=df.iloc[i,j]
#print "Total_count: ", total_count

P_words={}
for i in range(len(words)):
	P_w=0
	for j in range(len(context)):
		P_w+=df.iloc[i,j]
	P_w=P_w/total_count
	P_words[words[i]]=P_w
#print "Probability of words: ", P_words
	
P_context=[]
for j in range(len(context)):
	P_c=0
	for i in range(len(words)):
		P_c+=df.iloc[i,j]
	P_c=P_c/total_count
	P_context.append(P_c)
#print "Probability of context: ", P_context 


#Calculate the Pointwise Mutual Information for each word,context in the co-occurrence matrix
pmi_matrix=pandas.DataFrame(numpy.matlib.zeros((len(words),len(context))),columns=context, index=words)

for i in range(len(words)):
	for j in range(len(context)):
		P_w_c=df.iloc[i,j]/total_count
		#print P_w_c
		P_w=P_words[words[i]]
		#print P_w
		P_c=P_context[j]
		#print P_c
		prob=P_w_c/(P_w*P_c)
		#print "prob", prob
		
		if P_w_c:
		
			pmi_matrix.iloc[i,j]=math.log(prob,2)
		else:
			pmi_matrix.iloc[i,j]=0
print pmi_matrix

statement= ''
total_score=0.0
count_conversations=0
print "I forgot my password."
while statement.lower() !='exit':
	statement= raw_input("Enter statement: ")
	tokenized_words=tokenizer.tokenize(statement)
	parsed_input=[]
	for word in tokenized_words:
		if word not in english_stopwords:
			parsed_input.append(word)
			
	#Find context of this statement
	context_probability_for_word=0.0
	context_of_word=None
	context_of_statement={}
	for word in parsed_input:
		if word in words:
			for context_word in context:
				P_w_c=pmi_matrix.at[word,context_word]
				P_w=P_words[word]
				#print "numerator", P_w_c
				#print "denominator", P_w
				context_probability=P_w_c/P_w
				#print context_probability
				if context_probability>context_probability_for_word:
					context_probability_for_word=context_probability
					context_of_word=context_word
			context_of_statement[context_of_word]=context_probability_for_word
	
	#print "C",context_of_statement
	final_context_for_statement=sorted(context_of_statement.items(), key=lambda x: -x[1])
	if final_context_for_statement:
		final_context_for_statement=final_context_for_statement[0][0]
	if final_context_for_statement:
		print "Context: ",final_context_for_statement
	
		#Total Score
		i=0
		while i<len(context) and context[i]!=final_context_for_statement:
			i+=1
		total_score+=context_flag_score[i]
		count_conversations+=1
	else:
		count_conversations+=1
	
	

print "Your score on a scale 0-5 (5 highest) is: ",total_score/count_conversations

