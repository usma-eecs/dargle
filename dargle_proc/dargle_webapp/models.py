from datetime import datetime
from dargle_webapp import db

# Creates a object class 'Domains' for table in database
# Domain class has the following attributes:
#   - darkweb domain hash
#   - hidden service status (e.g. 404)
#   - how many times it appears on clear web (hits)
#   - title of page if connection is successful
class Domain(db.Model):
    __tablename__ = 'domains'

    # id = Column(Integer, primary_key=True)
    domain = db.Column(db.String,primary_key=True)
    current_status = db.relationship("Timestamp")
    hits = db.Column(db.Integer)
    references = db.Column(db.String)
    origins = db.Column(db.String)
    title = db.Column(db.String)

    def __repr__(self):
        return "<Domain(domain={},title={},hits={})>".format(self.domain,self.title,self.hits)

# Creates a object class 'Timestamp' for table in database
# Timestamps have following attributes:
#   - time of attempted connection
#   - domain
#   - status
class Timestamp(db.Model):
    __tablename__ = 'timestamps'

    timestamp = db.Column(db.String,primary_key=True)
    domain = db.Column(db.String,db.ForeignKey('domains.domain'))
    status = db.Column(db.String)

    def __repr__(self):
        return "<Timestamp(domain={},timestamp={},status={}>".format(self.domain,self.timestamp,self.status)
