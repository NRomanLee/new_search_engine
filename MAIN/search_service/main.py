from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from models import SessionLocal, Document, engine
from pydantic import BaseModel
from typing import List
from datetime import datetime
import whoosh.index as index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os
from import_data import import_data

app = FastAPI()

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

schema = Schema(id=ID(stored=True), text=TEXT)
ix = index.create_in("indexdir", schema)

def get_db():
    db = SessionLocal()  
    try:
        yield db
    finally:
        db.close()

class DocumentCreate(BaseModel):
    rubrics: List[str]
    text: str
    created_date: datetime

@app.post("/documents/")
async def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    db_doc = Document(rubrics=",".join(doc.rubrics), text=doc.text, created_date=doc.created_date)
    db.add(db_doc)
    db.commit()  
    db.refresh(db_doc)
    writer = ix.writer()
    writer.add_document(id=str(db_doc.id), text=db_doc.text)
    writer.commit()  
    return db_doc

@app.delete("/documents/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    db_doc = db.query(Document).filter(Document.id == document_id).first()
    if db_doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(db_doc)
    db.commit()  
    writer = ix.writer()  
    writer.delete_by_term("id", str(document_id))
    writer.commit()  
    return {"message": "Document deleted", "document": {
        "id": db_doc.id,
        "rubrics": db_doc.rubrics,
        "text": db_doc.text,
        "created_date": db_doc.created_date.isoformat()
    }}  

@app.get("/search/")
async def search_documents(query: str, db: Session = Depends(get_db)):
    searcher = ix.searcher()
    query_parser = QueryParser("text", ix.schema)
    parsed_query = query_parser.parse(query)
    results = searcher.search(parsed_query, limit=20)
    ids = [int(result['id']) for result in results]
    documents = db.query(Document).filter(Document.id.in_(ids)).order_by(Document.created_date.desc()).all()
    
    formatted_documents = []
    for doc in documents:
        formatted_doc = {
            "id": doc.id,
            "rubrics": doc.rubrics,
            "text": doc.text.replace('\n', ' '),  
            "created_date": doc.created_date.isoformat()
        }
        formatted_documents.append(formatted_doc)
    
    return formatted_documents

import_data()
    
    


