import nltk
from nltk.corpus import wordnet as wn
from nltk import sent_tokenize, word_tokenize, pos_tag
import re
from collections import OrderedDict
from sense2vec import Sense2Vec
import random
import pandas as pd

s2v = Sense2Vec().from_disk("/home/yacir/Downloads/s2v_reddit_2015_md/s2v_old")


def extract_keywords(text):
    tokens = word_tokenize(text)
    # print(tokens)
    tags = pos_tag(tokens)
    # print(tags)
    keywords = []
    for i in range(0, len(tags)):
        if tags[i][1] in ('NNP', '') and tags[i + 1][1] in ('NNP', ''):
            keywords.append(tags[i][0] + ' ' + tags[i + 1][0])
        if tags[i][1] in ('NNP', '') and tags[i + 1][1] not in ('NNP', '') and tags[i - 1][1] not in ('NNP', ''):
            keywords.append(tags[i][0])
        if tags[i][1] in ('DT', '') and tags[i + 1][1] in ('NN', ''):
            keywords.append(tags[i + 1][0])
        if tags[i][1] in ('DT', '') and tags[i + 1][1] in ('JJ', ''):
            keywords.append(tags[i + 1][0])
        if tags[i][1] in ('CD', ''):
            keywords.append(tags[i][0])
    return list(set(keywords))


def sentence_preprocessing(self, text):
    print("Sentence preprocessing Please wait!...")
    # split sentences from paragraph
    sentences = []
    All_sentences = []
    # sent_tokenize split the paragraph into sentences
    # return nested list
    sentences.append(sent_tokenize(text))
    # nested list to single list
    for sent in sentences:
        sentences = sent
        # removing short sentences less than 20 characters
    for s in sentences:
        if len(s) > 20:
            All_sentences.append(s.strip())  # strip() removes leading and trailing spaces
    return All_sentences


def get_sentence(self, text):
    print("Sentences are being selected on the basis of keywords.Please wait!..")
    # calling keyword function
    keywords, text = self.get_keywords(text)
    # flashtext
    key_processor = self.KeywordProcessor()
    # dictionary key-value
    filtered_sentences = {}

    # adding keywords to processor and to dict
    for k in keywords:
        filtered_sentences[k] = []
        # keywords adding to flashtext
        key_processor.add_keyword(k)

    # calling fn to preprocess sentences from text
    sentences = self.sentence_preprocessing(text)
    print("4.Filtering sentences...")
    keyword_searched = []
    # extracting sentences with given keywords and add to dict keys(keys that are already added)
    for sent in sentences:
        # checking added keywords to flashtext exist in senteces are not
        keyword_searched = key_processor.extract_keywords(sent)
        for key in keyword_searched:
            # appending data at specific key
            filtered_sentences[key].append(sent)

    return filtered_sentences


def get_distractors(self, syn, word):
    print("6.Obtaining relative options from Wordnet...")
    distractors = []
    word = word.lower()
    orignal_word = word

    # checking if word is more than one word then make it one word with _
    if len(word.split()) > 0:
        word = word.replace(" ", "_")

    hypernym = syn.hypernyms()

    if (len(hypernym) == 0):
        return distractors
    for i in hypernym[0].hyponyms():
        name = i.lemmas()[0].name()

        if (name == orignal_word):
            continue
        name = name.replace("_", " ")
        name = " ".join(i.capitalize() for i in name.split())
        if name is not None and name not in distractors:
            distractors.append(name)
    return distractors


def sense2vec_distractors(self, word, s2v):
    output = []
    word = word.lower()
    word = word.replace(" ", "_")

    sense = s2v.get_best_sense(word)
    most_similar = s2v.most_similar(sense, n=8)

    # print ("most_similar ",most_similar)

    for each_word in most_similar:
        append_word = each_word[0].split("|")[0].replace("_", " ").lower()
        if append_word.lower() != word:
            output.append(append_word.title())

    out = list(OrderedDict.fromkeys(output))
    return out


def word_sense(self, sentence, keyword):
    print("5.Getting word sense to obtain best MCQ options with WordNet...")
    word = keyword.lower()
    # pakistan
    # print(keyword)
    if len(word.split()) > 0:
        word = word.replace(" ", "_")
    # pakistan
    syon_sets = wn.synsets(word, 'n')
    # print(keyword)
    # if there is any synset of given keywords
    if syon_sets:
        # checking for wordsense
        # try:
        #     wup = max_similarity(sentence, word, 'wup', pos='n')
        #     adapted_lesk_output = adapted_lesk(sentence, word, pos='n')
        #     lowest_index = min(syon_sets.index(wup), syon_sets.index(adapted_lesk_output))
        #     return syon_sets[lowest_index]
        #
        # except:
        return syon_sets[0]
    else:
        return None


def display(text):
    # dict contains key(keyword) value(sentence)
    # {'pakistan': ["Pakistan is the world's fifth-most populous country."]}
    filtered_sentences = get_sentence(text)
    print(filtered_sentences)
    options_for_mcq = {}
    # keyword(keys in dict)
    for keyword in filtered_sentences:
        # pakistan
        wordsense = self.word_sense(filtered_sentences[keyword][0], keyword)
        if wordsense:
            distractors = get_distractors(wordsense, keyword)
            if len(distractors) > 0:
                options_for_mcq[keyword] = distractors
            if len(distractors) < 4:
                distractors = sense2vec_distractors(keyword, s2v)
                if len(distractors) > 0:
                    options_for_mcq[keyword] = distractors

            else:
                distractors = sense2vec_distractors(keyword, s2v)
                if len(distractors) > 0:
                    options_for_mcq[keyword] = distractors
    print("7. Creating JSON response for API...")
    # empty dataframe using pandas
    df = pd.DataFrame()
    # columns for dataframe
    cols = ['question', 'options', 'extras', 'answer']
    # index for data frame's columns(start from 1)
    index = 1
    print("**********************************************************************************")
    print("NOTE: Human intervention is required to correct some of the generated MCQ's ")
    print("************************************************************************************\n\n")
    for i in options_for_mcq:
        sentence = filtered_sentences[i][0]
        sentence = sentence.replace("\n", '')
        pattern = re.compile(i, re.IGNORECASE)
        # Return the string obtained by replacing the leftmost occurrences
        output = pattern.sub(" ______ ", sentence)
        # printing the question
        print("%s)" % index, output)
        # original world +all options list comprehension
        options = [i.capitalize()] + options_for_mcq[i]
        # list slicing 0 to 4
        top4 = options[:4]
        random.shuffle(top4)
        optionsno = ['a', 'b', 'c', 'd']
        # options generations
        count = 0
        for choice in top4:
            print("\t", optionsno[count], ")", " ", choice)
            count = count + 1
        index = index + 1
        # print("\nMore options: ", options[4:8], "\n\n")
        df = df.append(pd.DataFrame([[output, top4, options[4:8], i.capitalize()]], columns=cols))
        index = index + 1
    df.to_json('response.json', orient='records', force_ascii=False)
