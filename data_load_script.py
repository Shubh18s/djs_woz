import models
from database import SessionLocal, engine
import json

# Creating local db session
db=SessionLocal()

# Creating all the tables in model
models.Base.metadata.create_all(bind=engine)

with open('path_to_file/person.json') as f:
  data = json.load(f)