from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Category, CatItem, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(name='abdo', email='ar1813@fayoum.edu.eg')

category1 = Category(name="Basketball")

session.add(category1)
session.commit()


catItem1 = CatItem(title="Basketball ball ", description='''A basketball is a
                   spherical ball used in basketball games. Basketballs
                   typically range in size from very small promotional
                   items only a few inches in diameter to extra large balls
                   nearly a foot in diameter used in training exercises.
                   For example, a youth basketball could be 27 inches (69 cm)
                   in circumference, while a National Collegiate Athletic
                   Association (NCAA) men's ball would be a maximum of 30
                   inches (76 cm) and an NCAA women's ball would be a maximum
                   of 29 inches (74 cm)''',
                   category=category1, user=user1)

session.add(catItem1)
session.commit()

catItem3 = CatItem(title="Ring", description='''A backboard is a piece of
                   basketball equipment. It is a raised vertical board with
                   an attached basket consisting of a net suspended from a
                   hoop. It is made of a flat, rigid piece of, often Plexiglas
                   or tempered glass which also has the properties of safety
                   glass when accidentally shattered. It is usually
                   rectangular as used in NBA, NCAA and international
                   basketball. In recreational environments, a backboard may
                   be oval or a fan-shape, particularly in non-professional
                   games.''',
                   category=category1, user=user1)

session.add(catItem3)
session.commit()


category2 = Category(name="Volleyball")

session.add(category2)
session.commit()


catItem1 = CatItem(title="Volleyball ball", description='''A volleyball is a
                   ball used to play indoor volleyball, beach volleyball,
                   or other less common variations of the sport. Volleyballs
                   are round and traditionally consist of eighteen nearly
                   rectangular panels of synthetic or genuine leather, arranged
                   in six identical sections of three panels each, wrapped
                   around a bladder. However, in 2008, the FIVB adopted as its
                   official indoor ball a new Mikasa with dimples and only
                   eight panels for a softer touch and truer flight. A
                   valve permits the internal air pressure to be adjusted.''',
                   category=category2, user=user1)

session.add(catItem1)
session.commit()

catItem2 = CatItem(title="Volleyball Antenna", description='''An antenna is
                   placed on each side of the net perpendicular to the
                   sideline and is a vertical extension of the side boundary
                   of the court. A ball passing over the net must pass
                   completely between the antennae (or their theoretical
                   extensions to the ceiling) without contacting them''',
                   category=category2, user=user1)

session.add(catItem2)
session.commit()

catItem2 = CatItem(title="Volleyball Net", description=''' the high net that
                   separates the two teams and over which the volleyball must
                   pass''',
                   category=category2, user=user1)

session.add(catItem2)
session.commit()

#
category1 = Category(name="hockey")

session.add(category1)
session.commit()


catItem1 = CatItem(title="Hockey Stick", description='''A long-handled stick
                   with one curved end that is used in hockey.''',
                   category=category1, user=user1)

session.add(catItem1)
session.commit()


catItem1 = CatItem(title="Corner flag", description='''Each of the flags that
                   denotes the corner of the field of play.''',
                   category=category1, user=user1)

session.add(catItem1)
session.commit()

catItem1 = CatItem(title="Bibs", description="bib for protecting players ",
                   category=category1, user=user1)

session.add(catItem1)
session.commit()

catItem1 = CatItem(title="Hockey Kit bag", description='''A duffel bag, duffle
                   bag, or kit bag is a large cylindrical bag made of natural
                   or synthetic fabric, historically with a top closure using
                   a drawstring. Generally a duffel bag is used by
                   non-commissioned personnel in the military, and for
                   travel, sports and recreation by civilians. When used by
                   sailors or marines a duffel is known as a \"seabag\".
                   A duffel's open structure and lack of rigidity makes it
                   adaptable to carrying sports gear and similar bulky
                   objects''',
                   category=category1, user=user1)

session.add(catItem1)
session.commit()
