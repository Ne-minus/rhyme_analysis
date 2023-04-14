def palatalization(given): # must be first!!
    to_pal = ['k', 'g', 'l', 'ɾ', 'm', 'p', 's', 'ŋ', 'cʰ', 'kʰ', 'tʰ', 'pʰ', 
              't', 'n', 'h', 'k͈', 't͈', 'p͈', 's͈', 'c͈']
    
    front_row = ['i', 'e']

    for tp in to_pal:
        # гласные переднего ряда
        for fr in front_row:
            given = given.replace(tp+'-'+fr, tp+'ʲ-'+fr)
            given = given.replace(tp+fr, tp+'ʲ'+fr)

        # йотированные гласные
        given = given.replace(tp+'-j', tp+'ʲ-')
    
    return given
    
def liquids(given):
    vowels = ['ɐ', 'ʌ', 'o', 'ɨ', 'u', 'i', 'ɛ', 'e']
    given = given.replace('ɾ', 'l')
    for v in vowels:
        given = given.replace('l'+v, 'ɾ'+v)
        given = given.replace('l-'+v, 'ɾ-'+v)
        # нечитаемое ㅎ
        given = given.replace('lh-'+v, 'ɾ-'+v)
        given = given.replace('l-h'+v, 'ɾ-'+v)
    return given


def aspiration(given):
    # ассимиляция по аспирации
    to_fix_k = ['k-h', 'k͈-h', 'kʰ-h', 'h-k', 'h-k͈', 'h-kʰ']
    to_fix_t = ['t-h', 't͈-h', 'tʰ-h', 'h-t', 'h-t͈', 'h-tʰ']
    to_fix_c = ['c-h', 'c͈-h', 'cʰ-h', 'h-c', 'h-c͈', 'h-cʰ']

    for k in to_fix_k:
        given = given.replace(k, '-kʰ')
    for t in to_fix_t:
        given = given.replace(t, '-tʰ')
    for c in to_fix_k:
        given = given.replace(c, '-cʰ')
    
    # нечитаемый ㅎ (с ㄹ разобрались в liquids)
    h_silent = ['m-h', 'n-h', 's-h', 's͈-h', 
                'h-m', 'h-n', 'h-s', 'h-s͈']
    for h in h_silent:
        hh = h.replace('h', '')
        given = given.replace(h, hh)

    return given

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
            chanks[i] = chanks[i][:-1] + 'l'
            chanks[i + 1] = 'l' + chanks[i + 1][1:]
            
        elif chanks[i][-1] == 'n' and chanks[i + 1][0] == 'ɾ':
            chanks[i] = chanks[i][:-1] + 'l'
            chanks[i + 1] = 'l' + chanks[i + 1][1:]
            
        elif chanks[i][-1] in final_sonor and chanks[i + 1][0] == 'ɾ':
            chanks[i + 1] = 'n' + chanks[i + 1][1:]
            
    return chanks


#for i in range(len(words)):
    #ассимиляция между слогами
#    words[i] = "-".join(stop_assim(words[i].split('-')))
#    words[i] = "-".join(sonor_assim(words[i].split('-')))

#ассимиляция между словами
#words = stop_assim(words)
#words = sonor_assim(words)