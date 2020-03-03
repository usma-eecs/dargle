import sqlalchemy
import csv

from sqlalchemy import create_engine
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func

Base = declarative_base()

class Domain(Base):
	__tablename__ = 'domains'

	# id = Column(Integer, primary_key=True)
	domain = Column(String,primary_key=True)
	current_status = relationship("Timestamp")
	hits = Column(Integer)
	references = Column(String)
	origins = Column(String)

	def __repr__(self):
		return "<Domain(domain={},hits={})>".format(self.domain,self.hits)

class Timestamp(Base):
	__tablename__ = 'timestamps'

	timestamp = Column(String,primary_key=True)
	domain = Column(String,ForeignKey('domains.domain'))
	status = Column(String)

	def __repr__(self):
		return "<Timestamp(domain={},timestamp={},status={}>".format(self.domain,self.timestamp,self.status)

def csvTransfer(file,sess):
	infile = open(file,'r')
	reader = csv.reader(infile,delimiter=',')

	next(reader,None)

	for row in reader:
		domain = row[0]
		status = row[1]
		hits = row[2]
		timestamp = row[3]

		onion = Domain(domain=domain,hits=hits)
		tstamp = Timestamp(domain=domain,timestamp=timestamp,status=status)
		merge1 = sess.merge(onion)
		merge2 = sess.merge(tstamp)

		sess.commit()

	print(sess.query(Domain).all())
	print("\n")
	print(sess.query(Timestamp).all())

def dbUpdate(file):
	engine = create_engine('sqlite:///dargle.sqlite', convert_unicode=True)
	session = sessionmaker()
	session.configure(bind=engine)
	Base.metadata.create_all(engine)

	s = session()
	csvTransfer(file,s)

# dbUpdate(file)
