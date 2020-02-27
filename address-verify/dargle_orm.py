import sqlalchemy
import csv

from sqlalchemy import create_engine
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func

Base = declarative_base()

class Domain(Base):
	__tablename__ = 'domains'

	# id = Column(Integer, primary_key=True)
	domain = Column(String, primary_key=True)
	status = Column(String)
	hits = Column(Integer)
	references = Column(String)
	origins = Column(String)
	timestamp = Column(String)

	def __repr__(self):
		return "<Domain(domain={},status={},hits={})>".format(self.domain,self.status,self.hits)

def csvTransfer(file,sess):
	infile = open(file,'r')
	reader = csv.reader(infile,delimiter=',')

	next(reader,None)

	for row in reader:
		domain = row[0]
		status = row[1]
		hits = row[2]

		onion = Domain(domain=domain,status=status,hits=hits)
		merge = sess.merge(onion)

		sess.commit()

	print(sess.query(Domain).all())

def dbUpdate(file):
	engine = create_engine('sqlite:///dargle.sqlite')
	session = sessionmaker()
	session.configure(bind=engine)
	Base.metadata.create_all(engine)

	s = session()
	csvTransfer(file,s)

# dbUpdate(file)
