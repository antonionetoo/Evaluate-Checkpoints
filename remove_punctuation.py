
import nltk

def remove_contractions(phrase):
    tokens = nltk.word_tokenize(phrase)
    tokens = [t for t in tokens if t.strip()]

    index = [i for i, t in enumerate(tokens) if t == "'s"]

    if index:
        tags = nltk.pos_tag(tokens)

        for i in index:
            if tags[i][1] == 'VBZ':
                tokens[i] = 'is'
    
    return ' '.join(tokens)

def remove(phrase):
    puctutation = [['.', ''], 
                   ['"', ''], 
                   [',', ''], 
                   [':', ''],
                   ['(', ''],
                   [')', ''],
                   ['\n', '']
                   ]

    for p in puctutation:
        phrase = phrase.replace(p[0], p[1])

    return remove_contractions(phrase)