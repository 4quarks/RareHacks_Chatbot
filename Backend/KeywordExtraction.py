from SQLconnection import SqlConnection
from rake_nltk import Rake
import regex as re

sql = SqlConnection()


def getKeywords(text):
    r = Rake()  # Uses stopwords for english from NLTK, and all puntuation characters.

    r.extract_keywords_from_text(text)
    list_keywords_scored = r.get_ranked_phrases_with_scores()
    list_keywords = []
    for keyword_scored in list_keywords_scored:
        list_keywords.append(keyword_scored[1])
    return list_keywords


def updateKeywordsDB():
    data_diseases = sql.select("SELECT * FROM diseases")

    for row in data_diseases:
        keywords = ";".join(getKeywords(cleanTextDB(row[2])))
        print(keywords)
        sql.update("UPDATE diseases SET keywords = '{}' WHERE id = {}".format(keywords, row[0]))


def cleanTextDB(text):
    character_replace_exceptions = ["-"]
    text_result = ""
    for character in text:
        if character.isalnum() or character in character_replace_exceptions or character == ' ':
            text_result += character
    return text_result


# updateKeywordsDB()
# print(getKeywords('what is the AA amyloidosis?'))
