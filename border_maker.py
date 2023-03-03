# ЭТОТ КОД ДЕЛАЕТ РАЗНЫЕ ВИДЫ ГРАНИЦ МЕЖДУ СЛОГАМИ, КЛИТИКАМИ,
# СЛОВАМИ И СИНТАГМАМИ
# подробнее: https://colab.research.google.com/drive/1F6rf_Difpv1sYtp2X1PNsvUi3ARu0b07#scrollTo=KE5t4CsRGmzl

#!pip install konlpy
from konlpy.tag import Twitter
from konlpy.tag import Kkma

twitter = Twitter()
kkma = Kkma()

def separator(text):
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
            good_text = good_text.strip(" /-#") + '-' + entity[0] + '#'

        elif entity[1] in end_morphs:
            if good_text.endswith('/ '):
                good_text += entity[0] + ' / '
            else:
                good_text += entity[0] + ' / '

        elif entity[1] == 'Adjective' or entity[1] == 'Verb':
            # проверяем, аттрибутивное или предикативное употребление
            if kkma.pos(entity[0])[-1][1]:
                good_text += entity[0] + '#'
            else:
                good_text += entity[0] + ' / '

        elif entity[1] == 'Punctuation':
            good_text = good_text.strip(" /-#") + ' / '
        elif entity[1] in bad:
            pass

        else:
            good_text += entity[0] + '#'


    return good_text.strip(' /#') + ' / '