# Function to convert   
def list_to_string(s):
	# initialize an empty string
	str1 = " "

	# return string
	return (str1.join(s))


def using_comprehension(word, sentence):
	return [n for n in range(len(sentence)) if sentence.find(word, n) == n]


def add_tag(words, string):
	indexs = []

	for word in words:
		len_word = len(word)
		index = using_comprehension(word, string)
		for value in index:
			indexs.append(value)
			indexs.append(value + len_word)

	indexs = sorted(indexs)

	add = 0
	for i, index in enumerate(indexs):
		if i % 2 == 0:
			start = index + add
			end = indexs[i + 1] + add
			string = string[:start] + "<b>" + string[start:end] + "</b>" + string[end:]
			add = add + 7
	return string
