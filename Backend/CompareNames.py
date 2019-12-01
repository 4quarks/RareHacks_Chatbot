import unidecode
import math

def processNameForCorrectFormat(name):
    name_processed = unidecode.unidecode(name).strip()
    name_processed = name_processed.replace('-', ' ')
    name_processed = getCorrectNameForSurnameCommaName(name_processed)
    return name_processed


def unidecodeToUtf8(unicode_string):
    return unidecode.unidecode(unicode_string)


def namesHave2CommonWords(name, name_to_compare):
    components_name = name.split(" ")
    components_name_to_compare = name_to_compare.split(" ")
    num_common_words = 0

    for component_name in components_name:
        if component_name in components_name_to_compare:
            num_common_words += 1
            # print(component_name+" esta en "+ name_to_compare)

    return num_common_words >= 2


def nameContainsTheOtherName(name, name_to_compare):
    return name in name_to_compare or name_to_compare in name


# Ejemplo:  Verdasco F. (Fernando Verdasco)
def surnameInitialLetterNamePoint(name_sql, name_website):
    same_name = False
    if '.' in name_website:
        full_surname_sql = name_sql.split(" ")[-1].strip()
        full_surname_website = name_website.split(" ")[0].strip()
        initial_letter_name_sql = name_sql.split(" ")[0][0]
        position_initial_letter_name_website = name_website.find('.') - 1
        initial_letter_name_website = name_website[position_initial_letter_name_website]

        same_name = initial_letter_name_website == initial_letter_name_sql and \
                    full_surname_sql == full_surname_website

    return same_name


# Ejemplo:  Verdasco, Fernando (Fernando Verdasco)
def getCorrectNameForSurnameCommaName(name_website):
    if ',' in name_website:
        components_name_website = name_website.split(",")
        if len(components_name_website) >= 2:
            name_website = components_name_website[1] + " " + components_name_website[0]

    return name_website


# para betfair
def initialLetterNameSurname(name_sql, name_website):
    same_name = False
    all_words_name_website = name_website.split(' ')
    first_word_name_website = name_website.split(' ')[0].strip().replace('.', '')
    all_words_name_sql = name_sql.split(' ')
    if len(first_word_name_website) == 1:
        first_letter_name_sql = all_words_name_sql[0][0]
        same_name = first_word_name_website == first_letter_name_sql \
                    and all_words_name_sql[-1].strip() == all_words_name_website[-1].strip()

        # print("sql", all_words_name_sql[-1].strip(),"web",all_words_name_website[-1].strip(),same_name)

    return same_name


def sameNames(name_db, name_to_compare, flexible_comparison=True):
    """
    Function that compare the names to see if they are equal.
    Args
        name_db: string with the name saved in the database.
        name_to_compare: string of the name scraped.
        flexible_comparison:
    Return
        same_name: Boolean indicator if the names are equal or not.
    """
    same_name = False
    try:
        if name_db is not None and name_to_compare is not None:
            name_db = processNameForCorrectFormat(name_db).lower()
            name_to_compare = processNameForCorrectFormat(name_to_compare).lower()
            same_name = name_db == name_to_compare or nameContainsTheOtherName(name_db, name_to_compare)
            if not same_name and flexible_comparison:
                same_name = namesHave2CommonWords(name_db, name_to_compare) \
                            or surnameInitialLetterNamePoint(name_db, name_to_compare) \
                            or initialLetterNameSurname(name_db, name_to_compare)
    except:
        pass
    return same_name
