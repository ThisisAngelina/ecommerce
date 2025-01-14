import random
import string



def generate_slug():
    ''' needed to generate a url slug out of a model instance name '''
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))