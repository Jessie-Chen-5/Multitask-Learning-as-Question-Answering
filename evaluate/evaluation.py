from __future__ import print_function
from collections import Counter
import string
import re
import argparse
import json
import sys
import numpy as np


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def f1_score(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return [0]
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    # print(precision, recall, f1)
    return [precision, recall, f1]

def f1_beam(output, groundtruth):
	f1 = []
	precision_total = []
	recall_total = []
	while True:
		line1 = output.readline().strip().replace('<unk>', '')
		line2 = groundtruth.readline().strip()
		if not line1 or not line2:
			break
		beam_results = line1.split('\t')
		highest_score = float("-inf")
		highest_precision = float("-inf")
		highest_recall = float("-inf")
		for beam_result in beam_results:
			m = f1_score(beam_result, line2)
			if len(m) != 3:
				continue
			precision, recall, score = m[0], m[1], m[2]
			# print(precision, recall, score)
			highest_score = max(highest_score, score)
			highest_precision = max(highest_precision, precision)
			highest_recall = max(highest_recall, recall)
		if highest_score != float("-inf"):
			f1.append(highest_score)
			precision_total.append(highest_precision)
			recall_total.append(highest_recall)


	f1 = np.array(f1)
	print(np.mean(f1), np.max(f1))
	precision_total = np.array(precision_total)
	print(np.mean(precision_total), np.max(precision_total))
	recall_total = np.array(recall_total)
	print(np.mean(recall_total), np.max(recall_total))

def BLEU_score(output, groundtruth):
	output_words = output.split()
	total_count = 0
	pre = 0
	for word in output_words:
		word = word.strip()
		if word:
			total_count += 1
			if word in groundtruth:
				pre += 1
	return pre/total_count if total_count != 0 else 0

def BLEU_beam(output, groundtruth):
	bleu = []
	while True:
		line1 = output.readline().strip().replace('<unk>', '')
		line2 = groundtruth.readline().strip()
		if not line1 or not line2:
			break
		beam_results = line1.split('\t')
		highest_score = float("-inf")
		for beam_result in beam_results:
			score = BLEU_score(beam_result, line2)
			highest_score = max(highest_score, score)
		bleu.append(highest_score)
	bleu = np.array(bleu)
	print(np.mean(bleu), np.max(bleu))

def acc_score(output, groundtruth):
	output_words = output.split()
	for word in output_words:
		word = word.strip()
		if word:
			if word in groundtruth:
				return 1
	return 0

def hashtag_beam(output, groundtruth):
	acc = []
	while True:
		line1 = output.readline().strip().replace('<unk>', '')
		line2 = groundtruth.readline().strip()
		if not line1 or not line2:
			break
		beam_results = line1.split('\t')
		highest_score = float("-inf")
		for beam_result in beam_results:
			score = acc_score(beam_result, line2)
			highest_score = max(highest_score, score)
		acc.append(highest_score)
	acc = np.array(acc)
	print(np.mean(acc), np.max(acc))



output = open(sys.argv[1], 'r')
groundtruth = open(sys.argv[2], 'r')
metric = sys.argv[3]
if metric == 'squad':
	f1_beam(output, groundtruth)
elif metric == 'dialogue':
	BLEU_beam(output, groundtruth)
elif metric == 'hashtag':
	hashtag_beam(output, groundtruth)


