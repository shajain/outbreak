import pdb
import numpy as np
import spacy
from Levenshtein import distance
from itertools import compress



def matchingPairs(ob2Names, OBKeys=None):
    OB = list(ob2Names.keys())
    #K1 = []]
    #pdb.set_trace()
    if OBKeys is not None:
        #OB = compress(OB, [i in ix for i in range(len(OB))])
        OB = OBKeys
        # for i in ix:
        #     K1.append(OB[i])
        #OB = K1
    ob2Names = {ob: ob2Names[ob] for ob in OB}
    outDict = {ob:[] for ob in OB}
    ob2Names2 = removeExtraneous(ob2Names)
    OB = list(ob2Names2.keys())
    #pdb.set_trace()
    for i in np.arange(len(OB)):
        if i % 25==0:
            print(i)
        outDict[OB[i]] = {}
        for j in np.arange(i+1, len(OB)):
            #print(i, 'matching ', j)
            match, noMatch = findMatching(ob2Names2[OB[i]], ob2Names2[OB[j]])
            if len(match) > 0:
                print(i,':',OB[i], '   ', j, ':', OB[j], ' match')
                outDict[OB[i]][OB[j]] = match
    #pdb.set_trace()
    return outDict


def findMatching(str1List, str2List):
    # if (type(str1List) is not list) or (type(str2List) is not list):
    #     return [], []
    # if (not isinstance(str1List[0], str)) or (not isinstance(str2List[0], str)):
    #     return [], []
    # if str1List[0] == 'None' or  str2List[0] == 'None':
    #     return [], []
    match = []
    noMatch = []
    for (i, str1_prc) in enumerate(str1List):
        for (j, str2_prc) in enumerate(str2List):
            res = align(str1_prc, str2_prc)
            #pdb.set_trace()
            if res['match']:
                match.append({'i': int(i), 'j': int(j), 'diff': int(res['diff'])})
            else:
                noMatch.append({'i': int(i), 'j': int(j), 'diff': int(res['diff'])})
    return match, noMatch


def align(str1_prc, str2_prc):
    if len(str1_prc) == 0 or len(str2_prc) == 0:
        return {'match':False, 'diff':100}
    match1 = np.array(matchWords(str1_prc, str2_prc))
    match2 = np.array(matchWords(str2_prc, str1_prc))
    diff1 = match1.size - np.sum(match1)
    diff2 = match2.size - np.sum(match2)
    if ((match1.size > 3 and diff1 <= 1) or diff1 == 0) and \
        ((match2.size > 3 and diff2 <= 1) or diff2 == 0):
        return {'match': True, 'diff': diff1 + diff2}
    else:
        return {'match': False, 'diff': diff1 + diff2}


def removeExtraneous(ob2Names):
    nlp = spacy.load("en_core_web_sm")
    K = list(ob2Names.keys())
    ob2Names2 = {}
    for k in K:
        names = ob2Names[k]
        names_prc = []
        if type(names) is list and len(names)>0:
            names_prc = []
            for name in names:
                if isinstance(name,str) and name != 'None':
                    name_prc = nlp(name)
                    #pdb.set_trace()
                    ws = []
                    for w in name_prc:
                        if w.pos_ not in ['ADP', 'PUNCT', 'CCONJ', 'SPACE', 'AUX', 'DET', 'INTJ', 'PART', 'PRON', 'SCONJ', 'SYM', 'X']:
                            ws.append(w)
                    names_prc.append(ws)
            if len(names_prc) > 0:
                ob2Names2[k] = names_prc
    return ob2Names2

def matchWordsL(str1_prc, str2_prc):
    match = [False]*len(str1_prc)
    #pdb.set_trace()
    for (i,s1) in enumerate(str1_prc):
        for s2 in str2_prc:
            if distance(str(s1), str(s2)) == 0:
                match[i] = True
                break
    return match

def matchWords(str1_prc, str2_prc):
    match = [False]*len(str1_prc)
    #pdb.set_trace()
    for (i,s1) in enumerate(str1_prc):
        for s2 in str2_prc:
            if str(s1).lower() == str(s2).lower():
                match[i] = True
                break
    return match

