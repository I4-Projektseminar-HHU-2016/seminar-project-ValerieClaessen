# -*- coding: utf-8 -*-
from __future__ import division
from Tkinter import *
import string


root = Tk()
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
words = []
testsatz= "hallo ich bin ein Testsatz"
testliste= testsatz.split()
print testliste
text_correct = "textc.txt"
text_mistakes = "textm.txt"
text_jaccard = "textj.txt"

with open('textc.txt', 'r') as myfile:
    data_correct=myfile.read().replace('\n', '')
with open('textm.txt', 'r') as myfile:
    data_mistakes=myfile.read().replace('\n', '')
with open('textj.txt', 'r') as myfile:
    data_nmatches=myfile.read().replace('\n', '')
with open('lex.txt', 'r') as myfile:
    data_lex=myfile.read().replace('\n', '')
'''
with open('textm.txt') as f:
    datam = f.readlines()
with open('textj.txt') as f:
    dataj = f.readlines()
#for element in data:
#	words.append (element)
'''
def remove_punctation(raw_string):
	no_punct = ""
	for char in raw_string:
	   if char not in punctuations:
		   no_punct = no_punct + char
	return no_punct
	
#print remove_punctation(data_correct)

def text_to_set (text_doc):
	lex_list = remove_punctation(text_doc)
	lex_list = lex_list.split()
	lex_set = set(lex_list)
	return lex_set

		
	

#print text_to_set(data_correct)

def set_to_lex (text_doc):
	new_lex = open("lex.txt", "w")
	text_as_set = text_to_set(data_correct)
	for element in text_as_set:
		new_lex.write(element + " " )
	new_lex.close()

#set_to_lex(text_to_set(data_correct))	

	


def open_lexicon(): #erzeugt GUI um eigene Lexikoneinträge zu schreiben
	root_lex = Tk()
	global lexicon_text
	
	lexicon_text = Text(root_lex, height = 20, width = 40, bg = "white" )
	lexicon_text.pack(padx=10, pady=20, side=LEFT)
	button_do_lex = Button(root_lex, text='Lexikon', width=25, command = save_lexicon) # speichert die neuen Einträge
	button_do_lex.pack(padx=5, pady=5)
	root_lex.mainloop() #Lexikoneditor GUI
	
def save_lexicon(): # Methode um neue Lexikoneinträge in Textdokument zu speichern
	new_lex = lexicon_text.get("1.0", END)
	new_lex_out = open("lex.txt","a")
	new_lex_out.write (new_lex)
	
	new_lex_out.close()

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
	#print ngram_list
	return ngram_list

def matches_out(list1, list2): # zählt die Übereinstimmungen der N-Gramme 
    set1 = set(list1)
    set2 = set(list2)
    # set3 contains all items comon to set1 and set2
    set3 = set1.intersection(set2)
    #return matches
    found = []
    for match in set3:
        found.append(match)
    return found

def correction_nmatches(lexicon, w_word): # führt eine Fehlerkorrektur nach NGram-Ähnlichkeit durch
	matchcounter = 0
	match = ""
	for word in lexicon:# WICHTIG: wenn Wörter sich gleichähnlich sind wird dies im moment noch nicht beachtet
		if len(matches_out(ngram_splitter(w_word), ngram_splitter(word))) > matchcounter:
			matchcounter = len(matches_out(ngram_splitter(w_word), ngram_splitter(word)))
			match = word
		elif len(matches_out(ngram_splitter(w_word), ngram_splitter(word))) == matchcounter:
			matchcounter = len(matches_out(ngram_splitter(w_word), ngram_splitter(word)))
			match = match + " und " + word

#	print "das Wort:" + match + " ist dem Wort:" + w_word + " am ähnlichsten"
	return match
	
def correction_jaccard(lexicon, w_word): # führt eine Fehlerkorrektur nach Jaccard Sneath durch
	matchcounter = 0
	matchj = ""
	for match in lexicon:# WICHTIG: wenn Wörter sich gleichähnlich sind wird dies im moment noch nicht beachtet
		if len(matches_out(ngram_splitter(w_word), ngram_splitter(match)))/(len(ngram_splitter(w_word))+ len(ngram_splitter(match))-len(matches_out(ngram_splitter(w_word), ngram_splitter(match)))) > matchcounter:
			matchcounter = len(matches_out(ngram_splitter(w_word), ngram_splitter(match)))/(len(ngram_splitter(w_word))+ len(ngram_splitter(match))-len(matches_out(ngram_splitter(w_word), ngram_splitter(match))))
			matchj = match
		elif len(matches_out(ngram_splitter(w_word), ngram_splitter(match)))/(len(ngram_splitter(w_word))+ len(ngram_splitter(match))-len(matches_out(ngram_splitter(w_word), ngram_splitter(match)))) == matchcounter:
			matchcounter =len(matches_out(ngram_splitter(w_word), ngram_splitter(match)))/(len(ngram_splitter(w_word))+ len(ngram_splitter(match))-len(matches_out(ngram_splitter(w_word), ngram_splitter(match))))
			matchj = matchj + " und " + match

	print "das Wort:" + matchj + " ist dem Wort:" + w_word + " am ähnlichsten"
	return matchj
'''
def correction_jaccard(w_word, match):
#	jaccard = 0.0
	jaccard= len(matches_out(ngram_splitter(w_word), ngram_splitter(match)))/(len(ngram_splitter(w_word))+ len(ngram_splitter(match))-len(matches_out(ngram_splitter(w_word), ngram_splitter(match))))
	print len(matches_out(ngram_splitter(w_word), ngram_splitter(match)))
	print len(ngram_splitter(w_word))
	print len(ngram_splitter(match))
	return jaccard
'''	
print correction_jaccard(data_lex.split(), "Cots")

def make_correction_nmatches(wrong_text, lexicon):
	
	wrong_text_list = remove_punctation(wrong_text).split()
	lexicon_list = lexicon.split()
	ausgabe = ""
	correction = ""
	for word in wrong_text_list:
		word_correct = False
		for lex_ent in lexicon_list:
			if word == lex_ent:
#				print word + " und " + lex_ent + " sind gleich!"
				word_correct = True
				correction = correction + word + " "
		
		if word_correct == False:
			korrektur =  "das Wort:" + correction_nmatches(lexicon.split(), word) + " ist dem Wort:" + word + " am aehnlichsten" + "\n"
			korrektur2 = correction_nmatches(lexicon.split(), word)
			word = '''word'''
			correction  =  correction + korrektur2 + " "
			ausgabe = ausgabe + korrektur
	'''		
	root_correct = Tk()
	
	correct_text = Text(ausgabe, height = 20, width = 40, bg = "white" )
	correct_text.pack(padx=10, pady=20, side=LEFT)
	root_correct.mainloop() #Lexikoneditor GUI
	'''
	print ausgabe
	return correction
	

def give_correction_nmatches(wrong_text, lexicon):
	
	wrong_text_list = remove_punctation(wrong_text).split()
	lexicon_list = lexicon.split()
	ausgabe = ""
	correction = ""
	for word in wrong_text_list:
		word_correct = False
		for lex_ent in lexicon_list:
			if word == lex_ent:
#				print word + " und " + lex_ent + " sind gleich!"
				word_correct = True
				correction = correction + word + " "
		
		if word_correct == False:
			korrektur =  "das Wort: " + correction_nmatches(lexicon.split(), word) + " ist dem Wort: " + word + " am aehnlichsten" + "\n"
			korrektur2 = correction_nmatches(lexicon.split(), word)
			word = '''word'''
			correction  =  correction + korrektur2 + " "
			ausgabe = ausgabe + korrektur
	return ausgabe



def write_correctionfile(correction_string):
	new_correction = file("correction.txt","a")
	new_correction.write (correction_string)
	new_correction.close()	
	
#write_correctionfile(make_correction_nmatches(data_mistakes, data_lex))

def show_mistakes():
	root_cor = Tk()
	global lexicon_text
	cor_text = Text( root_cor, height = 20, width = 40, bg = "white" )
	cor_text.pack(padx=10, pady=20, side=LEFT)
	cor_text.insert(END, give_correction_nmatches(data_mistakes, data_lex))
	
	root_cor.mainloop() #Lexikoneditor GUI
	





w = Text(root, height = 20, width = 40, bg = "white")
w.pack(padx=10, pady=20, side=LEFT)
w.insert(END,data_mistakes)
w = Text(root, height = 20, width = 40, bg = "white")
w.pack(padx=5, pady=20, side=LEFT)
w.insert (END, make_correction_nmatches(data_mistakes, data_lex)	)
button_lex = Button(root, text='Lexikon', width=25, command=open_lexicon)
button_lex.pack(padx=5, pady=5)
button_graph = Button(root, text='Graph', width=25, command=root.destroy)
button_graph.pack(padx=5, pady=5)
button_check = Button(root, text='Check', width=25, command=show_mistakes)
button_check.pack(padx=5, pady=5)


	
root.mainloop() # Haupt-GUI
