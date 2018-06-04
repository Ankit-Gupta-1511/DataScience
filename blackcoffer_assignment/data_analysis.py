import pandas as pd
import re
import nltk
import spacy
from textstat.textstat import textstatistics, easy_word_set, legacy_round


"""
create Dictionaries from master
"""
def createDictionaries(master):
	positive = []
	negative = []
	uncertainty = []
	constraining = []
	complex_words = []
	
	for i,w in master.iterrows():
		if w['Positive']>0:
			positive.append(w["Word"])
		elif w['Negative']>0:
			negative.append(w["Word"])
		elif w['Constraining']>0:
			constraining.append(w["Word"])
		elif w['Uncertainty']>0:
			uncertainty.append(w["Word"])	
		elif w['Syllables']>2:
			complex_words.append(w["Word"])

	return positive,negative, uncertainty, constraining, complex_words
"""
cleanData removes the stopwords from the data
"""
# def cleanWords(data, stopwords):
# 	word_tokens = nltk.tokenize.word_tokenize(data)
# 	print(word_tokens)
# 	filtered_data = [w for w in word_tokens if not w in stopwords]
# 	return filtered_data

"""
returnCount function returns the count of the type of words present in dictionary
"""	
def returnCount(tokens, dictionary):
	count = 0
	for w in tokens:
		if w.upper() in dictionary:
			count = count + 1
	return count

def wordCount(text, stopwords):	
	"""
	This regex removes punctuation marks 
	"""
	tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(text)
	#removing stopwords from the list
	words = [w for w in tokens if w not in stopwords]
	return len(words), words

def dataAnalyzer(data, query_type):

	"""
	Loading dictionaries
	"""
	master = pd.read_csv("dictionaries/master.csv")
	# creating dictionaries out of master
	stopwords = pd.read_csv("dictionaries/stopwords.csv")

	negative, positive, uncertainty, constraining, complex_words = createDictionaries(master)

	# removing the stopwords from the data and providing the tokenized data
	word_count, tokenized_clean_data = wordCount(data, stopwords)

	"""
	Analysis
	"""
	total_number_of_words = len(tokenized_clean_data)
	total_number_of_sentences = len(nltk.tokenize.sent_tokenize(data))

	negative_score = returnCount(tokenized_clean_data, negative)
	positive_score = returnCount(tokenized_clean_data, positive)
	uncertainty_score = returnCount(tokenized_clean_data, uncertainty)
	constraining_score = returnCount(tokenized_clean_data, constraining)

	polarity_score = ((positive_score) - (negative_score)) / ((positive_score + negative_score) + 0.000001)
	subjectivity_score = (positive_score + negative_score) / ((total_number_of_words) + 0.000001)

	average_sentence_length = total_number_of_words / total_number_of_sentences
	
	total_number_of_complex_words = returnCount(tokenized_clean_data, complex_words)
	percentage_of_complex_words = total_number_of_complex_words / total_number_of_words 
	fog_index = 0.4 * (average_sentence_length + percentage_of_complex_words)

	

	positive_word_proportion = positive_score / word_count
	negative_word_proportion = negative_score / word_count
	uncertainty_word_proportion = uncertainty_score / word_count
	constraining_word_proportion = constraining_score / word_count
	

	result = {
		"positive_score" : positive_score,
	    "negative_score" : negative_score,
	    "polarity_score" : polarity_score,
	    "average_sentence_length" : average_sentence_length,
	    "percentage_of_complex_words" : percentage_of_complex_words,
	    "fog_index" : fog_index,
	    "complex_word_count" : total_number_of_complex_words,
	    "word_count" : word_count,
	    "uncertainty_score" : uncertainty_score,
	    "constraining_score" : constraining_score,
 	    "positive_word_proportion" : positive_word_proportion,
	    "negative_word_proportion" : negative_word_proportion,
	    "uncertainty_word_proportion" : uncertainty_word_proportion,
	    "constraining_word_proportion" : constraining_word_proportion
	}

	return result