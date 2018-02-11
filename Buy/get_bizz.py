import random
bizz = {
        "clothing": {
            "Aerie": " Aerie focuses on intimates and swimwear for teens and young women. But Aerie has one big difference that makes it stand out from competitors: It was the first major brand to ban Photoshop in ad campaigns and deviate from the prototypical model in favor of average women proudly displaying their curves and flaws.",
            "S'Well": "S'well is a reusable water bottle company headquartered in Manhattan, New York. Sarah Kauss founded the company in 2010. Kauss is the CEO of the company.",
            "Tory Burch": "The designer started her eponymous “affordable luxury” brand in 2004 out of her kitchen with borrowed money and built it from the ground up, expanding the business into a $3 billion company with more than 160 stores across the world."
        },
        "software": {
            "Flickr": "Flickr is an image- and video-hosting website and web services suite that was created by Ludicorp in 2004 and acquired by Yahoo on 20 March 2005.", 
            "BlackLine": "BlackLine is an American enterprise software company that develops cloud-based accounting software that helps businesses manage their quarterly financial reports."
        },
        "health and wellness": {
            "The Honest Company" : "The Honest Company is an American consumer goods company, founded by actress Jessica Alba, that emphasizes household products to supply the marketplace for ethical consumerism",
            "Birchbox":"Birchbox is a New York City-based online monthly subscription service that sends its subscribers a box of four to five selected samples of makeup, or other beauty related products.",
            "The Body Shop" : "The Body Shop International Limited, trading as The Body Shop, is a British cosmetics, skin care and perfume company that was founded in 1976 by Dame Anita Roddick.",
            "ProActiv" : "Proactiv, also known as Proactiv Solution, is a brand of skin-care products developed by two American dermatologists, Katie Rodan and Kathy Fields, and launched in 1995"
        }
    }
    
cool_synonyms = ["cool", "interesting", "unique", "innovative"]
def get_bizz():
    return random.choice(list(bizz))
    
def get_bizz_info(key):
    return random.choice(list(bizz[key]))
    
def cool():
    return random.choice(cool_synonyms)
