from sqlalchemy import Integer, String, Column


class User(db.Model):
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    language = Column(String(50))

    def __init__(self, name=None, last_name=None, age=None, language=None):
        self.name = name
        self.last_name = last_name
        self.age = age
        self.language = language

    def __repr__(self):
        return "<User {}>".format(self.name)


class Message(db.Model):

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    content = Column(String(150))

    def __repr__(self):
        return "<Message {}>".format(self.id)