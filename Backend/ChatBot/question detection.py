from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk

sentence = 'Usually I go to the hospital when I am afraid. When I sould go there?'

sentences_splitted = sent_tokenize(sentence)
sentence_words_splitted = [word_tokenize(s) for s in sentences_splitted]
question = [ne_chunk(pos_tag(s)) for s in sentences_splitted]
labeled_sentence = []
helping_verbs = ['is', 'am', 'are', 'was', 'were', 'be', 'being', 'been', 'has', 'have', 'had', 'do', 'does', 'did',
                 'will', 'shall', 'should', 'would']
for sentence in sentence_words_splitted:
    if 'wh' in sentence[0] or '?' in sentence[-1] or sentence[0] in helping_verbs:  # First word is where, when, which, who, what... and not helping verbs in the first word
        labeled_sentence.append(sentence)

