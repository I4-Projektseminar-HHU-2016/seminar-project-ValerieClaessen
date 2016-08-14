import string










#with open('textm.txt') as f:
#
#    datam = f.readlines()

with open('textm.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')

data_list = data.split()
print data_list


text_correct = "textc.txt"


def remove_punctation(my_str):
	no_punct = ""
	for char in my_str:
	   if char not in punctuations:
		   no_punct = no_punct + char
	return no_punct

def text_to_lex (text_doc):
	
	lex_list = remove_punctation(text_doc)
	lex_set = set(lex_list)
	return lex_set

print remove_punctation(data)
	
#print text_to_lex(text_correct)
	

