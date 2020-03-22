import json
import re


class RuleBase:
	def __init__(self, dict_file='utils/text_correction/rule_base_dict.json'):
		with open(dict_file, 'r') as fp:
			self.data = json.load(fp)
		self.error_words = []
		self.correct_words = []
		for error_word, correct_word in self.data.items():
			self.error_words.append(error_word)
			self.correct_words.append(correct_word)

	def correct(self, string_to_correct):
		string_words = re.findall(r'\S+|\n', string_to_correct)
		for i in range(len(string_words)):
			if string_words[i] == '\n':
				continue
			if string_words[i].lower() in self.error_words:
				string_words[i] = self.data[string_words[i].lower()]
		return " ".join(string_words)
