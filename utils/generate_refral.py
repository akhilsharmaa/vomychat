import random
import string

def generate_referral():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
