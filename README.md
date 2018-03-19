# ChatBot Interface based on Pointwise Mutual Information

## String preprocessing

1. Remove punctuation/symbols using regular expressions
2. Convert to lowercase
3. Remove stopwords

## Calculate Pointwise Mutual Information

Pointwise Mutual Information is a concept in information theory and statistics where the probability of word 'w' and context 'c' occurring together is given by the following formula:

PMI(w,c) = log (p(w,c)/(p(w)p(c)))

PMI measures the likeliness of w and c to occur together vs if they were to exist independently.

## Compute word to context co-occurrence matrix

1. Context refers to flagging words that might be malicious like asking for PII, for example: password, address, ssn 
2. Co-occurrence matrix is of shape len(words) * len(context_words) where each i,j reflects how many times does context j appear in a window around word i
3. Calculate for each word p(w) 
4. Calculate for each context p(c)
5. Calculate PMI using above formula

## ChatBot Interface

Get an input sentence (S) and check if the chatbot is asking for malicious information (like PII).
1. Preprocess S.
2. For each word (w) in input, check what is the max context word (c) appearing in training set, assign the probability of  context (c) to the word w.
3. Compute score for sentence by taking max probability overall words.
4. Compute total score by averaging over all conversations.



