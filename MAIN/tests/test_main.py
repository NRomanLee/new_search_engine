from fastapi.testclient import TestClient
from search_service.main import app
from search_service.models import Base, engine, Document, SessionLocal
import pytest
from datetime import datetime

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)  # Инициализация базы данных
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_document(db):
    response = client.post(
        "/documents/",
        json={"rubrics": ["test"], "text": "test document", "created_date": "2023-09-01T00:00:00"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "test document"
    assert data["rubrics"] == "test"  # Исправлено: теперь проверяем строку, а не список

    db_doc = db.query(Document).filter(Document.id == data["id"]).first()
    assert db_doc is not None
    assert db_doc.text == "test document"
    assert db_doc.rubrics == "test"

def test_read_documents(db):
    test_doc = Document(rubrics="test", text="test document", created_date=datetime(2023, 9, 1))
    db.add(test_doc)
    db.commit()
    db.refresh(test_doc)

    response = client.get("/search/?query=test")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["text"] == "test document"

def test_delete_document(db):
    test_doc = Document(rubrics="test", text="document to delete", created_date=datetime(2023, 9, 1))
    db.add(test_doc)
    db.commit()
    db.refresh(test_doc)

    response = client.delete(f"/documents/{test_doc.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Document deleted"
    assert data["document"]["text"] == "document to delete"

    db_doc = db.query(Document).filter(Document.id == test_doc.id).first()
    assert db_doc is None