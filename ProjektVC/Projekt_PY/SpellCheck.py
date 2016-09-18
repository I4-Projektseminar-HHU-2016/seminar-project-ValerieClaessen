# -*- coding: utf-8 -*-

from __future__ import division
from Tkinter import *
from time import *
import matplotlib.pyplot as plt
from collections import Counter


root = Tk()
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~''' # Satzzeichen/Sonderzeichen die erntfernt werden sollen
words = []

text_correct = "textc.txt"
text_mistakes = "textm.txt"
#text_jaccard = "textj.txt"

with open('textc.txt', 'r') as myfile:
    data_correct=myfile.read().replace('\n', '')
with open('textm.txt', 'r') as myfile:
    data_mistakes=myfile.read().replace('\n', '')
'''
with open('textj.txt', 'r') as myfile:
    data_nmatches=myfile.read().replace('\n', '')
'''
    
#Textdateien werden eingelesen

def remove_punctation(raw_string):
	no_punct = ""
	for char in raw_string:
	   if char not in punctuations:
		   no_punct = no_punct + char
	return no_punct


def text_to_set (text_doc):
	lex_list = remove_punctation(text_doc)
	lex_list = lex_list.split()
	lex_set = set(lex_list)
	return lex_set


def set_to_lex (text_doc):
	new_lex = open("lex.txt", "w")
	text_as_set = text_to_set(data_correct)
	for element in text_as_set:
		new_lex.write(element + " " )
	new_lex.close()

set_to_lex(text_to_set(data_correct))	
with open('lex.txt', 'r') as myfile:
    data_lex=myfile.read().replace('\n', '')
	


def open_lexicon(): #erzeugt GUI um eigene Lexikoneinträge zu schreiben
	root_lex = Tk()
	global lexicon_text
	
	lexicon_text = Text(root_lex, height = 20, width = 40, bg = "white" )
	lexicon_text.pack(padx=10, pady=20, side=LEFT)
	button_do_lex = Button(root_lex, text='Hinzufügen', width=25, command = save_lexicon) # speichert die neuen Einträge
	button_do_lex.pack(padx=10, pady=10)
	lexicon_des = Label (root_lex, text = "Hier können neue Lexikoneinträge \n geschrieben und hinzugefügt werden.", height = 10, width = 40) 	#hier noch um den Zeilenumbruch kümmern!
	lexicon_des.pack(padx=5, pady=5)
	
	root_lex.mainloop() #Lexikoneditor GUI
	
def save_lexicon(): # Methode um neue Lexikoneinträge in Textdokument zu speichern
	new_lex = lexicon_text.get("1.0", END)
	new_lex_out = open("lex.txt","a")
	new_lex_out.write (new_lex + " ")
	
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
			match = match + "/" + word
			
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
			matchj = matchj + "/" + match
	
	return matchj


def words(text): 
	return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('lex.txt').read()))


def P(word, N=sum(WORDS.values())): 
	#Probability of `word`.
	return WORDS[word] / N


def damerau_correction(word): 
	#Most probable spelling correction for word.
	return max(candidates(word), key=P)


def candidates(word): 
	#Generate possible spelling corrections for word.
	return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
	#The subset of `words` that appear in the dictionary of WORDS.
	return set(w for w in words if w in WORDS)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word): 
	#All edits that are two edits away from `word`.
	return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def make_correction_nmatches(wrong_text, lexicon):
	
	t1 = clock()
	wrong_text_list = remove_punctation(wrong_text).split()
	lexicon_list = lexicon.split()
	ausgabe = ""
	correction = ""
	for word in wrong_text_list:
		word_correct = False
		for lex_ent in lexicon_list:
			if word == lex_ent:
				word_correct = True
				correction = correction + word + " "
		
		if word_correct == False:
			korrektur =  "das Wort:" + correction_nmatches(lexicon.split(), word) + " ist dem Wort:" + word + " am aehnlichsten" + "\n"
			korrektur2 = correction_nmatches(lexicon.split(), word)
			word = '''word'''
			correction  =  correction + korrektur2 + " "
			ausgabe = ausgabe + korrektur

	t2 = clock()
	time = t2 - t1
	return correction  

def make_correction_nmatches_time(wrong_text, lexicon):
	
	t1 = clock()
	wrong_text_list = remove_punctation(wrong_text).split()
	lexicon_list = lexicon.split()
	ausgabe = ""
	correction = ""
	for word in wrong_text_list:
		word_correct = False
		for lex_ent in lexicon_list:
			if word == lex_ent:
				word_correct = True
				correction = correction + word + " "
		
		if word_correct == False:
			korrektur =  "das Wort:" + correction_nmatches(lexicon.split(), word) + " ist dem Wort:" + word + " am aehnlichsten" + "\n"
			korrektur2 = correction_nmatches(lexicon.split(), word)
			word = '''word'''
			correction  =  correction + korrektur2 + " "
			ausgabe = ausgabe + korrektur

	t2 = clock()
	time = t2 - t1
	return time
	

def make_correction_jaccard(wrong_text, lexicon):
	t1 = clock()
	wrong_text_list = remove_punctation(wrong_text).split()
	lexicon_list = lexicon.split()
	ausgabe = ""
	correction = ""
	for word in wrong_text_list:
		word_correct = False
		for lex_ent in lexicon_list:
			if word == lex_ent:
				word_correct = True
				correction = correction + word + " "
		
		if word_correct == False:
			korrektur =  "das Wort:" + correction_jaccard(lexicon.split(), word) + " ist dem Wort:" + word + " am aehnlichsten" + "\n"
			korrektur2 = correction_jaccard(lexicon.split(), word)
			word = '''word'''
			correction  =  correction + korrektur2 + " "
			ausgabe = ausgabe + korrektur

	t2 = clock()
	time = t2 - t1
	return correction  

def make_correction_jaccard_time(wrong_text, lexicon):
	t1 = clock()
	wrong_text_list = remove_punctation(wrong_text).split()
	lexicon_list = lexicon.split()
	ausgabe = ""
	correction = ""
	for word in wrong_text_list:
		word_correct = False
		for lex_ent in lexicon_list:
			if word == lex_ent:
				word_correct = True
				correction = correction + word + " "
		
		if word_correct == False:
			korrektur =  "das Wort:" + correction_jaccard(lexicon.split(), word) + " ist dem Wort:" + word + " am aehnlichsten" + "\n"
			korrektur2 = correction_jaccard(lexicon.split(), word)
			word = '''word'''
			correction  =  correction + korrektur2 + " "
			ausgabe = ausgabe + korrektur

	t2 = clock()
	time = t2 - t1
	return time

	
def make_correction_damerau(wrong_text, lexicon):
	t1 = clock()
	wrong_text_list = remove_punctation(wrong_text).split()
	lexicon_list = lexicon.split()
	ausgabe = ""
	correction = ""
	for word in wrong_text_list:
		word_correct = False
		for lex_ent in lexicon_list:
			if word == lex_ent:
				word_correct = True
				correction = correction + word + " "
		
		if word_correct == False:
			korrektur =  "das Wort:" + damerau_correction(word) + " ist dem Wort:" + word + " am aehnlichsten" + "\n"
			korrektur2 = damerau_correction(word)
			word = '''word'''
			correction  =  correction + korrektur2 + " "
			ausgabe = ausgabe + korrektur

	t2 = clock()
	time = t2 - t1
	return correction  	

def make_correction_damerau_time(wrong_text, lexicon):
	t1 = clock()
	wrong_text_list = remove_punctation(wrong_text).split()
	lexicon_list = lexicon.split()
	ausgabe = ""
	correction = ""
	for word in wrong_text_list:
		word_correct = False
		for lex_ent in lexicon_list:
			if word == lex_ent:
				word_correct = True
				correction = correction + word + " "
		
		if word_correct == False:
			korrektur =  "das Wort:" + damerau_correction(word) + " ist dem Wort:" + word + " am aehnlichsten" + "\n"
			korrektur2 = damerau_correction(word)
			word = '''word'''
			correction  =  correction + korrektur2 + " "
			ausgabe = ausgabe + korrektur

	t2 = clock()
	time = t2 - t1
	return time
	

def give_correction_all(wrong_text, lexicon):	#schreibt in ein neues Textfeld die falschen WÖrter mit dem Korrekturvorschlag, aus den Radiobuttons wird die Art der Korrektur herausgelesen
	
	if v.get() == 1:
		wrong_text_list = remove_punctation(wrong_text).split()
		lexicon_list = lexicon.split()
		ausgabe = ""
		correction = ""
		for word in wrong_text_list:
			word_correct = False
			for lex_ent in lexicon_list:
				if word == lex_ent:
					word_correct = True
					correction = correction + word + " "
			
			if word_correct == False:
				korrektur =  "das Wort: " + correction_nmatches(lexicon.split(), word) + " ist dem Wort: " + word + " am aehnlichsten" + "\n"
				korrektur2 = correction_nmatches(lexicon.split(), word)
				word = '''word'''
				correction  =  correction + korrektur2 + " "
				ausgabe = ausgabe + korrektur
		return "N-Gramm Korrekturen: \n" + ausgabe
	elif v.get() == 2:
		wrong_text_list = remove_punctation(wrong_text).split()
		lexicon_list = lexicon.split()
		ausgabe = ""
		correction = ""
		for word in wrong_text_list:
			word_correct = False
			for lex_ent in lexicon_list:
				if word == lex_ent:
					word_correct = True
					correction = correction + word + " "
			
			if word_correct == False:
				korrektur =  "das Wort: " + correction_jaccard(lexicon.split(), word) + " ist dem Wort: " + word + " am aehnlichsten" + "\n"
				korrektur2 = correction_jaccard(lexicon.split(), word)
				word = '''word'''
				correction  =  correction + korrektur2 + " "
				ausgabe = ausgabe + korrektur
		return "Jaccard Korrekturen: \n" + ausgabe
	else:
		wrong_text_list = remove_punctation(wrong_text).split()
		lexicon_list = lexicon.split()
		ausgabe = ""
		correction = ""
		for word in wrong_text_list:
			word_correct = False
			for lex_ent in lexicon_list:
				if word == lex_ent:
					word_correct = True
					correction = correction + word + " "
			
			if word_correct == False:
				korrektur =  "das Wort:" + damerau_correction(word) + " ist dem Wort:" + word + " am aehnlichsten" + "\n"
				korrektur2 = damerau_correction(word)
				word = '''word'''
				correction  =  correction + korrektur2 + " "
				ausgabe = ausgabe + korrektur
				
		return "Damerau Korrekturen: \n" + ausgabe



def write_correctionfile(correction_string):
	new_correction = file("correction.txt","a")
	new_correction.write (correction_string)
	new_correction.close()	
	

def show_mistakes():
	root_cor = Tk()
	global lexicon_text
	cor_text = Text( root_cor, height = 20, width = 40, bg = "white" )
	cor_text.pack(padx=10, pady=20, side=LEFT)
	cor_text.insert(END, give_correction_all(data_mistakes, data_lex))
	if v.get() == 1:
		root_cor.title("N-Gramme")
		
	elif v.get()== 2:
		root_cor.title("Jaccard")
	else:
		root_cor.title("Damerau")
		
	root_cor.mainloop() #Lexikoneditor GUI
	
	
def show_correction_txt():
	w2.insert(END, make_correction_nmatches(data_mistakes, data_lex))
	
def compare_methods_time_gui():
	root_comp = Tk()
	time_ngrams = make_correction_nmatches_time(data_mistakes, data_lex)
	time_jaccard = make_correction_jaccard_time(data_mistakes, data_lex)
	time_damerau = make_correction_damerau_time(data_mistakes, data_lex)
	button_comp = Button(root_comp, text='Graph', width=50, command=compare_methods)
	button_comp.pack(padx=10, pady=10)
	label_ngrams = Label(root_comp, text = "N-Gramme: " + str(time_ngrams))
	label_ngrams.pack(padx=10, pady=10)
	label_ngrams = Label(root_comp, text = "Jaccard: " + str(time_jaccard))
	label_ngrams.pack(padx=10, pady=10)
	label_ngrams = Label(root_comp, text = "Damerau: " + str(time_damerau))
	label_ngrams.pack(padx=10, pady=10)
	root_comp.title("Vergleich: Zeit")
	root_comp.mainloop()

def compare_methods_accuracy_gui():
	root_comp = Tk()
	accuracy_ngrams = compare_accuracy(make_correction_nmatches(data_mistakes, data_lex).split())
	accuracy_jaccard = compare_accuracy(make_correction_jaccard(data_mistakes, data_lex).split())
	accuracy_damerau = compare_accuracy(make_correction_damerau(data_mistakes, data_lex).split())
	button_comp = Button(root_comp, text='Graph', width=50, command=compare_methods_accuracy)
	button_comp.pack(padx=10, pady=10)
	label_ngrams = Label(root_comp, text = "N-Gramme: " + str(accuracy_ngrams))
	label_ngrams.pack(padx=10, pady=10)
	label_ngrams = Label(root_comp, text = "Jaccard: " + str(accuracy_jaccard))
	label_ngrams.pack(padx=10, pady=10)
	label_ngrams = Label(root_comp, text = "Damerau: " + str(accuracy_damerau))
	label_ngrams.pack(padx=10, pady=10)
	root_comp.mainloop()

	
def compare_methods():
	order = range(1,4)
	methods = [u'N-Gramme', u'Jaccard', u'Damerau']
	time_ngrams = make_correction_nmatches_time(data_mistakes, data_lex)
	time_jaccard = make_correction_jaccard_time(data_mistakes, data_lex)
	time_damerau = make_correction_damerau_time(data_mistakes, data_lex)
	counts = [time_ngrams, time_jaccard, time_damerau]
	fig = plt.figure()
	plt.bar(order, counts, align="center")
	plt.xticks(order, methods, rotation=45, ha='right')
	plt.title(u'Geschwindikeitsvergleich der Algorithmen')
	plt.tight_layout()
	plt.show()

def compare_methods_accuracy():
	order = range(1,4)
	methods = [u'N-Gramme', u'Jaccard', u'Damerau']
	accuracy_ngrams = compare_accuracy(make_correction_nmatches(data_mistakes, data_lex).split())/(len(data_correct.split())/100)
	accuracy_jaccard = compare_accuracy(make_correction_jaccard(data_mistakes, data_lex).split())/(len(data_correct.split())/100)
	accuracy_damerau = compare_accuracy(make_correction_damerau(data_mistakes, data_lex).split())/(len(data_correct.split())/100)
	counts = [accuracy_ngrams, accuracy_jaccard, accuracy_damerau]
	fig = plt.figure()
	plt.bar(order, counts, align="center")
	plt.xticks(order, methods, rotation=45, ha='right')
	plt.title(u'Fehlerquote der Algorithmen in Prozent ')
	plt.tight_layout()
	plt.show()

def compare_accuracy(text_to_compare):
	clean_text = []
	clean_text = remove_punctation(data_correct).split()
	i = 0
	mistake_counter = 0
	while i < len(clean_text):
		if  clean_text[i] != text_to_compare[i]:
			mistake_counter = mistake_counter +1
		i = i+1
	return mistake_counter
	




v = IntVar()
#v.set(1)  # hiermit kann man von Anfang an einen der Radiobutton angeklickt lassen

languages = [
    ("N-Grams",1),
    ("Jaccard-Sneath",2),
    ("Damerau-Levinshtein",3)
    
]

def give_algorithm():		#fügt die richtigen algorithmen beim drücken des Radiobuttons ein
	w2.delete('1.0',END)	#löscht das was im textfenster steht
	if v.get() == 1:
		w2.insert(END, make_correction_nmatches(data_mistakes, data_lex))
	elif v.get()== 2:
		w2.insert(END, make_correction_jaccard(data_mistakes, data_lex))
	else:
		w2.insert(END, make_correction_damerau(data_mistakes, data_lex))
		
		  

Label(root, 
      text="""Choose an algorithm:""",
      justify = LEFT,
      padx = 20,font=(16)).pack()
      

for txt, val in languages:
    Radiobutton(root, 
                text=txt,
                padx = 20, 
                variable=v, 
                command=give_algorithm,
                value=val).pack(anchor=W)

w1 = Text(root, height = 20, width = 40, bg = "white")
w1.insert(END, "Unkorrigerter Text: \n")
w1.pack(padx=10, pady=20, side=LEFT)
w1.insert(END,data_mistakes)
w2 = Text(root, height = 20, width = 40, bg = "white")
w2.pack(padx=5, pady=20, side=LEFT)
#w2.insert (END, make_correction_nmatches(data_mistakes, data_lex)	)
button_lex = Button(root, text='Lexikon', width=25, command=open_lexicon)
button_lex.pack(padx=5, pady=5)
button_check = Button(root, text='Check', width=25, command=show_mistakes)
button_check.pack(padx=5, pady=5)
button_compare = Button(root, text='Compare Time', width=25, command=compare_methods_time_gui)
button_compare.pack(padx=5, pady=5)
button_compare = Button(root, text='Compare Accuracy', width=25, command=compare_methods_accuracy_gui)
button_compare.pack(padx=5, pady=5)	
	
root.mainloop() # Haupt-GUI
