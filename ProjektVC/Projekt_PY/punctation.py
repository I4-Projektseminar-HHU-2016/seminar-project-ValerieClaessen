punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''


with open('textm.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')
  
def remove_punctation(my_str):
	no_punct = ""
	for char in my_str:
	   if char not in punctuations:
		   no_punct = no_punct + char
	return no_punct

print remove_punctation(data)


def text_to_lex (text_doc):
	
	lex_list = remove_punctation(text_doc)
	lex_list = lex_list.split()
	lex_set = set(lex_list)
	return lex_set

print text_to_lex(data)

