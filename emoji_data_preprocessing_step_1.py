import enchant, sys
import pandas as pd

from nltk.tokenize import RegexpTokenizer
from nltk.metrics import edit_distance
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')
import re

import numpy as np
import io

if sys.version_info[0] > 2:
    unicode = str
    


def read_urban_dict(fname):
    with io.open('u_'+fname +'.txt', encoding='utf8') as f:
        lines = f.readlines()
        word_lst = []
        for line in lines:
            striped_value = line.strip()
            word_lst.append(striped_value)

        return word_lst


def fill_urban_dict():
    urban_dict = {}

    u_files = 'abcdefghijklmnopqrstuvwxyz'
    u_files = list(u_files)
    for fname in u_files:  
        u_words = read_urban_dict(fname)
        urban_dict[fname] = u_words
    return urban_dict


urban_dict = fill_urban_dict()


def urban_chek(word):
    word =  word.lower()
    first_later = word[0]
    if first_later not in 'abcdefghijklmnopqrstuvwxyz':
        return False
    L = urban_dict[first_later]
    start = 0
    end = len(L) - 1
    
    while start <= end:
        middle = int((start + end)/ 2)
        midpoint = L[middle]
        if midpoint == word:
            return True
        elif midpoint > word:
            end = middle - 1
        elif midpoint < word:
            start = middle + 1
    return False


def __concat(object1, object2):
    if isinstance(object1, str) or isinstance(object1, unicode):
        object1 = [object1]
    if isinstance(object2, str) or isinstance(object2, unicode):
        object2 = [object2]
    return object1 + object2


def __capitalize_first_char(word):
    return word[0].upper() + word[1:]


def split2(word, language='en_us'):
    dictionary = enchant.Dict(language)
    max_index = len(word)
    for index, char in enumerate(word):
        left_compound = word[0:max_index-index]
        right_compound_1 = word[max_index-index:max_index]
        right_compound_2 = word[max_index-index+1:max_index]
        if right_compound_1:
            right_compound1_upper = right_compound_1[0].isupper()
        if right_compound_2:
            right_compound2_upper = right_compound_2[0].isupper()
        if index > 0 and len(left_compound) > 1 and not dictionary.check(left_compound):
            left_compound = __capitalize_first_char(left_compound)
        is_left_compound_valid_word = len(left_compound) > 1 and dictionary.check(left_compound)
        if is_left_compound_valid_word and \
                ((not split(right_compound_1, language) == '' and not right_compound1_upper) \
                or right_compound_1 == ''):
            return [compound for compound in __concat(left_compound, split(right_compound_1, language))\
                    if not compound == '']
        elif is_left_compound_valid_word and word[max_index-index:max_index-index+1] == 's' and \
            ((not split(right_compound_2, language) == '' and not right_compound2_upper) \
            or right_compound_2 == ''):
            return [compound for compound in __concat(left_compound, split(right_compound_2, language))\
                    if not compound == '']
    if not word == '' and dictionary.check(word):
        return word
    elif not word == '' and dictionary.check(__capitalize_first_char(word)):
        return __capitalize_first_char(word)
    else:
        return ''

def split(word, language='en_us'):
    dictionary = enchant.Dict(language)
    max_index = len(word)
    for index, char in enumerate(word):
        left_compound = word[0:max_index-index]
        right_compound_1 = word[max_index-index:max_index]
        right_compound_2 = word[max_index-index+1:max_index]
        if right_compound_1:
            right_compound1_upper = right_compound_1[0].isupper()
        if right_compound_2:
            right_compound2_upper = right_compound_2[0].isupper()
        if index > 0 and len(left_compound) > 1 and (not dictionary.check(left_compound) or not urban_chek(left_compound)):
            left_compound = __capitalize_first_char(left_compound)
        is_left_compound_valid_word = len(left_compound) > 1 and (dictionary.check(left_compound) or urban_chek(left_compound))
        if is_left_compound_valid_word and \
                ((not split(right_compound_1, language) == '' and not right_compound1_upper) \
                or right_compound_1 == ''):
            return [compound for compound in __concat(left_compound, split(right_compound_1, language))\
                    if not compound == '']
        elif is_left_compound_valid_word and word[max_index-index:max_index-index+1] == 's' and \
            ((not split(right_compound_2, language) == '' and not right_compound2_upper) \
            or right_compound_2 == ''):
            return [compound for compound in __concat(left_compound, split(right_compound_2, language))\
                    if not compound == '']
    if not word == '' and (dictionary.check(word) or urban_chek(word)):
        return word
    elif not word == '' and dictionary.check(__capitalize_first_char(word)) and urban_chek(__capitalize_first_char(word)):
        return __capitalize_first_char(word)
    else:
        return ''



class RepeatReplacer(object):
  def __init__(self):
    self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
    self.repl = r'\1\2\3'
  def replace(self, word):
    if (wordnet.synsets(word) or urban_chek(word)):
      return word
    repl_word = self.repeat_regexp.sub(self.repl, word)
    if repl_word != word:
      return self.replace(repl_word)
    else:
      return repl_word
rep_replacer = RepeatReplacer()


class SpellingReplacer(object):
  def __init__(self, dict_name='en_US', max_dist=2):
    self.spell_dict = enchant.Dict(dict_name)
    self.max_dist = max_dist
  def replace(self, word):
    if (self.spell_dict.check(word) or urban_chek(word)):
      return word
    suggestions = self.spell_dict.suggest(word)
    if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
      return suggestions[0]
    else:
      return word
spel_replacer = SpellingReplacer()
def read_file(fname):
    data = []
    with io.open(fname,encoding='Utf8') as f:
        for line in f:
            data.append(line)
    return data
from nltk.corpus import stopwords
english_stops = set(stopwords.words('english'))
def tokenize_text(text):
    tokens = []
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            if word in english_stops:
                continue
            tokens.append(word)
    return tokens

loc_tokenizer = RegexpTokenizer("@([ ]*[A-Za-tv-z].*)")
hash_tokenizer = RegexpTokenizer("#[ ]*([A-Za-z0-9]*)")
                                 
def find_hashtags(row):
    new_row = hash_tokenizer.tokenize(row)
    result = []
    for word in new_row:
        splited_words = split(word)
        splited_words_only_us = split2(word)
        if len(splited_words_only_us) <= len(splited_words):
            splited_words = splited_words_only_us
        for new_word in splited_words:
            result.append(new_word)
    return result


def find_locations(row):
    new_row = loc_tokenizer.tokenize(row)                 
    loc_tokens = []
    for word in new_row:
        word = rep_replacer.replace(word)
        word = spel_replacer.replace(word)
        loc_tokens = loc_tokens + nltk.word_tokenize(word)
    return loc_tokens

def splitter(row):

    row = tokenize_text(row)

    result = []

    for word in row:
        word = rep_replacer.replace(word)
        word = spel_replacer.replace(word)
        #splited_words = split(word)
        #splited_words_only_us = split2(word)
        #if len(splited_words_only_us) <= len(splited_words):
            #splited_words = splited_words_only_us
        #for new_word in splited_words:
        result.append(word)

    return result

def save_file(the_list):
    with io.open('tweets_word_tok_2h_test'+'.txt', 'w', encoding='utf8') as f:
        for item in the_list:
            f.write(item + "\n")
def save_file2(the_list):
    with io.open('tweets_word_tok_low_2h_test'+'.txt', 'w', encoding='utf8') as f:
        for item in the_list:
            f.write(item.lower() + "\n")


tweets = read_file('us_test.text')
df =pd.DataFrame(tweets,columns =['Text'])
df['hashtags'] = df['Text'].apply(find_hashtags)
df['location'] = df['Text'].apply(find_locations)
df['Text'] = df['Text'].str.replace(r'#[ ]*[A-Za-z0-9]*','')
df['Text'] = df['Text'].str.replace(r'@[ ]*[A-Za-tv-z].*','')
df['Text'] = df['Text'].str.replace(r'@','')
df['Text'] = df['Text'].apply(splitter)
text_to_list = df['Text'].values.tolist()
hashtag_to_list = df['hashtags'].values.tolist()
location_to_list = df['location'].values.tolist()
result = []
for idx in range (len(df['Text'])):
    row = ''
    for item in df['Text'][idx]:
        row = row + ' ' + item
    row = row +' @'
    for item in df['location'][idx]:
        row = row + ' ' + item
    row = row + ' #'
    for item in df['hashtags'][idx]:
        row = row + ' ' + item
    result.append(row)

save_file(result) 
save_file2(result)
