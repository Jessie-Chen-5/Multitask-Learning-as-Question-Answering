from collections import defaultdict
import random
import json
import string
import re

regex = re.compile('[^a-zA-Z0-9]')
dic = defaultdict(int)

inputfile = open('out.txt', 'r')

table = str.maketrans({key: None for key in string.punctuation})
for line in inputfile:
	words = line.strip().split()
	for word in words:
		if word[0] == '#':
			word = regex.sub('', word)
			dic[word.lower().translate(table)] += 1

print(len(dic))
inputfile.close()

inputfile = open('out.txt', 'r')
outputfile = open('hashtag.json', 'w')
count = 0
for line in inputfile:
	words = line.strip().split()
	if len(words) == 0:
		continue
	else:
		data = defaultdict(str)
		context = []
		for word in words:
			# word = re.sub(u"(\u2018|\u2019)", "" , word)
			if word[0] == '#':
				word = regex.sub('', word)
				data['answer'] = data['answer'] + word.lower().translate(table) +' '
				context.append(word)
			elif word[:4] == 'http':
				continue
			else:
				word = regex.sub('', word)
				data['question'] = data['question'] + word.lower().translate(table) + ' '
		for i in range(10-len(context)):
			context.append(random.choice(list(dic.keys())))

		random.shuffle(context)
		for m in context:
			data['context'] = data['context'] + m + ' '
		outputfile.write(json.dumps(data) + '\n')
		count += 1
		if count % 1000 == 0:
			print(count)








