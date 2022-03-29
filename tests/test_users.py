from app import schemas
from app.config import settings

import pytest
from jose import jwt








def test_root(client):
    res =client.get('/') 
    print(res.json())
    assert(res.json().get('click here to go to Docs')) == '/docs'
    assert(res.status_code) == 200


def test_create_user(client):
    res = client.post('/user/',json={'email':'philiptest@gmail.com','password':'weraiseby'})
    

    new_test_user =schemas.UserResponse(**res.json())
    assert( new_test_user.email == 'philiptest@gmail.com')
    assert(res.status_code) == 201



def test_login_user(client,test_user):
    res = client.post('/login',data = {'username':test_user['email'], 'password':test_user['password']})
    logged_user = schemas.Token(**res.json())
    payload = jwt.decode(logged_user.access_token, settings.secret_key,algorithms=settings.algorithm)
    id = payload.get('user_id')
    assert(id == test_user['id'])
    assert(logged_user.token_type =='bearer')
    assert(res.status_code == 200)


@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@gmail.com','weraiseby', 403),
    ('philiptest@test.com','wrongpassword',403),
    (None,'weraiseby',422),
    ('philiptest@test.com', None, 422)
])
def test_incorrect_login(test_user,client, email, password, status_code):
    res = client.post('/login',data ={"username":email,'password':password})
    assert(res.status_code==status_code)
    print(res.json())
    # assert(res.json().get('detail')== 'Invalid Credentials' )