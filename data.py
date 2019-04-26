from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Category, CatItem,User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 =User(name='abdo', email='ar1813@fayoum.edu.eg')
#
category1 = Category(name="BASKETBALL")

session.add(category1)
session.commit()


catItem1 = CatItem(title="Basketballs", description="just balls", category=category1, user=user1)

session.add(catItem1)
session.commit()

catItem2 = CatItem(title="Basketball Net", description="the ball goes in it", category=category1, user=user1)

session.add(catItem2)
session.commit()

catItem3 = CatItem(title="Basketball Ring", description="don`t know but seem useful", category=category1, user=user1)

session.add(catItem3)
session.commit()


#
category2 = Category(name="VOLLEYBALL")

session.add(category2)
session.commit()


catItem1 = CatItem(title="Volleyball", description="another ball", category=category2)

session.add(catItem1)
session.commit()

catItem2 = CatItem(title="Volleyball Fiber Antennas",
                   description="the fiber antennas", category=category2)

session.add(catItem2)
session.commit()

catItem2 = CatItem(title="Volleyball Cotton Nets", 
                   description="the Antennas", category=category2)

session.add(catItem2)
session.commit()

# 
category1 = Category(name="HOCKEY")

session.add(category1)
session.commit()


catItem1 = CatItem(title="Hockey Stick", description="a stick", category=category1, user=user1)

session.add(catItem1)
session.commit()


catItem1 = CatItem(title="Corner flag", description="you will now when you need it", category=category1, user=user1)

session.add(catItem1)
session.commit()

catItem1 = CatItem(title="Bibs", description="it`s name seem strange but ok", category=category1, user=user1)

session.add(catItem1)
session.commit()

catItem1 = CatItem(title="Hockey Kit bag", description="your hand would be free don`t worry", category=category1)

session.add(catItem1)
session.commit()
