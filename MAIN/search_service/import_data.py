import csv
from sqlalchemy.orm import Session
from models import Document, engine, SessionLocal
from datetime import datetime
import whoosh.index as index
from whoosh.fields import TEXT, Schema, ID
import os

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

schema = Schema(id=ID(stored=True), text=TEXT)
ix = index.create_in("indexdir", schema)

def import_data():
    db = SessionLocal()
    writer = ix.writer()

    with open("posts.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rubrics = row["rubrics"]
            text = row["text"]
            created_date = datetime.strptime(row["created_date"], "%Y-%m-%d %H:%M:%S")
            db_doc = Document(rubrics=rubrics, text=text, created_date=created_date)
            db.add(db_doc)
            db.commit()  
            db.refresh(db_doc)
            writer.add_document(id=str(db_doc.id), text=db_doc.text)
    writer.commit()  
    db.close()



