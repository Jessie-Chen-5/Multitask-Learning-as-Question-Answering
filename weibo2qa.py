import json

inputfile = open('./data/train.txt', 'r')
outputfile = open('./data/weibo.json', 'w')

data = []
for line in inputfile:
	line = line.strip()
	if line:
		data.append(line)
	else:
		dic = {}
		context = ""
		for i in range(len(data)-2):
			context = context + data[i] + ' '
		dic['context'] = context
		dic['question'] = data[len(data)-2]
		dic['answer'] = data[len(data)-1]
		outputfile.write(json.dumps(dic) + '\n')
		data = []

