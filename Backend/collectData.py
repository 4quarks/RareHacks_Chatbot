import unicodedata
from SQLconnection import SqlConnection
import numpy as np

sql = SqlConnection()


class DiseaseInfo:
    def __init__(self):
        self.text = None
        self.entity = None
        self.vector_keywords = []
        self.family = None
        self.reference = None


class Disease:
    def __init__(self):
        self.orphan_code = None
        self.cie10 = None
        self.medical_name = None
        self.coloquial_name = None
        self.vector_disease_info = []


class User:
    def __init__(self):
        self.name = None
        self.surname = None
        self.mail = None
        self.country = None
        self.phone_number = None
        self.share_contact = False
        self.share_info = False
        self.update_news = False


def getDesiredDisease(name_id):
    unicodedata.normalize('NFC', string1) == unicodedata.normalize('NFC', string2)


# print(unicodedata.normalize('NFC', 'lAussane'.lower()) == unicodedata.normalize('NFC', '/lAussanE'.lower()))


def loadInfo():
    global_table = sql.select(
        "select d.name as name_medical, d.text,d.entity,d.keywords,d.family,d.reference,d_id.ORPHA,d_id.CIE10,d_id.name as name_coloquial from diseases d inner join diseases_id d_id on d_id.ORPHA=d.orpha")
    all_diseases = []
    code_orpha = []
    [code_orpha.append(sample[6]) for sample in global_table]
    unique_orpha_ids = np.unique(code_orpha)
    for disease_orpha_id in unique_orpha_ids:
        new_disease = Disease()
        for sample in global_table:
            if sample[6] == disease_orpha_id:
                new_disease_information = DiseaseInfo()
                new_disease_information.entity = sample[2]
                new_disease_information.family = sample[4]
                new_disease_information.reference = sample[5]
                new_disease_information.text = sample[1]
                new_disease_information.vector_keywords = sample[3].split(';')
                new_disease.vector_disease_info.append(new_disease_information)
                new_disease.cie10 = sample[7]
                new_disease.coloquial_name = sample[8]
                new_disease.medical_name = sample[0]
                new_disease.orphan_code = sample[6]

        all_diseases.append(new_disease)
    return all_diseases


def loadUsers():
    all_users = []
    users_data = sql.select("SELECT * FROM users ")
    for user_data in users_data:
        new_user = User()
        new_user.name = user_data[1]
        new_user.surname = user_data[2]
        new_user.mail = user_data[3]
        new_user.country = user_data[4]
        new_user.phone_number = user_data[5]
        new_user.share_contact = user_data[6]
        new_user.share_info = user_data[7]
        new_user.update_news = user_data[8]
        all_users.append(new_user)
    return all_users

all_diseases = loadInfo()

users_data = loadUsers()

f = open("languages.txt", "r")
a = f.read().split(';')
languages_dictionary = {}
for country in a:
    country, language = country.split('-')
    languages_dictionary.update({country: language})

if __name__ == "__main__":
    pass
