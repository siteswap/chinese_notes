import pandas as pd
from text_analysis.subtlex import access as subtlex

df = pd.read_csv('c:/Users/Alex/Desktop/cmn_sentences.tsv', sep='\t')
# Filter out rare hanzi early
valid_chars = set(list(subtlex.HANZI_RANK.keys())[:2000])
valid_chars.update(['，', '。', '！', '？', ' '])

import pynlpir
pynlpir.open()


def contains_rare_words(word, sentence):
    freqs = [subtlex.word_rank(token) for token in pynlpir.segment(sentence, pos_tagging=False) if token not in ['，', '。', '！', '？', ' '] ]
    return max(freqs) > subtlex.word_rank(word)


def get_examples(word):
    df2 = df.loc[df['sentence'].str.contains(word) & (df['sentence'].str.len() < 20)]
    valid_ex = [s for s in df2.sentence.values if valid_chars.issuperset(set(s))]
    valid_ex = [ex for ex in valid_ex if not contains_rare_words(word, ex)]
    return valid_ex


for word in list(subtlex.WORD_RANK.keys())[:1000]:
    print(get_examples(word)[:1])

