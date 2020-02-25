import sqlalchemy
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func

Base = declarative_base()

class Domain(Base):
	__tablename__ = 'domains'

	id = Column(Integer, primary_key=True)
	domain = Column(String)
	status = Column(String)
	hits = Column(Integer)
	references = Column(String)
	origins = Column(String)

	def __repr__(self):
		return "<Domain(domain={},status={},hits={})>".format(self.domain,self.status,self.hits)

def csvTransfer(sess):
	infile = open('output.csv','r')
	reader = csv.reader(infile,delimiter=',')

	next(reader,None)

	for row in reader:
		domain = row[0]
		status = row[1]
		hits = row[2]

		onion = Domain(domain=domain,status=status,hits=hits)

		sess.add(onion)
		sess.commit()

	print(sess.query(Domain).all())

def dbUpdate():
	engine = create_engine('sqlite:///dargle.sqlite')
	session = sessionmaker()
	session.configure(bind=engine)
	Base.metadata.create_all(engine)

	s = session()
	csvTransfer(s)

dbUpdate()
