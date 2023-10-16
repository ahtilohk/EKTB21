# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 22:45:02 2023

Added analyses mesting
Separate syllabification of the parts of a compound word
Text from corpus's files

@author: Ahti Lohk
"""
from estnltk import Text
from estnltk.vabamorf.morf import synthesize
from estnltk.vabamorf.morf import syllabify_word
from fonotemplates_library import capitalize_palatalization_letters
from fonotemplates_library import find_fono_templates, shift_colons, fono_shift_dict
from list_of_sentences_in_subfolders_files_library import find_all_sentences
import re

def choose_correct_morph_synthesis_seq_index(word, morph_synthesis):
    seq_index = -1
    for i, m in enumerate(morph_synthesis):
        clean_mp = re.sub("[^a-zA-Zõäöüšž]", "" ,m.lower())
        if clean_mp == word.lower():
            seq_index = i
            break
    return  0 if seq_index == -1 else seq_index

def replace_in_pos(word, pos, replacement):
    return word[:pos] + replacement + word[pos+1:]

def correct_syllable_with_question_mark(word):
    if '?' not in word:
        return word
    else:
        syllables = word.split('$')
        for i in range(len(syllables)):
            if '?' in syllables[i]:
                if syllables[i][0] == '"':
                    syllables[i] = syllables[i][1:]
                if syllables[i][0] != '%':
                    syllables[i] = '%' + syllables[i]
                syllables[i] = syllables[i].replace('?', '')
        corrected_word = '$'.join(syllables)
        return corrected_word

def correct_accents(input_word):
    word = input_word[:]
    pattern = r'[%\"]'
    accent_poses = [match.start() for match in re.finditer(pattern, word)]
    accent_symbols = [word[accent_pos] for accent_pos in accent_poses]
    
    nr_of_syls = len(accent_poses) 
    
    if nr_of_syls > 1:
        replacements = [''] * nr_of_syls
        first_accent_flag = False
        
        
        if accent_symbols[0] == '%':
            replacements[0] = '%'
            first_accent_flag = True
        if accent_symbols[0] == '"':
            replacements[0] = '"'
        if accent_symbols[1] == '%':
            if first_accent_flag:
                replacements[1] = '"'
            else:
                replacements[1] = '%'
                first_accent_flag = True
        
        if nr_of_syls > 3:
            for i in range(2, len(accent_symbols)):
                if (i + 1) % 2 != 0 and i + 1 != nr_of_syls: 
                    if not first_accent_flag:
                        replacements[i] = '%'
                        first_accent_flag = True
                    else:
                        replacements[i] = '"'
        
        for i in range(len(accent_poses)-1, -1, -1):
            position = accent_poses[i]
            replacement = replacements[i]
            word = replace_in_pos(word, position, replacement)
    
    
    return correct_syllable_with_question_mark(word)

def separate_first_part(word_part, compound)->str:
  i = 0
  j = 0
  
  if word_part == "üks" and "h" in compound:
     word_part = "ühe"
      
  if word_part == "kaks" and "h" in compound:
     word_part = "kahe"
      
  if word_part == "lapse" and "t" in compound:
     word_part = "laste"

  if word_part == "neli" and compound[:5] == "nelja":
     word_part = "nelja"
   
  if word_part == "viis" and compound[:4] == "viie":
     word_part = "viie"
     
  if word_part == "kuus" and compound[:4] == "kuue":
     word_part = "kuue"
 
  if word_part == "seitse" and compound[:5] == "seitsme":
     word_part = "seitsme"
           
  while i < len(word_part) and j < len(compound):
    if word_part[i].lower() == compound[j].lower():
      i += 1
    j += 1
  return compound[:j]
 
    
def find_word_parts(compound, compound_with_borders)->list:
    no_letter_patern = "[^a-zA-ZõäöüÕÄÖÜšžŠŽ]"
    word_parts = compound_with_borders.split("_")
    word_parts_list = []
    for i in range(len(word_parts)-1):
        word = re.sub(no_letter_patern, "", word_parts[i])
        first_part = separate_first_part(word, compound)
        word_parts_list.append(first_part)
        compound = compound[len(first_part):]
    if len(compound) > 0:
        word_parts_list.append(compound)
    return word_parts_list


def combine_analyses(word1: str, word2: str) -> str:
    result = ""
    i1 = 0
    i2 = 0
    while True:
        if i1 < len(word1) and word1[i1] in ['%', '$', '"']:
            result += word1[i1]
            i1 += 1
        elif i2 < len(word2) and word2[i2] in ['<', ']', '?']:
            result += word2[i2]
            i2 += 1
        elif i1 < len(word1) and i2 < len(word2) and word1[i1].lower() == word2[i2].lower():
            result += word2[i2]
            i1 += 1
            i2 += 1
        else:
            break
    return result


def make_morpho_phonetic_analyse_for_words(sentence_list):

    # input: list of sentences
    # output: list of morpho-phoneticly analysed words 
    accent_dict = {0: '"', 1: '%'}
    result_list = []
    for sentence in sentence_list:
        #print()
        #print(sentence)
        txt = Text(sentence)
        txt.tag_layer(['morph_analysis', 'compound_tokens'])
        
        from estnltk.taggers import VabamorfTagger
        vm_phonetic=VabamorfTagger(output_layer='morph_phonetic', phonetic=True)
        vm_phonetic.tag(txt)
        
        # === BEGIN CORRECTIONS ===
        
        my_corrections = {
            'üheteistkümne': {'root': 'üks_teist_kümmend', 'lemma': 'üksteistkümmend', 
                               'partofspeech': 'N'},
            'kaheteistkümne': {'root': 'kaks_teist_kümmend', 'lemma': 'kaksteistkümmend', 
                               'partofspeech': 'N'},
            'kolmeteistkümne': {'root': 'kolm_teist_kümmend', 'lemma': 'kolmteistkümmend', 
                               'partofspeech': 'N'},
            'neljateistkümne': {'root': 'neli_teist_kümmend', 'lemma': 'neliteistkümmend', 
                               'partofspeech': 'N'},
            'viieteistkümne': {'root': 'viis_teist_kümmend', 'lemma': 'viisteistkümmend', 
                               'partofspeech': 'N'},
            'kuueteistkümne': {'root': 'kuus_teist_kümmend', 'lemma': 'kuusteistkümmend', 
                               'partofspeech': 'N'},
            'seitsmeteistkümne': {'root': 'seitse_teist_kümmend', 'lemma': 'seitseteistkümmend', 
                               'partofspeech': 'N'},
            'kaheksateistkümne': {'root': 'kaheksa_teist_kümmend', 'lemma': 'kaheksateistkümmend', 
                               'partofspeech': 'N'},
            'üheksateistkümne': {'root': 'üheksa_teist_kümmend', 'lemma': 'üheksateistkümmend', 
                               'partofspeech': 'N'},
            'kolmekümne': {'root': 'kolme_kümne', 'partofspeech': 'N'},
            'viiekümne': {'root': 'viie_kümne', 'partofspeech': 'N'},
            'kuuekümne': {'root': 'kuue_kümne', 'partofspeech': 'N'},
            'seitsmekümne': {'root': 'seitsme_kümne', 'partofspeech': 'N'}
            }
        
        from estnltk.taggers import UserDictTagger
        userdict = UserDictTagger(output_layer='morph_phonetic', words_dict = my_corrections, ignore_case=True )
        
        userdict.retag(txt)
        #print(text.morph_analysis)
        
        # Konverteerime json-iks ja tagasi, see peaks nullima puhvris olevad tulemused
        from estnltk.converters import text_to_json, json_to_text
        txt = json_to_text(text_to_json(txt))
        
        # === END CORRECTIONS ===
        
        
        sentences = txt.sentences
        
        #error_f_temp_dict = dict()
        for j, sent in enumerate(sentences):
            m_p = sent.morph_phonetic.root
            
            #morf_phonetics = [morph_phonetic[0] for morph_phonetic in sent.morph_phonetic.root]
            words = [word.lower() for word in sent.text]
            
            lemmas = [l[0].lower() for l in sent.lemma]
            postags = [p[0] for p in sent.partofspeech]
            forms = [f[0] for f in sent.form]
            clitics = [c[0] for c in sent.clitic]
            
            for i, lemma in enumerate(lemmas):
                if lemma in '"()[]{}':
                    pass
                elif any(char.isdigit() for char in lemma):
                    pass
                elif postags[i] == 'Z':
                    #print(f"<{lemma}>")
                    result_list.append(f"<{lemma}>")
                    
                    pass
                else:
                    morph_synthesis = synthesize(lemma, form=forms[i], partofspeech=postags[i], phonetic=True)
                    nr_of_synthesis = len(morph_synthesis)
                    
                    seq_index = 0
                    if nr_of_synthesis > 1:
                        seq_index = choose_correct_morph_synthesis_seq_index(words[i], morph_synthesis)
                     
                    if len(morph_synthesis) > 0:
                        final_morph_synthesis = morph_synthesis[seq_index] + clitics[i] if clitics[i] != "" else morph_synthesis[seq_index]
        
                    else:
                        clean_m_p = re.sub("[<\?\]]", "", m_p[i][0])
        
                        if words[i] == clean_m_p:
                            morph_synthesis = [words[i]]
                        else:
                            morph_synthesis = [words[i]]
                        final_morph_synthesis = morph_synthesis[0]
                        
                    syl_word_parts = []
                    if '_' in m_p[i][0]:
                        word_parts = find_word_parts(final_morph_synthesis, m_p[i][0])
                        
                        word_parts_for_syl = find_word_parts(words[i], m_p[i][0])
                        for word_part_for_syl in word_parts_for_syl:
                        
                            syllables = syllabify_word(word_part_for_syl)
                            syllabified_word_part = "$".join([accent_dict[syllable["accent"]] + syllable["syllable"] for syllable in syllables])
                            syllabified_word_part = correct_accents(syllabified_word_part)
                            syl_word_parts.append(syllabified_word_part)
                        
                    else:
                        syllables = syllabify_word(words[i])
                        syllabified_word = "$".join([accent_dict[syllable["accent"]] + syllable["syllable"] for syllable in syllables])
                        syllabified_word = correct_accents(syllabified_word)
                        syl_word_parts.append(syllabified_word)
                        
                        word_parts = [final_morph_synthesis]
                    
                    for ii, word_part in enumerate(word_parts):
                        try:
                            pal_word_part = capitalize_palatalization_letters(word_part)
                            comb_word = combine_analyses(syl_word_parts[ii], pal_word_part)
                            
                            if '<' in comb_word or ':' in comb_word:
                                
                                fono_templates = find_fono_templates(comb_word.lower())
                                
                                shifts = []
                                for fono_template in fono_templates:
                                    shift = fono_shift_dict[fono_template]
                                    shifts.append(shift)
                                
                                comb_word = shift_colons(comb_word, shifts)
                            word_analyse = comb_word if comb_word[0] != '$' else comb_word[1:]
                            result_list.append(word_analyse)    
                        except:
                            pass
    return result_list

def find_len_of_sentences(sentences):
    sent_len_dict = dict()
    pattern = "[a-zA-ZäöõüÕÄÖÜšžŠŽ]+"
    for sentence in sentences:
        words = re.findall(pattern, sentence)
        sent_len = len(words)
        sent_len_dict[sent_len] = sent_len_dict.get(sent_len, 0) + 1
    return sent_len_dict


def phones_syllables_statics(word_analyse_list, phonemes):
    syl_stat_dict = dict()
    
    phonemes_or_expression = "(" + "|".join(phonemes) + ")"
    phoneme_stat_dict = dict.fromkeys(phonemes, 0)
    
    palat_replacements = {"T": "t'","S": "s'","N": "n'","L": "l'","D": "d'"}
    
    for token in word_analyse_list:
        if "<" not in token[0]:
            nr_of_syllables = token.count("$") + 1
            syl_stat_dict[nr_of_syllables] = syl_stat_dict.get(nr_of_syllables, 0) + 1
            
            new_token = ''.join(palat_replacements.get(c, c) for c in token)
            found_phonemes = re.findall(phonemes_or_expression, new_token)
            
            for phoneme in found_phonemes:
                phoneme_stat_dict[phoneme] += 1
            
    return syl_stat_dict, phoneme_stat_dict
    

if __name__ == "__main__":
    path = r'C:\Users\kasutaja\Documents\Ahti\Liisi projekt\Tasakaalus_korpus\\' 
    
    phonemes = ["ü:", "ü", "ö:", "ö", "ä:", "ä", "õ:", "õ", "v:", "w", "v", 
                "u:", "u", "t':", "t:", "t'", "t", "ž:", "ž", "š:", "š", 
                "s':", "s:", "s'", "s", "r:", "r", "p:", "p", "o:", "o", 
                "ng:", "ng", "n':", "n:", "n'", "n", "m:", "m", 
                "l':", "l:", "l'", "l", "k:", "k", "j:", "j", "i:", "i", 
                "h:", "h", "g", "f:", "f", "e:", "e", "d'", "d", "b", "a:", "a"]
    
    phonemes_or_expression = "(" + "|".join(phonemes) + ")"
    phoneme_dict = dict.fromkeys(phonemes, 0)
    
    diphthongs = ["üo", "üi:", "üi", "üe", "üa", "öi:", "öi", "öe:", "öa:", 
                  "äu:", "äu", "äo:", "äi:", "äi", "äe:", "äe", "õu:", "õu", 
                  "õo:", "õi:", "õi", "õe:", "õe", "õa:", "uo", "ui:", "ui", 
                  "ue", "ua", "ou:", "ou", "oi:", "oi", "oe:", "oe", "oa:", 
                  "iu:", "iu", "io", "ie", "ia", "eu", "eo:", "ei:", "ei", 
                  "ea:", "ea", "au:", "au", "ao:", "ai:", "ai", "ae:", "ae"]
    
    diphthongs_or_expression = "(" + "|".join(diphthongs) + ")"
    diphthong_dict = dict.fromkeys(diphthongs, 0)
    
    sentence_list = find_all_sentences(path)
    
    #print(len(sentence_list))
    #print(sentence_list[:10])
    
    word_analyse_list = make_morpho_phonetic_analyse_for_words(sentence_list[:1000])
    #print(word_analyse_list)
    
    sent_len_dict = find_len_of_sentences(sentence_list)
    
    print("\nSTATISTICS OF SENTENCES")
    print(sent_len_dict)
    #sorted_sent_len = sorted(sent_len_dict.keys())
    #for key in sorted_sent_len:
    #    print(key, sent_len_dict[key])
    
    
    syl_stat_dict, phoneme_stat_dict = phones_syllables_statics(word_analyse_list, phonemes)
    print("\nSTATISTICS OF SYLLABLES")
    print(syl_stat_dict)
    print("\nSTATISTICS OF PHONEMS")
    print(phoneme_stat_dict)