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
	title = Column(String)

	references = Column(String)
	origins = Column(String)

	def __repr__(self):
		return "<Domain(domain={},title={},hits={})>".format(self.domain,self.title,self.hits)

class Source(Base):
	__tablename__ = 'sources'

	domain = Column(String,primary_key=True)
	unique_onions = Column(Integer)

	def __repr__(self):
		return "<Source(domain={},hits={}>".format(self.domain,self.hits)

class Timestamp(Base):
	__tablename__ = 'timestamps'

	timestamp = Column(String,primary_key=True)
	domain = Column(String,ForeignKey('domains.domain'))
	status = Column(String)

	def __repr__(self):
		return "<Timestamp(domain={},timestamp={},status={}>".format(self.domain,self.timestamp,self.status)

def csvTransfer(onions,domains,sess):
	domain_in = open(domains,'r')
	domain_reader = csv.reader(domain_in,delimiter=',')

	onion_in = open(onions,'r')
	onion_reader = csv.reader(onion_in,delimiter=',')

	next(domain_reader,None)

	for row in onion_reader:
		domain = row[0]
		status = row[1]
		hits = row[2]
		timestamp = row[3]
		title = row[4]

		onion = Domain(domain=domain,title=title,hits=hits)
		tstamp = Timestamp(domain=domain,timestamp=timestamp,status=status)
		merge1 = sess.merge(onion)
		merge2 = sess.merge(tstamp)

		sess.commit()

	for row in domain_reader:
		domain = row[0]
		hits = row[1]

		domain = Source(domain=domain,unique_onions=hits)
		merge1 = sess.merge(domain)

		sess.commit()

	'''
	# For Troubleshooting:
	print(sess.query(Domain).all())
	print("\n")
	print(sess.query(Timestamp).all())
	'''

def dbUpdate(onion,domain):
	engine = create_engine('sqlite:///dargle.sqlite', convert_unicode=True)
	session = sessionmaker()
	session.configure(bind=engine)
	Base.metadata.create_all(engine)

	s = session()
	csvTransfer(onion,domain,s)

# dbUpdate(file)
