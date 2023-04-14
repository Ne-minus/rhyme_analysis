# ЭТОТ КОД ДЕЛАЕТ РАЗНЫЕ ВИДЫ ГРАНИЦ МЕЖДУ СЛОГАМИ, КЛИТИКАМИ,
# СЛОВАМИ И СИНТАГМАМИ
# подробнее: https://colab.research.google.com/drive/1F6rf_Difpv1sYtp2X1PNsvUi3ARu0b07#scrollTo=KE5t4CsRGmzl

pip install konlpy
from konlpy.tag import Twitter
from konlpy.tag import Kkma
import csv
import re

twitter = Twitter()
kkma = Kkma()

def intruser(word, final_trans):
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

        elif entity[1] == 'Adjective':
            # проверяем, аттрибутивное или предикативное употребление
            if 'ETD' in kkma.pos(entity[0])[-1][1]:
                good_text += intruser(entity[0], ft) + '#'
            else:
                good_text += intruser(entity[0], ft) + ' / '
        
        elif entity[1] == 'Verb':

            # проверка на грамматику, в которой нет озвончения
            tr = intruser(entity[0], ft)
            if 'ɾ-ke-' in tr:
              # мы хотим заменить последнее вхождение такого куска
              rtr = ''.join(reversed(list(tr)))
              rtr.replace('-ek-ɾ', '-ek͈-ɾ', 1)
              tr = ''.join(reversed(list(rtr)))

            # проверяем, аттрибутивное или предикативное употребление
            if 'ETD' in kkma.pos(entity[0])[-1][1]:
                good_text +=  + '#'
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

text = '예쁜 언니가 약하고 넉넉해요'
print(separator(text, final_trans))
print('')

def stop_assim(chanks):
    sonors = ['m', 'n']
    stops_to_sonors = {'m': ['p', 'pʰ', 'p͈', 'lb', 'ps'],
                       'n': ['t', 'tʰ', 't͈', 'c', 'cʰ', 'c͈', 's', 's͈'],
                       'ŋ': ['k', 'kʰ', 'k͈', 'lg', 'ks'],
                      }
    for i in range(len(chanks) - 1):
        for k, v in stops_to_sonors.items():
            bgram = re.search(r'(lg|ps|ks|lb|cʰ|kʰ|tʰ|pʰ|t͈|k͈|p͈|c͈)', chanks[i][-2:])
            if bgram is None: 
                if chanks[i][-1] in v and chanks[i + 1][0] == 'ɾ':
                    chanks[i] = chanks[i][:-1] + k
                    chanks[i + 1] = 'n' + chanks[i + 1][1:]
                    
                elif chanks[i][-1] in v and chanks[i + 1][0] in sonors:
                    chanks[i] = chanks[i][:-1] + k
            else:
                if bgram.group(1) in v and chanks[i + 1][0] == 'ɾ':
                    chanks[i] = chanks[i][:-2] + k
                    chanks[i + 1] = 'n' + chanks[i + 1][1:]
                                        
                elif bgram.group(1) in v and chanks[i + 1][0] in sonors:
                    chanks[i] = chanks[i][:-2] + k
                    
    return chanks

def sonor_assim(chanks):
    final_sonor = ['m', 'ŋ']
    for i in range(len(chanks) - 1):
        if chanks[i][-1] == 'ɾ' and chanks[i + 1][0] == 'n':
            chanks[i + 1] = 'ɾ' + chanks[i + 1][1:]
            
        elif chanks[i][-1] == 'n' and chanks[i + 1][0] == 'ɾ':
            chanks[i] = chanks[i][:-1] + 'ɾ'
            
        elif chanks[i][-1] in final_sonor and chanks[i + 1][0] == 'ɾ':
            chanks[i + 1] = 'n' + chanks[i + 1][1:]
            
    return chanks

text2 = '국립 막내'
text3 = '몇 마리'
text5 = '닭 넋만 신라'
text6 = '디귿 리을'
separated = separator(text5, final_trans)
print(separated)
words = separated.split('#')
print('')

for i in range(len(words)):
    #ассимиляция между слогами
    words[i] = "-".join(stop_assim(words[i].split('-')))
    words[i] = "-".join(sonor_assim(words[i].split('-')))

#ассимиляция между словами
words = stop_assim(words)
words = sonor_assim(words)

print("#".join(stop_assim(words))) #возвращаю строчку в том же виде как и separator            
