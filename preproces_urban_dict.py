"""
Prepoces files from:
https://github.com/mattbierner/urban-dictionary-word-list/tree/master/data
to serve as urban dictonary for word cheking, as the api for the dictonary 
have time constraints 

"""
import enchant, sys
import pandas as pd
import urbandictionary as ud
from nltk.tokenize import RegexpTokenizer
import numpy as np
import re

class RepeatReplacer(object):
  def __init__(self):
    self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
    self.repl = r'\1\2\3'
  def replace(self, word):
    repl_word = self.repeat_regexp.sub(self.repl, word)
    if repl_word != word:
      return self.replace(repl_word)
    else:
      return repl_word
rep_replacer = RepeatReplacer()

def save_file(name, the_list):
    with open('u_'+name+'.txt', 'w', encoding='utf8') as f:
        for item in the_list:
            f.write(item + "\n")

def read_file(fname):
    with open(fname +'.txt', encoding='utf8') as f:
        lines = f.readlines()
        word_set = set()
        for line in lines:
            striped_value = line.strip()
            word = rep_replacer.replace(striped_value)
            word_set.add(word.lower())
    return word_set

files = 'abcdefghijklmnopqrstuvwxyz'
files = list(files) + ['numeric']
for file in files:  
    words = list(read_file(file))
    save_file(file, sorted(words))
