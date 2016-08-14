
def ngram_splitter(inputg):
	ngram_list = []
	i = 0
	while i <= len(inputg)-3:
		zipped = zip( inputg[i],inputg[i+1], inputg[i+2])
		#print zipped
		ngram_list.append(zipped)
		#print ngram_list
		i =i+1
	return ngram_list

print ngram_splitter("hallo")



	

