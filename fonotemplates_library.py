# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 21:24:27 2023

@author: Ahti Lohk
"""

import re

# MEELISE PROGRAMMI MALLID: 55 TK
fono_templates = ["VV#","VVQ#","VVQQ#","VVC#","VVss#","VVsQ#","VVQs#",
"VVLQ#","VVLQQ#","VVCC#","VVCCC#","V#","VC#","VLQ#","VLQQ#",
"VLh#","VCC#","VLss#","VLsQ#","VLhv#","VLQC#",
"VCCC#","VCCCC#","VV$Q","VV$","VVs$s","VVs$Q","VVL$Q",
"VVQ$L","VVQ$j","VVQ$","VVQQ$","VVC$","VVQs$","VVsQ$","VVLQ$","VVLQ$Q","VVLQQ$","VVCC$",
"VVCCC$","VL$Q","VL$h","VC$","VLQ$","VLQ$Q","VLQ$s","VLs$",
"VLh$","VCC$","VLsQ$","VLQC$","VCCC$","VLQCC$","VCCCC$","VC$C", 'V$']

shift = [2,2,3,2,3,2,3,2,4,2,2,1,2,2,3,3,2,3,3,3,3,2,2,2,2,3,3,2,2,2,3,3,2,3,3,
         2,4,4,2,2,2,4,2,2,3,3,3,3,2,3,3,2,3,2,2,1]

fono_shift_dict = dict(zip(fono_templates, shift))

words = ['v:öö', 'l:aat', 'v:eel', 'p:oiss', 'l:aast', 'l:oots','h:uult', 'k:eeld', 
         'p:aavst', 'j:a', 'k:as', 'k:urt', 'mon:arh', 'k:ast', 'm:arss', 'k:unst', 
         'v:urhv', 'l:onks', 't:ekst', 'l:aa$ta', 'kr:oo$ni', 'p:ois$se', 'l:aas$tu', 'k:aar$ti', 
         'k:aat$ri', 'k:eel$du', 'r:oots$lane', 's:ääst$lik', 'k:aart$lane', 'j:uurd$lus', 'p:aavst$lus', 'k:ar$ta', 
         'mon:ar$hi', 'k:al$du', 'p:ilt$lik', 'v:els$ker', 'v:urh$vi', 'k:aps$lid', 'k:orst$na', 'k:ants$ler', 
         ':ekst$ra', 'v:intsk$lema', 'g:angst$rid']


trans_dict = {'a':'V', 'e': 'V', 'i': 'V', 'o':'V', 'u': 'V', 'õ': 'V', 'ä': 'V', 
              'ö': 'V', 'ü': 'V', 'k': 'Q', 'p': 'Q', 't':'Q', 'T': 'Q', 'f': 'Q', 'š':'Q', 
              'l':'L', 'L': 'L', 'm':'L', 'n': 'L', 'N': 'L', 'r':'L', 'b':'C', 'c': 'C', 'd': 'C', 
              'D': 'C', 'g': 'C', 'h': 'C', 'j':'C', 'v': 'v', 's': 's', 'S': 's'}


keys = ['Vs$','VVv#', 'VC$v', 'VCv$','VC$j','VCQ$','VL$s','Vs$S',
        'Vss#','VQ$s','VsQ$s','VLL$','VCL#','VQs#','VV$s','VV$j',
        'VCQ#','VQQ#','VC$Q','VQ$','Vs$s','VL#', "VL$v", 'Vs$Q',
        'VsQ$','VL$j','VLL#', 'VQ$Q','VVs#','VVL#', 'VVLC#', 'VVvsQ#', 
        'Vs#', 'VLC#', 'VsQ#', 'VLCv#', 'VLQs#', 'VQsQ#', 'VVL$', 'VVLC$', 
        'VVvsQ$', 'VL$', 'VLC$', 'VQs$', 'VLQs$', 'VQsQ$', 'VLQsQ$', 'VLCsQ$', 
        'VLs$Q', 'VVs$j', 'VVQ$s', 'VVC$s', 'VLC$s', 'VV$v', 'VCQ$s', 'VsQ$j', 
        'VVL$s', 'VVQ$v', 'VQs$Q', 'Vv$v', 'VVC$j', 'VQ#', 'VLv#', 'VLs$s', 
        'VVv$', 'VQQ$', 'VLQs$j', 'VVQs$Q', 'VVL$j', 'VsQ$v', 
        'VQs$j', 'VLQ$j', 'VLv$', 'VQ$j', 'VLC$j', 'Vs$v', 'VLL$s', 'VVs$',
        'VV$S', 'VCL$', 'VCL$j', 'VCL$s', 'VQ$v', 'Vs$h', 'Vs$j', 'VQQ$j', 
        'VQQ$s', 'VQs$s', 'VQs$v', 'VLC$Q', 'VLv$Q', 'VLv$s', 'VCQ$Q', 'VCQ$v',
        'VsQ$Q', 'VCvQ#']

values = ['VC$','VVC#', 'VC$C','VCC$','VC$C','VCC$','VC$C','VC$C','VCC#',
          'VC$','VCC$','VCC$','VCC#','VCC#','VV$','VV$','VCC#','VCC#','VC$C',
          'VC$','VC$', 'VC#', 'VC$C','VC$C','VCC$','VC$C','VCC#', 'VC$C',
          'VVC#','VVC#', 'VVCC#', 'VVCCC#', 'VC#', 'VLh#', 'VCC#', 'VLhv#', 
          'VLQC#', 'VCCC#', 'VVC$', 'VVCC$', 'VVCCC$', 'VC$', 'VLh$', 'VCC$', 
          'VLQC$', 'VCCC$', 'VLQCC$', 'VCCCC$', 'VLs$', 'VVC$', 'VVQ$', 'VVC$', 
          'VCC$', 'VV$', 'VCC$', 'VCC$', 'VVC$', 'VVQ$', 'VCC$', 'VC$C', 'VVC$', 
          'VC#', 'VCC#', 'VLs$', 'VVC$', 'VCC$', 'VLQC$', 'VVQs$', 'VVC$', 'VVC$',
          'VCC$', 'VLQ$', 'VCC$', 'VC$', 'VCC$', 'VC$', 'VCC$', 'VVC$',
          'VV$', 'VCC$', 'VCC$', 'VCC$', 'VC$', 'VC$', 'VC$', 'VCC$',
          'VCC$', 'VCC$', 'VCC$', 'VCC$', 'VCC$', 'VCC$','VCC$', 'VCC$',
          'VCC$', 'VCCC#']


except_dict = dict(zip(keys, values))
"""
sorted_except_dict = sorted(except_dict.items(), key=lambda x: x[0])

k = 0    
for key, value in sorted_except_dict:
    k += 1
    print(k, ":", key, "->", value, "->", fono_shift_dict[value])
"""

def shift_colon(word, x):
    index = word.find(':')
    if index == -1:
        index = word.find('<')
    if index == -1 or index + x >= len(word):
        return word
    return word[:index] + word[index+1:index+x+1] + ':' + word[index+x+1:]

def shift_colons(initial_word, shifts):
    word = initial_word[:]
    positions = [m.start() for m in re.finditer("<", word)]
    for i, position in enumerate(positions):
        if position + shifts[i] >= len(word):
            pass
        else:
            word = word[:position] + word[position+1:position+shifts[i]+1] + ':' + word[position+shifts[i]+1:]
    return word


def find_fono_template(word):
    k_pos = word.find(":")
    if k_pos == -1:
        k_pos = word.find('<')
    if k_pos == -1:
        return ''
    template = ''
    for i in range(k_pos+1, len(word)):
        if word[i] == "$":
            template += '$'
            if word[i+1] in ['k', 'p','t', 'T', 'f', 'š']:
                template += "Q"
            elif word[i+1] in ['j', 'h', 'v', 's', 'S']:
                template += word[i+1]
            break
        try:
            template += trans_dict[word[i]]
        except:
            return word[i]
    else:
        template += '#'
    if template not in fono_templates:
        try:
            return except_dict[template]
        except:
            return template + " NO"
    return template

def find_fono_templates(word):
    positions = [m.start() for m in re.finditer("<", word)]
    if len(positions) == 0:
        return []
    templates = []
    for position in positions:
        template_str = ''
        for i in range(position+1, len(word)):
            if word[i] == "$":
                template_str += '$'
                if word[i+1] in ['k', 'p','t', 'T', 'f', 'š']:
                    template_str += "Q"
                elif word[i+1] in ['j', 'h', 'v', 's', 'S']:
                    template_str += word[i+1]
                break
            try:
                template_str += trans_dict[word[i]]
            except:
                templates.append(word[i])
        else:
            template_str += '#'
        if template_str not in fono_templates:
            try:
                templates.append(except_dict[template_str])
            except:
                templates.append(template_str + " NO")
        else:
            templates.append(template_str)
                
    return templates

    
def capitalize_letter(word, pos):
    if pos < len(word):
        return word[:pos] + word[pos].upper() + word[pos+1:]
    else:
        return word
        
def capitalize_palatalization_letters(word):
    try:
        if "]" in word:
            pos = word.index("]")
            if pos + 1 <= len(word)-1:
                if word[pos-1] == word[pos+1]:
                    word = capitalize_letter(word, pos+1)
                elif word[pos+1] in ['<', ':', '$', '?'] and word[pos-1] == word[pos+2]:
                    word = capitalize_letter(word, pos+2)
            word = capitalize_letter(word, pos-1)
            word = word.replace("]", "")
    except:
        print("Pallatalization problem with word:" + word)
    return word

def capitalize_palatalization_letters2(word):
    try:
        if "]" in word:
            pos = word.index("]")
            if pos + 1 <= len(word)-1:
                if word[pos-1] == word[pos+1]:
                    word = capitalize_letter(word, pos+1)
                elif word[pos+1] in ['<', ':', '$', '?'] and word[pos-1] == word[pos+2]:
                    word = capitalize_letter(word, pos+2)
            word = capitalize_letter(word, pos-1)
            word = word.replace("]", "")
    except:
        print("Pallatalization problem with word:" + word)
    return word

if __name__ == "__main__":
    
    print(find_fono_templates("s<eis$m<a"))
    
    """
    cases = ['psst','per$v<ers$ne', 'n:är$vi', 's:öök', 's<at$tu', 'k<aar$li', 
             't<in$gi$ma$ta', 't<und$mus', 't<ões$ti', 'k<ast$mi$ne', 
             'm<ees', 'k<üll','k<il]$ju$mi$ne', 'v<as$ta']

    for word in cases:
        word = capitalize_palatalization_letters(word)
        if '<' in word or ':' in word:
            fono_template = find_fono_template(word)
            shift = fono_shift_dict[fono_template]
            print(word, fono_template, shift, shift_colon(word, shift))
        else:
            print(word)
    """