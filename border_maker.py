# ЭТОТ КОД ДЕЛАЕТ РАЗНЫЕ ВИДЫ ГРАНИЦ МЕЖДУ СЛОГАМИ, КЛИТИКАМИ,
# СЛОВАМИ И СИНТАГМАМИ
# подробнее: https://colab.research.google.com/drive/1F6rf_Difpv1sYtp2X1PNsvUi3ARu0b07#scrollTo=KE5t4CsRGmzl

#!pip install konlpy
from konlpy.tag import Twitter
from konlpy.tag import Kkma
import csv

twitter = Twitter()
kkma = Kkma()

def intruser(word, final_trans):
    # ЗДЕСЬ НУЖНО БУДЕТ ПЕРЕФОРМИРОВЫВАТЬ СИНОКОРЕЙСКИЕ СЛОВА (ЗВОНКИЕ -> TENSE)
    ready_word = ''
    for char in word:
        ready_word += '-' + final_trans[char]
    return ready_word.strip('-')

def separator(text, ft):
    syll_dict = dict()

    with open('final_trans.csv') as csvfile:
        spamreader = csv.reader(csvfile)
        sylls = list(spamreader)
        for s in sylls:
            syll_dict[s[0]] = s[2]

    good_text= ' '
    twit_morph = twitter.pos(text, norm = True)

    lil_morphs = ('Josa', 'Suffix', 'Eomi', 'PreEomi')
    end_morphs = ('Exclamation', 'Conjunction', 'Eomi', 'PreEomi')
    bad = ('Foreign', 'Alpha', 'Number', 'Unknown', 'KoreanParticle', 
           'Hashtag', 'ScreenName', 'Email', 'URL')

    for entity in twit_morph:
        print(entity)
        if entity[1] in lil_morphs:
            good_text = good_text.strip(" /-#") + '-' + intruser(entity[0], 
                                                                 ft) + '#'

        elif entity[1] in end_morphs:
            if good_text.endswith('/ '):
                good_text += intruser(entity[0], ft) + ' / '
            else:
                good_text += intruser(entity[0], ft) + ' / '

        elif entity[1] == 'Adjective' or entity[1] == 'Verb':
            # проверяем, аттрибутивное или предикативное употребление
            if 'ETD' in kkma.pos(entity[0])[-1][1]:
                good_text += intruser(entity[0], ft) + '#'
            else:
                good_text += intruser(entity[0], ft) + ' / '

        elif entity[1] == 'Punctuation':
            good_text = good_text.strip(" /-#") + ' / '
        elif entity[1] in bad:
            pass

        else:
            good_text += intruser(entity[0], ft) + '#'


    return good_text.strip(' /#') + ' / '

final_trans = dict()

with open('final_trans.csv', 'r', encoding='utf-8') as ft_file:
    spamreader = csv.reader(ft_file)
    for row in spamreader:
        final_trans[row[0]] = row[2]

#text = '예쁜 언니가 약하고 넉넉해요'
#print(separator(text, final_trans))