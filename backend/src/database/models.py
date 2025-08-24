# Here we use ORM where we can write python classes that represents a SQL table
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# sqlite just means that this db will run locally 
# a file that is automatically created 
# if you wanted to connect to a remote db, u just adjust the options to connect to that
engine = create_engine('sqlite:///database.db', echo=True)
# This is used so that we create not just normal python classes but to an object relational mapping classes
Base = declarative_base()

# We always inherit from base so that we can connect it to the database afterwards
class Challenge(Base):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True)
    difficulty = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    created_by = Column(String, nullable=False)
    title = Column(String, nullable=False)
    options = Column(String, nullable=False)
    correct_answer_id = Column(Integer, nullable=False)
    explanation = Column(String, nullable=False)

class ChallengeQuota(Base):
    __tablename__ = 'challenge_quotas'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, unique=True)
    quota_remaining = Column(Integer, nullable=False, default=50)
    last_reset_date = Column(DateTime, default=datetime.now)

# Code that will make this in SQL code
Base.metadata.create_all(engine)

# This will allow us to have a session that represents our db connection 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This creates a db session to handle db requests
def get_db():
    db = SessionLocal()
    try:
        # We give db connection to our code
        yield db
    finally:
        # We close the connection after its finished so that we can make sure that we dont create duplicate sessions
        # Since every session is kind of a different connection
        db.close()