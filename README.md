# Мои контакты
email: leeroman680@gmail.com
telegram: @romanok54
Выполнил работу - Ли Роман Геннадьевич


# Поисковик документов

Этот проект представляет собой RESTful API для поиска, создания и удаления документов, разработанный с использованием FastAPI и Whoosh.

# Как работает?

Склонируйте репозиторий, после этого пропишите docker-compose up --build
После перейдите и начните поиск через браузер http://localhost:8000/search/?query= "your query"
По этому пути вы можете прописать или удалить документ по id - localhost:8000/docs
Документация OpenApi http://localhost:8000/openapi.json


# Технологии, которые использовались в репозитории
python = "^3.10"
fastapi = "^0.112.2"
uvicorn = "^0.30.6"
sqlalchemy = "^2.0.32"
aiosqlite = "^0.20.0"
whoosh = "^2.7.4"
pydantic = "^2.8.2"

Более подробное README.md с скриншотами внутри MAIN папки. 
