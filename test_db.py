from app import db, model
'''
u = model.User(nickname='Rui Zhang', email='ruizhang@email.com')
db.session.add(u)
db.session.commit()

u = model.User(nickname='silverhawk', email='silverhawk@email.com')
db.session.add(u)
db.session.commit()

users = model.User.query.all()
print users
for u in users:
    print(u.id,u.nickname)

u = model.User.query.get(1)

import datetime
u = model.User.query.get(1)
p = model.Post(body='Rui to run the table', timestamp=datetime.datetime.utcnow(), author=u)
db.session.add(p)
db.session.commit()
posts = u.posts.all()

for p in posts:
    print(p.id,p.author.nickname,p.body)
'''

users = model.User.query.all()
for u in users:
     db.session.delete(u)

posts = model.Post.query.all()
for p in posts:
    db.session.delete(p)

db.session.commit()