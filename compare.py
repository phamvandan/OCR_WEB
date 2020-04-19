from difflib import SequenceMatcher

f_text_optimal = open('text_optimal.txt', 'r')
f_text_corrected = open('text_corrected.txt', 'r')

text_optimal = f_text_optimal.read()
text_corrected = f_text_corrected.read()

s = SequenceMatcher(lambda x: x == " ", text_optimal, text_corrected)

print(round(s.ratio(), 3))
