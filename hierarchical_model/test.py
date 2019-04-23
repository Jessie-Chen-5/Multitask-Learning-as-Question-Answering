import os
import sys

datasets = ['squad', 'hashtag', 'dialogue']
for dataset in datasets:
	s = 'THEANO_FLAGS=mode=FAST_RUN,device=cuda0,floatX=float32 python sample.py ' + sys.argv[1] + ' ./raw_data/context.' + dataset + ' ./Output/output.' + dataset + ' --ignore-unk'
	os.system(s)

