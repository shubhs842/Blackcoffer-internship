import pandas as pd
import re
import nltk
from nltk.corpus import opinion_lexicon
from nltk.tokenize import word_tokenize, sent_tokenize

# Ensure required resources are downloaded
nltk.download('opinion_lexicon')
nltk.download('punkt')


## Dependencies

- requests
- beautifulsoup4
- pandas
- openpyxl
- nltk


# Load positive and negative words
positive_words = set(opinion_lexicon.positive())
negative_words = set(opinion_lexicon.negative())

# Function to calculate positive score
def positive_score(text):
    words = word_tokenize(text)
    return sum(1 for word in words if word.lower() in positive_words)

# Function to calculate negative score
def negative_score(text):
    words = word_tokenize(text)
    return sum(1 for word in words if word.lower() in negative_words)

# Function to calculate polarity score
def polarity_score(pos_score, neg_score):
    return (pos_score - neg_score) / ((pos_score + neg_score) + 0.000001)

# Function to calculate subjectivity score
def subjectivity_score(text, pos_score, neg_score):
    words = word_tokenize(text)
    return (pos_score + neg_score) / (len(words) + 0.000001)

# Function to calculate average sentence length
def avg_sentence_length(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    return len(words) / len(sentences)

# Function to calculate percentage of complex words
def percentage_complex_words(text):
    words = word_tokenize(text)
    complex_words = sum(1 for word in words if syllable_count(word) >= 3)
    return (complex_words / len(words)) * 100

# Function to calculate Fog index
def fog_index(avg_sentence_length, percentage_complex_words):
    return 0.4 * (avg_sentence_length + percentage_complex_words)

# Function to calculate average number of words per sentence
def avg_words_per_sentence(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    return len(words) / len(sentences)

# Function to count complex words
def complex_word_count(text):
    words = word_tokenize(text)
    return sum(1 for word in words if syllable_count(word) >= 3)

# Function to count total words
def word_count(text):
    words = word_tokenize(text)
    return len(words)

# Function to calculate syllables per word
def syllable_per_word(text):
    words = word_tokenize(text)
    return sum(syllable_count(word) for word in words) / len(words)

# Function to count personal pronouns
def personal_pronouns(text):
    pronouns = ['I', 'we', 'my', 'ours', 'us']
    words = word_tokenize(text)
    return sum(1 for word in words if word in pronouns)

# Function to calculate average word length
def avg_word_length(text):
    words = word_tokenize(text)
    return sum(len(word) for word in words) / len(words)

# Helper function to count syllables in a word
def syllable_count(word):
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

# Read the extracted articles
articles_dir = 'articles'
articles = []
for filename in os.listdir(articles_dir):
    with open(os.path.join(articles_dir, filename), 'r', encoding='utf-8') as file:
        articles.append((filename.split('.')[0], file.read()))

# Compute variables for each article
output = []
for url_id, text in articles:
    pos_score = positive_score(text)
    neg_score = negative_score(text)
    pol_score = polarity_score(pos_score, neg_score)
    subj_score = subjectivity_score(text, pos_score, neg_score)
    avg_sent_len = avg_sentence_length(text)
    pct_complex_words = percentage_complex_words(text)
    fog_idx = fog_index(avg_sent_len, pct_complex_words)
    avg_words_sent = avg_words_per_sentence(text)
    comp_word_count = complex_word_count(text)
    word_count_total = word_count(text)
    syll_per_word = syllable_per_word(text)
    pers_pronouns = personal_pronouns(text)
    avg_word_len = avg_word_length(text)

    output.append({
        'URL_ID': url_id,
        'POSITIVE SCORE': pos_score,
        'NEGATIVE SCORE': neg_score,
        'POLARITY SCORE': pol_score,
        'SUBJECTIVITY SCORE': subj_score,
        'AVG SENTENCE LENGTH': avg_sent_len,
        'PERCENTAGE OF COMPLEX WORDS': pct_complex_words,
        'FOG INDEX': fog_idx,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_words_sent,
        'COMPLEX WORD COUNT': comp_word_count,
        'WORD COUNT': word_count_total,
        'SYLLABLE PER WORD': syll_per_word,
        'PERSONAL PRONOUNS': pers_pronouns,
        'AVG WORD LENGTH': avg_word_len
    })

# Convert to DataFrame
output_df = pd.DataFrame(output)

# Read the input file again to merge with the output
df_input = pd.read_excel('Input.xlsx')
df_output = df_input.merge(output_df, on='URL_ID')

# Save the output to an Excel file
df_output.to_excel('Output Data Structure.xlsx', index=False)
