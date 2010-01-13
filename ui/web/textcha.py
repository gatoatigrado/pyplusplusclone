import re
import random
import config

questions = {
    'Which programming language does the pygccxml project mainly use?' : re.compile( '\s*python\s*' )
}

question_keys = questions.keys()
question_keys_len = len(question_keys)

def random_question():
    return question_keys[ random.randrange( question_keys_len ) ]

def is_human( question, answer ):
    if question not in questions:
        return False
    return questions[question].match( answer.lower() )
        
    
