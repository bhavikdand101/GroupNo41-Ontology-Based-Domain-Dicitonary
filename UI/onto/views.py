import re
import nltk
import io
import math
import operator
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, ne_chunk
from nltk.tree import Tree
import json

import string
from owlready2 import *
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re


def remove_html_markup(s):
	tag = False
	quote = False
	out = ""

	for c in s:
		if c == '<' and not quote:
			tag = True
		elif c == '>' and not quote:
			tag = False
		elif (c == '"' or c == "'") and tag:
			quote = not quote
		elif not tag:
			out = out + c

	return out


def getTitle(url):
	try:
		html = urlopen(url)
	except HTTPError as e:
		return None
	try:
		bsObj = BeautifulSoup(html.read(), "lxml")
		title = bsObj.body.h1
	except AttributeError as e:
		return None
	return title


def getData(url):
	data = ""
	try:
		html = urlopen(url)
	except HTTPError as e:
		return None
	try:
		i = 1;
		soup = BeautifulSoup(html, 'lxml')
		for p in soup.find_all('p'):
			if (i < 30):
				data = data + p.text
				i = i + 1
			else:
				break
	except AttributeError as e:
		return None
	return data


##url = "https://www.wvnews.com/fairmontnews/news/marion-county-public-library-expands-digital-technological-reach/article_1ba36a28-9862-5700-aa86-38a522c3ef7a.html"

def afterGettingURL(url):
	title = getTitle(url)
	data = getData(url)

	if title == None:
		t = "Title could not be found"
	else:
		title = remove_html_markup(str(title))
		title = re.sub("^\s+|\s+$", "", title, flags=re.UNICODE)
		#print("\nTitle of the WebPage is: \n")
		#print(title)
	#print("\nScraped Data from the given URL:\n")
	#print(data)
	return data


# url = "http://www.thewestonmercury.co.uk/news/weston-super-mare-old-library-in-the-boulevard-to-be-sold-at-auction-1-5432928"
# url = "http://www.vnews.com/Man-Pleads-Guilty-Is-Sentenced-in-Kilton-Library-Sex-Assault-Lebanon-NH-16148267"
#url = "https://en.wikipedia.org/wiki/Library"


# Functions for Frequency, Total Word Count, Entropy

def getEntropy(word_freq, total_word_count):
	entropy = {}
	threshold = 0
	i = 0
	for word, freq in word_freq.items():
		temp = freq / total_word_count
		entropy[word] = -(temp) * (math.log2(temp))
		threshold += entropy[word]
		i += 1
	# print ('the current threshold is '+ str(threshold))
	threshold = threshold / i

	return entropy


def getFrequency(str):
	wordcount = {}
	i = 0
	for word in str.split():
		if word not in wordcount:
			wordcount[word] = 1.0
		else:
			wordcount[word] += 1.0
	return wordcount


def getWeightDueToIndex(sentences, words):  # returns w2
	sTotal = len(sentences)
	weightDueToIndex = {}
	for word in words:
		if word not in weightDueToIndex:
			i = 0
			for sentence in sentences:
				if word in sentence:
					weightDueToIndex[word] = (sTotal + 1) / (i + 1)
					break
				i = i + 1
	return weightDueToIndex


def getThreshold(w1):
	thresh = 0
	i = 0
	for word in w1:
		thresh += w1[word]
		i += 1
	# print ('the current threshold is '+ str(w1[word]))
	thresh = thresh / i
	# thresh = 0.003

	return thresh


def get_continuous_chunks(text, label):
	chunked = ne_chunk(pos_tag(word_tokenize(text)))
	prev = None
	continuous_chunk = []
	current_chunk = []

	for subtree in chunked:
		if type(subtree) == Tree and subtree.label() == label:
			current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
		elif current_chunk:
			named_entity = " ".join(current_chunk)
			if named_entity not in continuous_chunk:
				continuous_chunk.append(named_entity)
				current_chunk = []
		else:
			continue

	return continuous_chunk


def formDictionary(list, label):
	entity = {}
	for i in list:
		entity[i] = label
	return entity

def index(request):
	template = loader.get_template("onto/index.html")
	context = {'yo':'yo'}
	string = 'sddfs f sdfs dfd sdf df s'
	words = word_tokenize(string)
	return HttpResponse(template.render(context, request))

def process(request):
	text = request.POST.get('text', '')
	url = request.POST.get('url')
	if url!=None and len(url)!=0:
		text = afterGettingURL(url)

	template = loader.get_template("onto/keywords.html")
	###new ontology
	onto = get_ontology("file:///C:/Users/Bhavik/Desktop/BE Project/libraryonto.owl")

	genres = ['fiction', 'nonfiction', 'thriller', 'mythology', 'adventure', 'classic', 'comic', 'fable', 'folklore',
			  'history', 'geography', 'legend', 'fantasy', 'civic', 'mystery', 'mathematics', 'novel', 'saga',
			  'science', 'tragedy', 'poetry', 'religion', 'abstract', 'agriculture', 'anthropology', 'architecture',
			  'art', 'astronomy', 'biology', 'business', 'chemistry', 'communication', 'economic', 'engineering',
			  'fashion', 'law', 'film', 'food', 'geography', 'geology', 'history', 'math', 'medicine', 'music',
			  'physics', 'psychology', 'health', 'nutrition', 'philosophy', 'sociology', 'statictic', 'textile',
			  'theatre', 'cookery', 'genealogy', 'technical', 'computer', 'fanfiction', 'illustration', 'storybook',
			  'textbook']

	with onto:
		class library(Thing):
			pass

		class institute(Thing):
			pass

		class book(Thing):
			pass

		class librarian(Thing):
			pass

		class information(Thing):
			pass

		class volume(Thing):
			pass

		class newspaper(Thing):
			pass

		class shelf(Thing):
			pass

		class overdue(Thing):
			pass

		class knowledge(Thing):
			pass

		class education(Thing):
			pass

		class collection(Thing):
			pass

		class material(Thing):
			pass

		class college(Thing):
			pass

		class school(Thing):
			pass

		class literature(Thing):
			pass

		class biography(Thing):
			pass

		class autobiography(Thing):
			pass

		class journal(Thing):
			pass

		class reference(Thing):
			pass

		class textbook(Thing):
			pass

		class student(Thing):
			pass

		class child(Thing):
			pass

		class children(Thing):
			pass

		class literary(Thing):
			pass

		class manuscript(Thing):
			pass

		class bibliography(Thing):
			pass

		class citation(Thing):
			pass

		class database(Thing):
			pass

		class demography(Thing):
			pass

		class magazine(Thing):
			pass

		class management(Thing):
			pass

		class renewal(Thing):
			pass

		class academy(Thing):
			pass

		class archive(Thing):
			pass

		class author(Thing):
			pass

		class bibliomania(Thing):
			pass

		class bibliophilia(Thing):
			pass

		class bookable(Thing):
			pass

		class bookcase(Thing):
			pass

		class bookhound(Thing):
			pass

		class booklover(Thing):
			pass

		class bookrack(Thing):
			pass

		class bookseller(Thing):
			pass

		class bestseller(Thing):
			pass

		class bookshelf(Thing):
			pass

		class bookstand(Thing):
			pass

		class club(Thing):
			pass

		class compilation(Thing):
			pass

		class hardcover(Thing):
			pass

		class newsletter(Thing):
			pass

		class paperback(Thing):
			pass

		class page(Thing):
			pass

		class profession(Thing):
			pass

		class professional(Thing):
			pass

		class publication(Thing):
			pass

		class repository(Thing):
			pass

		class storage(Thing):
			pass

		class paper(Thing):
			pass

		class texts(Thing):
			pass

		class catalogue(Thing):
			pass

		class public(Thing):
			pass

		class literate(Thing):
			pass

		class building(Thing):
			pass

		class traditional(Thing):
			pass

		class room(Thing):
			pass

		class scroll(Thing):
			pass

		class large(Thing):
			pass

		class curriculum(Thing):
			pass

		class scholar(Thing):
			pass

		class staff(Thing):
			pass

		class subject(Thing):
			pass

		class picture(Thing):
			pass

		class manual(Thing):
			pass

		class report(Thing):
			pass

		class campus(Thing):
			pass

		class barcode(Thing):
			pass

		class computer(Thing):
			pass

		class DVD(Thing):
			pass

		class design(Thing):
			pass

		class dictionary(Thing):
			pass

		class directory(Thing):
			pass

		class employment(Thing):
			pass

		class encyclopedia(Thing):
			pass

		class environment(Thing):
			pass

		class event(Thing):
			pass

		class field(Thing):
			pass

		class fines(Thing):
			pass

		class folio(Thing):
			pass

		class government(Thing):
			pass

		class headings(Thing):
			pass

		class holdings(Thing):
			pass

		class human(Thing):
			pass

		class image(Thing):
			pass

		class index(Thing):
			pass

		class internet(Thing):
			pass

		class keyword(Thing):
			pass

		class labor(Thing):
			pass

		class language(Thing):
			pass

		class linguistic(Thing):
			pass

		class number(Thing):
			pass

		class media(Thing):
			pass

		class policy(Thing):
			pass

		class population(Thing):
			pass

		class primary(Thing):
			pass

		class program(Thing):
			pass

		class publisher(Thing):
			pass

		class periodic(Thing):
			pass

		class period(Thing):
			pass

		class theory(Thing):
			pass

		class thesaurus(Thing):
			pass

		class web(Thing):
			pass

		class copyright(Thing):
			pass

		class course(Thing):
			pass

		class depot(Thing):
			pass

		class ebook(Thing):
			pass

		class edition(Thing):
			pass

		class factbook(Thing):
			pass

		class foundation(Thing):
			pass

		class genre(Thing):
			pass
	for i in genres:
		i = genre(i)

	with onto:
		class issue(student >> book):
			pass

		class returns(student >> book):
			pass

		class fine(student >> book):
			pass

		class work(student >> book):
			pass

		class read(student >> book):
			pass

		class write(student >> book):
			pass

		class learn(student >> book):
			pass

		class understand(student >> book):
			pass

		class study(student >> book):
			pass

		class record(student >> book):
			pass

		class bookkeep(student >> book):
			pass

		class educate(student >> book):
			pass

		class open(student >> book):
			pass

		class consult(student >> book):
			pass

		class access(student >> book):
			pass

		class refer(student >> book):
			pass

		class texts(student >> book):
			pass

		class preserve(student >> book):
			pass

		class acquisition(student >> book):
			pass

		class accession(student >> book):
			pass

		class current(student >> book):
			pass

		class entry(student >> book):
			pass

		class publish(student >> book):
			pass

		class reserve(student >> book):
			pass

		class operation(student >> book):
			pass

		class resource(student >> book):
			pass

		class search(student >> book):
			pass

		class serial(student >> book):
			pass

		class space(student >> book):
			pass

		class stack(student >> book):
			pass

		class stream(student >> book):
			pass

		class circulate(student >> book):
			pass

		class imprint(student >> book):
			pass

		class lend(student >> book):
			pass

		class overdue(student >> book):
			pass

		class register(student >> book):
			pass

		class reissue(student >> book):
			pass
	cls = list(onto.classes())



	# print("I am main text")
	# print(text)
	# with open("test.txt",'r') as f:

	text_clean = re.sub(r'(?:(?:http|https):\/\/)?([-a-zA-Z0-9.]{2,256}\.[a-z]{2,4})\b(?:\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?',"", text, flags=re.MULTILINE)
	text_clean = '\n'.join([a for a in text.split("\n") if a.strip()])

	# print("I am clean text")
	# print(text_clean)

	# Convert all to lowercase

	cleanLower = ""
	for line in text_clean:
		line = line.lower()
		cleanLower += line

	# print("I am lowercase text")
	# print(cleanLower)


	# word_tokenize accepts a string as an input, not a file.


	stop_words = set(stopwords.words('english'))

	# file1 = open('cleanLower.txt')
	# line = file1.read()
	words = cleanLower.split()
	appendFile = ""
	for r in words:
		if r not in stop_words:
			var = " " + r
			appendFile += var
	# print(appendFile)

	# Tokenization + Lemmatisation

	# file_content = open("filteredtext.txt",'r').read()
	file_content = appendFile
	file_content = re.sub(r'\'', "", file_content, flags=re.MULTILINE)
	file_content = re.sub(r'\’', "", file_content, flags=re.MULTILINE)
	# print("######################################")
	# print(file_content)
	tokens = nltk.word_tokenize(file_content)

	# tokenOutput = open('data.txt' , 'w')
	tokenOutput = []
	# lemmaOutput = open('lemma.txt' , 'w')
	lemmaOutput = []
	lemmatizer = WordNetLemmatizer()
	lemmaInput = ""
	for i in tokens:
		lemmaOutput.append(lemmatizer.lemmatize(i))
		tokenOutput.append(i)

	for i in lemmaOutput:
		t = " " + i
		lemmaInput += t
	# print(lemmaInput)

	# Start processing for entropy

	# lemmaInput = open('lemma.txt' , 'r')
	example_sentence = lemmaInput

	# remove punctuation

	# example_sentence = re.sub(r'[^\w\s]','',example_sentence)


	# word tokenize to get total number of words

	words = word_tokenize(example_sentence)
	# print(words)
	total_word_count = len(words)

	###########################     W1       ########################################


	# Get occurrence frequency of words

	word_freq = getFrequency(example_sentence)

	# Get Entropy
	threshold = 0
	entropy = getEntropy(word_freq, total_word_count)

	###########################     W2       ########################################

	sentences = sent_tokenize(example_sentence)
	##for i in sentences:
	##        print("\n\n\n")
	##        print(i)

	weightDueToIndex = getWeightDueToIndex(sentences, words)

	#############################     W3       ########################################

	# len1= sent_tokenize(example_sentence)
	len1 = sentences
	w3 = {}
	# words = []

	# len1 = sent_tokenize(str1)
	candidate = words

	for key in range(len(candidate)):
		# print(candidate[key])
		# print("###################")
		ls = []
		ik = []
		pk = []
		s = 0

		for i in range(len(len1)):
			len1[i] = re.sub(r'[^\w\s]', '', len1[i])
			words = len1[i].split()
			# print(words)
			for j, word in enumerate(words):
				if candidate[key] == word:
					ls.append(len(words))
					ik.append(j + 1)
					break

		# print("Index list")
		# print(ik)
		# print("length of sentence list")
		# print(ls)
		for j in range(len(ik)):
			if ik[j] < (ls[j] / 2):
				pk.append(ik[j])
			else:
				pk.append(2 * (ls[j] - ik[j]))
		# print("PK weight")

		# print(pk)
		for m in range(len(ls)):
			# print(s)
			s = s + ((ls[m] + 1) / (pk[m] + 1))
		# print(s)

		# print("sum of index weight")
		# print(s)
		if (s == 0):
			w3[candidate[key]] = 0
		else:
			w3[candidate[key]] = math.log(s, 2)

	##
	##print("W1")
	##print(entropy)
	##print("W2")
	##print(weightDueToIndex)
	##print("W3")
	##print(w3)

	weight = {}
	for (k, v), (k2, v2) in zip(weightDueToIndex.items(), entropy.items()):
		if (k == k2):
			weight[k] = weightDueToIndex[k] * entropy[k2]

	for (k, v), (k2, v2) in zip(weight.items(), w3.items()):
		if (k == k2):
			weight[k] = weight[k] * w3[k2]

	##print("Total weight")
	##print(weight)


	shortlist = {}
	threshold = getThreshold(weight)

	sorted_x = sorted(weight.items(), key=operator.itemgetter(1))
	for word, weight in sorted_x:
		if (weight >= threshold):
			shortlist[word] = weight

	# print ('Final threshold is '+ str(threshold)+"\n\n")

	######################@@@@@@@@@@@@@@@@@@@@@@  Display Threshold


	# print(shortlist)
	# print("Shortlisted words on the basis of all weights are :\n\n")

	sorted_shortlist = sorted(shortlist.items(), key=operator.itemgetter(1))

	# print(sorted_shortlist)

	# for k,v in sorted_shortlist:
	#       print(str(k)+ ": "+str(v))
	# print("\n")


	#################### Integration of Mapping.py ##################

	lst2 = []
	score = {}



	class_list = list(onto.classes())
	individual_list = list(onto.individuals())
	properties_list = list(onto.properties())
	lst = class_list + individual_list + properties_list

	for i in range(len(lst)):
		str1 = str(lst[i])
		str1 = str1.lower()
		str1 = str1.replace('library.', '')
		lst2.append(str1)

	# print(lst2)
	# str2=str(candidates)
	# print(lst2)


	#############  appending only those candidates to score which exist in the ontology
	for i, val in shortlist.items():
		for j in lst2:
			if i in j:
				score[i] = val

	# print("\nFinal score:\n")

	# print(score)

	# print("\n\nShortlisted words after mapping :\n")
	##
	##for k in score:
	##        print(k)


	##############@@@@@@@@@@@@@@@@@@@@      diplay keyword with weightage from "score"

	################################# PERCENTAGES ######################################
	score_list = list(sorted(score.values()))
	# print(score_list)
	number = sum(num for num in score_list)
	# print (number)
	percentage = score
	for key in percentage:
		percentage[key] = (percentage[key] / number) * 100

	# print("\n\nRelevance of the keywords to the document :\n")
	# print(percentage)

	#########@@@@@@@@@@@@@@@@@@@@@@@@@@@     display "percentage" using pie chart. Give title as RELEVANCE


	shortlisted_list = list(sorted(shortlist.values()))
	total_number = sum(num for num in shortlisted_list)

	domain_relevance_score = (number * 100) / total_number

	# print (domain_relevance_score)

	##############@@@@@@@@@@@@@@@@@@@@        print the "domain_relevance_score" variable in the following sentence (The given text is 48.44% relevant to the domain)


	############# NER ##############################################
	sent = text
	organization = get_continuous_chunks(sent, 'ORGANIZATION')
	orgDict = formDictionary(organization, 'Organization')

	person = get_continuous_chunks(sent, 'PERSON')
	personDict = formDictionary(person, 'Person')

	location = get_continuous_chunks(sent, 'LOCATION')
	locationDict = formDictionary(location, 'Location')

	gpe = get_continuous_chunks(sent, 'GPE')
	gpeDict = formDictionary(gpe, 'Geo-Political')

	final_dictionary = dict(orgDict)
	final_dictionary.update(personDict)
	final_dictionary.update(locationDict)
	final_dictionary.update(gpeDict)

	# print(final_dictionary)
	################@@@@@@@@@@@@@@@@ this is the named_entity_recgnition dictionary, KEY = word, VALUE = label
	#percentage = {'1':10, '2':20,'3' : 30}
	pie_key = []
	pie_val = []
	for key,val in percentage.items():
		pie_key.append(key)
		pie_val.append(val)
	json_list = json.dumps(pie_key)
	context = {'threshold': threshold, 'score': score, 'pie_key': json_list, 'pie_val': pie_val, 'drs': domain_relevance_score,
			   'ner': final_dictionary, 'len': len(pie_key)}
	return HttpResponse(template.render(context, request))
