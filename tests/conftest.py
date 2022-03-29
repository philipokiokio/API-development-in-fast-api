
from venv import create
from fastapi.testclient import TestClient
from app.database import get_db
from app.main import app
from app import schemas, database, models
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest

from app.oauth2 import create_access_token



# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"
print(SQLALCHEMY_DATABASE_URL)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()





# Dependency
def overide_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()










@pytest.fixture() 
def session():
    database.Base.metadata.drop_all(bind=engine)
    database.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def overide_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = overide_get_db

    yield TestClient(app)

 
@pytest.fixture()
def test_user(client):
    user_data = {'email':'philiptest@test.com',
    'password': 'weraiseby'}
    res = client.post('/user/', json=user_data)
    assert(res.status_code == 201)
    new_user_data = res.json()
    new_user_data['password'] = user_data['password']
    print(new_user_data)
    return new_user_data


@pytest.fixture()
def test_user2(client):
    user_data = {'email':'philiptest1@test.com',
    'password': 'weraiseby11'}
    res = client.post('/user/', json=user_data)
    assert(res.status_code == 201)
    new_user_data = res.json()
    new_user_data['password'] = user_data['password']
    print(new_user_data)
    return new_user_data



@pytest.fixture()
def token(test_user):
    return create_access_token({'user_id':test_user['id']}) 

@pytest.fixture()
def authorized_client(client,token):
    client.headers={
        **client.headers,
        'Authorization':f'Bearer {token}'
    } 
    return client 


@pytest.fixture()
def test_post(test_user, session, test_user2):
    posts_data = [
         {
             "title":"first title",
             "content":'first content',
             'owner_id': test_user['id']
         },
         {
             "title":"second title",
             "content":'second content',
             'owner_id': test_user['id']
         },
         {
             "title":"third  title",
             "content":'third content',
             'owner_id': test_user['id']
         },
         {
             "title":"4th  title",
             "content":'4th content',
             'owner_id': test_user2['id']
         }                             
    ]

    def create_post_model(post):
        return models.Post(**post)


    post_map =map(create_post_model, posts_data)
    posts = list(post_map)
    print(posts)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts