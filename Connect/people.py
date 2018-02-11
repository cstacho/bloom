import random

directory = {
    "ui design": ["Rita Steele", "Shirley Montoya", "Patricia Braun", "Camille Stacho"],
    "coding": ["Glenda Nethercutt", "Jane Hernandez", "Katherine Tate", "Mollie Evans"],
    "yoga": ["Grace MacGregor","Zhen Juan Tai", "Stefanie Hirsch", "Iliana Cardona"]
    }

def get_mentor(skill):
    return random.choice(list(directory[skill]))
    
def date():
    days=["Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", "Sunday"]
    return random.choice(list(days))