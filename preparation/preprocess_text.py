import glob
import json
import spacy
from utils import get_text, load_dbnl_data
from itertools import repeat

nlp = spacy.load('nl_core_news_sm', disable=['tok2vec', 'morphologizer', 'tagger', 'parser', 'ner', 'attribute_ruler', 'lemmatizer'])
nlp.add_pipe('sentencizer')
nlp.max_length = 6_000_000


def select_sentences(paths):
    "Select sentences from files located in PATHS with a specific number of syllables."
    sent_index = dict()
    for path in paths:
        print(path)
        base_name = path.split('/')[-1].split('.')[0]
        text = get_text(path)
        doc = nlp(text)
        relevant_sentences = []
        for sentence in doc.sents:
            if sentence.text.endswith("?"):
                relevant_sentences.append(sentence.text)
        sent_index[base_name] = relevant_sentences
    return sent_index


paths = glob.glob('./proza/*.epub')
sent_index = select_sentences(paths)
with open('resources/selected_sentences.json','w') as f:
    json.dump(sent_index, f, indent=4)