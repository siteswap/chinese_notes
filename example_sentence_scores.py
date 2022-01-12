    # Mutual information - https://lexically.net/downloads/version7/HTML/formulae.html
    # Collocation - a series of words or terms that co-occur more often than would be expected by chance
    # Concordance - list of all examples containing the word
    # Huge list of lexical analysis tools:
    # - https://digitalresearchtools.pbworks.com/w/page/17801708/Text%20Analysis%20Tools
    
    # Example sentence desirata:
    # 1 - Example word should be the lowest (or nearly lowest) frequency word in the sentence s.t. we learn words
    #       in n+1 fashion
    # 2 - Other words in sentence should have high mutual-information i.e. play+soccer is better than like+soccer
    # 3 - Other words in sentence should be already known, but non-trivial s.t. we get to see those lower frequency
    #       words in different contexts. I.e. 咱们 is better than 我 (assuming you already know 咱们).
    # 4 - Similar to point 3, some grammatical variety is good too.
    # 5 - Go for linguistic chunks that often occur like 在这里，我有话给你说，
    # 6 - The phrase should not be too long, but can get longer for more advanced students
    # Current function looks at the rarest word in each sentence and tries to minimzie that.
    # Lexical-chunks & collocations: 想到办法解决的,  这种以为造成意外
    # - these are beautiful, they contain several useful words, with connected meanings, collocations, one phrase!
    # - to find really good ones, get some MI & collocations stats (reverso context offers a few examples)
    # - find "lexical chunks" like 都不会 even though this isn't a word in it's own right

from text_analysis.subtlex import access as subtlex
from catalogue.models import KnownWord


# Previously, we tried to minimize the rarest word, which naturally emphasized short phrases, since
# it's hard to have long phrases without hitting some low-frequency words, but here we are encouraging
# long sentences as a way to catch more high-learning-value words.
# Need to penalize long sentences, as well as overly short sentences
def score_examples_v2(wrd, example):
    phrase_word_counts = get_phrase_word_counts("user")
    ignore_punctuation = '，。？！'
    target_pts = subtlex.word_pts(wrd)
    word_learning_values = []
    for w in example:
        if w in ignore_punctuation:
            continue
        # Estimate comprehension improvement for subsequent occurrences of word
        comprehension_improvement = [0.5, 0.3, 0.2, 0][min(3, phrase_word_counts[w])]
        # Weight comprehension improvement by frequency word comes up
        # Don't reward use of non-target words (aim to build vocab known+1)
        learning_value = comprehension_improvement * subtlex.word_pts(w) if subtlex.word_pts(w) < target_pts else 0
        word_learning_values.append(learning_value)

    # This is the learning value if you learned the whole sentence
    # Obviously learning a very long piece, you will learn more
    # But, this is not the only thing we are learning.
    # It is competing with other phrases for my limited time ...
    total_learning_value = sum(word_learning_values)

    # So, we must also consider EFFICIENCY (the learning value per word, minus some overhead, plus some MI value)
    # Penalize phrases less than 3 words or more than 5:
    ideal_length = 4
    learning_efficiency = total_learning_value / max(1, len(word_learning_values) - ideal_length)
    return learning_efficiency


def get_phrase_word_counts(user):
    word_counter = Counter()
    for obj in KnownWord.objects.get_known_word_cards(user):
        word_counter.update(obj.get_phrase_segmented())
    return word_counter
