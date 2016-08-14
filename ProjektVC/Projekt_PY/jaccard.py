# -*- coding: utf-8 -*-
text_correct = "textc.txt"
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
text_mistakes = "textm.txt"

with open('textc.txt', 'r') as myfile:
    data_correct=myfile.read().replace('\n', '')
with open('textm.txt', 'r') as myfile:
    data_mistakes=myfile.read().replace('\n', '')
with open('textj.txt', 'r') as myfile:
    data_jaccard=myfile.read().replace('\n', '')
with open('lex.txt', 'r') as myfile:
    data_lex=myfile.read().replace('\n', '')

def remove_punctation(raw_string):
	no_punct = ""
	for char in raw_string:
	   if char not in punctuations:
		   no_punct = no_punct + char
	return no_punct

data_mistakes_np= remove_punctation(data_mistakes)

def remove_punctation(raw_string):
	no_punct = ""
	for char in raw_string:
	   if char not in punctuations:
		   no_punct = no_punct + char
	return no_punct

def ngram_splitter(inputg):# Zerteilt Woerter in Trigramme (ist verstellbar in jegliche Laenge)
	ngram_list = []
	i = 0
	inputg = "**" + inputg + "**"
	while i <= len(inputg)-3:
		zipped = inputg[i]+ inputg[i+1] + inputg[i+2]
		#print zipped
		ngram_list.append(zipped)
		#print ngram_list
		i =i+1
#	print ngram_list
	return ngram_list
	
#print  ngram_splitter("halo")

def matches_out(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    # set3 contains all items comon to set1 and set2
    set3 = set1.intersection(set2)
    #return matches
    found = []
    for match in set3:
        found.append(match)
    return found
    
#print matches_out(ngram_splitter("hallo"), ngram_splitter("hollo"))


testdaten = "hose haus hang huegel haufen habba higs banana hubb bling"
testliste = testdaten.split()

def correction_jaccard(lexicon, w_word):
	matchcounter = 0
	match = ""
	for word in lexicon:
		if len(matches_out(ngram_splitter(w_word), ngram_splitter(word))) > matchcounter:
			matchcounter = len(matches_out(ngram_splitter(w_word), ngram_splitter(word)))
			match = word
		elif len(matches_out(ngram_splitter(w_word), ngram_splitter(word))) == matchcounter:
			matchcounter = len(matches_out(ngram_splitter(w_word), ngram_splitter(word)))
			match = match + " und " + word

#	print "das Wort:" + match + " ist dem Wort:" + w_word + " am aehnlichsten"
	return match

#print correction_jaccard(testliste, "haus")

def make_correction_jaccard(wrong_text, lexicon):
	
	wrong_text_list = remove_punctation(wrong_text).split()
	lexicon_list = lexicon.split()
	for word in wrong_text_list:
		word_correct = False
		for lex_ent in lexicon_list:
			if word == lex_ent:
#				print word + " und " + lex_ent + " sind gleich!"
				word_correct = True
		if word_correct == False:
			print "das Wort:" + correction_jaccard(lexicon.split(), word) + " ist dem Wort:" + word + " am aehnlichsten"

#print data_mistakes.split()		
#print data_lex.split()	
make_correction_jaccard(data_mistakes, data_lex)
#print correction_jaccard( data_lex.split(), "cots")
#print correction_jaccard(testliste, "buddeln") + " aehneln buddeln am meisten"
 
