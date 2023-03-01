from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models import Base, User, Message, Follower

# connection URL: 'postgresql://postgres:password@host:port/database'
engine = create_engine('postgresql://postgres:postgres@localhost:5432/minitwit')


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)



""" Time line example 
('''
                select messages.*, users.* from messages, users
                where messages.flagged = 0 and messages.author_id = users.user_id and (
                    users.user_id = %s or
                    users.user_id in (select whom_id from followers
                                            where who_id = %s))
                order by messages.pub_date desc limit %s''',
                [user_id, user_id, per_page_limit])
"""
from sqlalchemy.orm import aliased, joinedload

# Create a user
user_one = User(username='test', email="a@a.com", pw_hash="123")
# session.add(user_one)
# session.commit()

users = session.query(User).all()
# print(users)

user_id = 1
per_page_limit = 10

user = session.query(User).filter_by(user_id=user_id).one()
following_ids = [follower.whom_id for follower in user.following]

query = session.query(Message, User).join(User)\
              .filter(Message.flagged == 0)\
              .filter((User.user_id == user_id) | (User.user_id.in_(following_ids)))\
              .order_by(Message.pub_date.desc())\
              .limit(per_page_limit)\
              .options(
                  # Load the author relationship to avoid additional queries
                  joinedload(Message.author)
              )

results = query.all()


