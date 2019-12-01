from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import spacy
import numpy as np
from SQLconnection import SqlConnection
from CompareNames import sameNames
from rake_nltk import Rake
from googletrans import Translator
import pycountry
from KeywordExtraction import getKeywords
from GoogleRetriever import getImageFromGoogle
from bot import loadModel, classify
from collectData import loadInfo, languages_dictionary, users_data
from ConstantsPY import Constants
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from telegram.error import TelegramError
from PDF_Routine import create_pdf
from random import randint
from datetime import date

translator = Translator()
nlp = spacy.load('en_core_web_sm')
sql = SqlConnection()
all_data = loadInfo()
history_conversations = dict()


class Response:
    def __init__(self, raw_text, entities, keywords):
        self.raw_text = raw_text
        self.entities = entities
        self.keywords = keywords
        self.recurrent_question_type = None


class Interactions:
    def __init__(self, user_message, bot_response):
        self.user_message = user_message
        self.bot_response = bot_response


class Conversation:
    def __init__(self, user_conv_id):
        self.user_conv_id = user_conv_id
        self.user_nickname = None
        self.interactions = []
        self.disease = None
        self.found_disease = False
        self.language = 'en'


def getData(sql_information):
    response_proposals = []
    for sql_row in sql_information:
        new_data = Response()
        new_data.raw_text = sql_row[2]
        new_data.entities = sql_row[3]
        new_data.keywords = sql_row[4]
        response_proposals.append(new_data)
    return response_proposals


def findDisaseName(list_words, conversation):
    for disease in all_data:
        for word in list_words:
            if word == str(disease.orphan_code) or word == str(disease.cie10) or \
                    sameNames(word, disease.medical_name) or sameNames(word, disease.coloquial_name):
                conversation.disease = disease
                conversation.found_disease = True
    print('found disease', conversation.found_disease)


def compareSimilarityKeywords(list_to_compare, objective_list):
    """
    As much higher the similarity most close in the word-embedding space.
    """
    try:
        similarity_values = []
        for reference_word in objective_list:
            for sample_word in list_to_compare:
                word_reference = wn.synsets(str(reference_word), pos=wn.NOUN)[0]
                word_sample = wn.synsets(str(sample_word), pos=wn.NOUN)[0]
                brown_ic = wordnet_ic.ic('ic-brown.dat')
                similarity_of_lists = word_reference.res_similarity(word_sample, brown_ic)
                if similarity_of_lists >= 0:
                    similarity_values.append(similarity_of_lists)
        if similarity_values:
            mean_keywords_similarity = np.prod(similarity_values) ** (1 / int(len(similarity_values)))
            return mean_keywords_similarity
    except:
        return 0


def getBestResponse(vector_diseases, user_message):
    # Calculate the significance of each DiseaseInfo --> REWARD
    rewards_for_reference = []
    for disease_information in vector_diseases:
        current_reward = 0
        for entity_in_user_message in user_message.entities:
            if entity_in_user_message == disease_information.entity:
                current_reward += Constants.REWARD_FOR_ENTITY
            mean_similarity = compareSimilarityKeywords(user_message.keywords, disease_information.vector_keywords)
            current_reward += mean_similarity
        rewards_for_reference.append(current_reward)
    index_max_reward = np.argmax(rewards_for_reference)
    return vector_diseases[index_max_reward]


def cleanAnswer(response_type):
    if response_type.lower() == 'yes' or response_type.lower() == 'y' or response_type.lower() == 'ye' or \
            response_type.lower() == 'okey' or response_type.lower() == 'ok':
        return 'yes'
    else:
        return 'no'


"""
def recurrentResponses():
    Recurrent situation --> Depends of the last question
    if current_conversation.interactions[0].recurrent_question_type:
        answer_type = cleanAnswer(current_conversation.interactions[0].recurrent_question_typ)
        if answer_type == 'yes':
            pass
        else:
            pass
    if not response_found:
        for entity_predicted in recieved_message.entities:
            print('entities comparison', info_disease.entity, entity_predicted, info_disease.entity == entity_predicted)
            if sameNames(info_disease.entity, entity_predicted):
                print('entities match')
                response = Response(info_disease.text, recieved_message.entities, recieved_message.keywords)
                response_found = True
                break
    if len(current_conversation.disease.vector_disease_info) == 0:  # Any information found for that family
        start_response = Constants.RESPONSE_NO_INFORMATION_DISEASE +\
                         str(current_conversation.disease.family)+". "
        for disease in all_data:
            # Found information about the family
            if current_conversation.disease.family == str(disease.orphan_code) or \
                    current_conversation.disease.family == str(disease.cie10) or \
                    sameNames(current_conversation.disease.family, disease.medical_name) or \
                    sameNames(current_conversation.disease.family, disease.coloquial_name):
                best_response = getBestResponse(disease.vector_disease_info, recieved_message) #returns DiseaseInfo
                response = Response(start_response+best_response.text,
                                    best_response.entity,
                                    best_response.vector_keywords)
    else:
        for disease_information in current_conversation.disease.vector_disease_info:
            pass
            # mean_similarity = compareSimilarityKeywords(recieved_message.keywords, disease_information.vector_keywords)
            # for entity in recieved_message.entities: #Multiple entities can mean  the need of another question

        response = Response(disease_information.text, disease_information.entity,
                            disease_information.vector_keywords)
    response = Response('UHFJHVK', [], [])
    pass
    # current_conversation[1].recurrent_question_type = Constants.RECURRENT_QUESTION
"""


def searchResponse(recieved_message, current_conversation):
    if current_conversation.found_disease:
        response_found = False
        number_keywords_match = 0
        number_entities_match = 0
        number_similarity_match = 0
        puntuation_reference = []
        if current_conversation.disease.vector_disease_info:
            for info_disease in current_conversation.disease.vector_disease_info:
                puntuation_reference = []
                # for article_keyword in info_disease.vector_keywords:
                #     number_similarity_match = compareSimilarityKeywords(info_disease.vector_keywords,
                #                                                         recieved_message.keywords)
                #     for message_keyword in recieved_message.keywords:
                #         if sameNames(article_keyword, message_keyword):
                #             number_keywords_match += 1
                # for entity_predicted in recieved_message.entities:
                #     if sameNames(info_disease.entity, entity_predicted):
                #         number_entities_match += 10
                # global_punctiation = number_keywords_match + number_entities_match + number_similarity_match
                # puntuation_reference.append(global_punctiation)
                # most_matched_response = current_conversation.disease.vector_disease_info[
                #     np.argmax(puntuation_reference)]
                for entity_predicted in recieved_message.entities:
                    if sameNames(info_disease.entity, entity_predicted):
                        response = Response(info_disease.text, recieved_message.entities,
                                            recieved_message.keywords)
                else:
                    index = randint(0, int(len(current_conversation.disease.vector_disease_info)))
                    response = Response(current_conversation.disease.vector_disease_info[index-1].text, recieved_message.entities,
                                        recieved_message.keywords)

            # response = Response(most_matched_response.text, recieved_message.entities, recieved_message.keywords)
        else:
            response = Response(Constants.ANY_INFORMATION_FOUND, [], [])
            current_conversation.found_disease = False

    else:
        response = Response(Constants.RESPONSE_ANY_DISEASE_GIVEN, [], [])
    return response


def sendImagesToTelegram(bot, update, msg, topic_images):
    for image_path in getImageFromGoogle(msg):
        print(image_path)
        try:
            bot.send_photo(chat_id=update.message.chat_id, photo=open(image_path, 'rb'))
        except Exception as e:
            print(str(e))


def identifyLanguage(conversation):
    # Should be connected with the user nickname
    country = users_data[0].country
    language = pycountry.languages.get(name=country).name
    for country_language in languages_dictionary:
        if sameNames(language, country_language):
            conversation.language = languages_dictionary[country_language]
            break


def analyzeMessage(message):
    list_of_keywords = getKeywords(message)
    list_of_entities = classify(message)
    print('prediction', message, list_of_entities)
    return list_of_keywords, list_of_entities


def detectWelcomeGoodbye(message):
    is_welcome = False
    is_goodbye = False
    if sameNames(message, 'bye') or sameNames(message, 'Good bye') or sameNames(message, 'See you soon'):
        is_goodbye = True
    if 'hello' in message.lower():
        is_welcome = True
    return is_welcome, is_goodbye


def sendMessage(bot, update):
    msg = update.message.text
    chat_id = update.message.chat_id
    picture_sent = False
    if sameNames(msg, 'picture') and history_conversations[chat_id].found_disease:
        sendImagesToTelegram(bot, update, Constants.PICTURE, False) #history_conversations[chat_id].disease.coloquial_name
        picture_sent = True
        return
    is_welcome, is_goodbye = detectWelcomeGoodbye(msg)
    if chat_id not in history_conversations:
        print('New conversation')
        new_conversation = Conversation(chat_id)
        history_conversations[chat_id] = new_conversation
        history_conversations[chat_id].user_nickname = 'juanpa'
        # identifyLanguage(history_conversations[chat_id])
    else:
        print('You are already in the list')
    if history_conversations[chat_id].language != 'en':
        message_english = translator.translate(msg, dest='en')
    else:
        message_english = msg
    list_of_keywords, list_of_entities = analyzeMessage(message_english)
    if not history_conversations[chat_id].found_disease:
        findDisaseName(list_of_keywords, history_conversations[chat_id])

    recieved_message = Response(message_english, list_of_entities, list_of_keywords)

    response_to_send = searchResponse(recieved_message, history_conversations[chat_id])

    new_interaction = Interactions(recieved_message, response_to_send)

    history_conversations[chat_id].interactions.append(new_interaction)

    # if history_conversations[chat_id].language != 'en':
    #     response_to_send.raw_text = translator.translate(response_to_send.raw_text,
    #                                                      dest=history_conversations[chat_id].language)
    if not is_goodbye and not picture_sent:
        bot.send_message(chat_id=chat_id, text=response_to_send.raw_text)

    if is_goodbye:  # Close conversation
        illness_id = history_conversations[chat_id].disease.orphan_code
        illness_name = history_conversations[chat_id].disease.coloquial_name
        illness_description = history_conversations[chat_id].interactions[0].user_message.raw_text
        symptoms = history_conversations[chat_id].interactions[0].bot_response.raw_text
        user_data = [['Name:', 'Jose Paco Martinez', 'Pacu2'], ['Contact:', '62475473', 'josepaco@gmail.com'],
                     ['Nationality:', 'France'],
                     ['Gender', 'Male'], ['Age:', '44']]
        illness_data = [['Illness Name', illness_name], ['Illness ID:', illness_id]]
        proposed_solution = history_conversations[chat_id].interactions[0].user_message.raw_text
        create_pdf('informe_pdf', 'Pacu2', user_data, illness_data, illness_description, symptoms)
        bot.send_message(chat_id=chat_id, text=r'Thank you very much, I really appreciate your confidence. I hope to see you very soon. ')
        bot.send_message(chat_id=chat_id, text=r'Here below is attached the summary of our conversation.')
        bot.send_document(chat_id=chat_id, document=open('informe_pdf.pdf', 'rb'))

        history_conversations[chat_id].disease = None
        history_conversations[chat_id].found_disease = False

    # bot.send_photo(chat_id=chat_id, photo=open('test_photo.png', 'rb'))


updater = Updater(token="813089953:AAHOqp5Mt8FfVS64WYUhgtYalt2-c-ILhe4")
# Get the dispatcher to register handlers
dispatcher = updater.dispatcher
# handling callbacks functions to the commands
dispatcher.add_handler(MessageHandler(Filters.text, sendMessage))
loadModel()
updater.start_polling()
