from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.types import Date
from database import Base
from sqlalchemy.orm import relationship

class UserQuery(Base):
    __tablename__ = 'userquery'
    id = Column(Integer, primary_key=True)
    user_request = Column(Text, default="Listening...")
    wizard_response = Column(Text, default="No Response")

    '''It will be set to 1 if user says something first'''
    #user_sent = Column(Integer, default=0)

    '''It will be set to 1 if wizard says something first'''
    #wizard_sent = Column(Integer, default=0)

    #user_utterance_time = Column(Integer, default=0)
    #wizard_utterance_time = Column(Integer, default=0)

    def __repr__(self):
       return("'{0}', '{1}'".format(self.user_request, self.wizard_response))


class Argument(Base):
    __tablename__ = 'arguments'
    id = Column(String, primary_key=True)
    title = Column(Text, default="")
    num_pros = Column(Integer, default=0)
    num_cons = Column(Integer, default=0)
    pros = relationship('Pro', backref='argument')
    cons = relationship('Con', backref='argument')
    def __repr__(self):
       return("'{0}', '{1}', '{2}'".format(self.title, self.num_pros, self.num_cons))


class Pro(Base):
    __tablename__ = 'pros'
    id = Column(String, primary_key=True)
    title = Column(Text, default="")
    text = Column(Text, default="")
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    argument_id = Column(String, ForeignKey('arguments.id'))
    def __repr__(self):
       return("'{0}', '{1}', '{2}', '{3}', '{4}'".format(self.title, self.text, self.like_count, self.comment_count, self.argument))


class Con(Base):
    __tablename__ = 'cons'
    id = Column(String, primary_key=True)
    title = Column(Text, default="")
    text = Column(Text, default="")
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    argument_id = Column(String, ForeignKey('arguments.id'))
    def __repr__(self):
       return("'{0}', '{1}', '{2}', '{3}', '{4}'".format(self.title, self.text, self.like_count, self.comment_count, self.argument))
