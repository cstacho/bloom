import random

def get_opportunities():
    opps = [
        { "name": "Girls on the Run", "description": "Girls on the Run is a North American non-profit program that works to encourage pre-teen girls to  develop self-respect and healthy lifestyles through dynamic, interactive lessons and running games, culminating in a celebratory 5k run"},
        { "name": "She Should Run", "description": "She Should Run is a non-partisan 501(c)3 that provides an approachable starting place and network for women leaders considering a future run for office and for those who support them. Our mission is to expand the talent pool of women running for office in the United States by providing community, resources, and growth opportunities for aspiring political leaders"},
        { "name": "Girls not Brides", "description":"Members of Girls Not Brides: The Global Partnership to End Child Marriage are committed to ending child marriage, a harmful traditional practice that affects millions of children, predominantly girls, every year. As members of Girls Not Brides, we are joining together to accelerate efforts to prevent child marriage, and to support girls who are or have been married, all over the world."},
        { "name": "Girls Who Code", "description":"At Girls Who Code, we believe the gender gap in technology is an issue we must all come together to solve. With your support, we will continue to build a future where our next generation of girls and boys will prosper through creativity, through bravery, and through teamwork."}
    ]
    return random.choice(opps)
