import random


class Constants:
    REWARD_FOR_ENTITY = 10
    RESPONSE_NO_INFORMATION_DISEASE = random.choice(["I am really sorry but i did not find the information. Give me more details about your need to look for it again.",
                                                    'If you can provide more information about it I will appreciate.',
                                                     'I do not have a specific information about it. Please talk me more about it.'])
    RESPONSE_ANY_DISEASE_GIVEN = random.choice(["Please specify the disease, the Orpha code or the CIE10 id which you are interested in. This will help me to understand better your situation. ",
                                                'I did not recognized your disease, try to give me the specific CIE10 id or Orpha code.',
                                                'Sorry, give me the specific name or Orpha code of this disease to be able to provide you more information.'])
    RECURRENT_QUESTION = 'family'
    ANY_INFORMATION_FOUND = random.choice(['Please, provide more information about your doubts such as the area that you would like to be informed treatments, ',
                                           'I am close to be able to help you. Please, give me more information about it.',
                                           'Please, provide more information about your doubts such as the area that you would like to be informed treatments, '])

    PUNTIATION_KWARDS = 1
    PUNTIATION_ENTITIES = 10
    PICTURE = 'melanoma'