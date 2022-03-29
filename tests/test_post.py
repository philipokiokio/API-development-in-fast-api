import json
from app import schemas
from typing import List
import pytest

def test_get_all_post(authorized_client,test_post):
    res = authorized_client.get('/posts/')
    print(res.json())
    def validate(post):
        return schemas.PostOut(**post)

    post_map= map(validate,res.json())
    post_list  = list(post_map)
    
    # assert(post_list[0].Post.id == test_post[0].id)
    assert(len(res.json())== len(test_post))
    assert(res.status_code == 200)



def test_unauthorized_user_get_all_posts(client, test_post):
    res = client.get('/posts/')
    # print(res.json())
    assert(res.status_code == 401)



def test_unauthorized_user_get_a_posts(client, test_post):
    res = client.get(f'/posts/{test_post[0].id}/')
    # print(res.json())
    assert(res.status_code == 401)  


def test_get_one_post_not_exist(authorized_client, test_post):

    res = authorized_client.get(f'/posts/121')
    assert(res.json().get('detail')== 'Post with Id: 121 was not found')
    assert(res.status_code == 404)



def test_get_one_post(authorized_client, test_post):
    res = authorized_client.get(f'/posts/{test_post[0].id}')
    post = schemas.PostOut(**res.json())

    print(post)
    assert(res.status_code == 200)
    assert(post.Post.id == test_post[0].id)
    assert(post.Post.content == test_post[0].content)


@pytest.mark.parametrize('title, content, published',[
        ('awesome new title', 'awesome new content', True),
        ('dodobabs', 'seems we went to the same school', True),
        ('anoti', 'Bella Shumurda', False),
])
def test_create_post(authorized_client,test_user,test_post, title, content,published):

    res = authorized_client.post('/posts/', json={'title':title, "content":content,'published':published})
    created_post = schemas.Post(**res.json())
    assert(res.status_code == 201)
    assert(created_post.title == title)
    assert(created_post.content == content)
    assert(created_post.published == published)
    assert(created_post.owner_id == test_user['id'])


def test_unauthorized_user_create_post(client, test_post):
    res = client.post('/posts/', json={'title':'Wo do this song',"content":'This song is so sweet come on feel the heat'})
    assert res.status_code == 401

    assert res.json().get('detail') == 'Not authenticated'


def test_unathorized_user_delete_post(client, test_post):
    res = client.delete(f'/posts/{test_post[0].id}')
    assert res.status_code == 401
    # assert res.json().get('detail') == 'Request Unauthorized'


# def test_delete_post_success(authorized_client, test_user, test_post):
#     res = authorized_client.delete(f'/posts/{test_post[1].id}')
#     print(test_post[0].id)
#     assert res.status_code == 204
    
def test_delete_post_non_exist(authorized_client, test_user, test_post):
    res = authorized_client.delete(f'/posts/13')
    assert res.status_code == 404
    assert res.json().get('detail') == 'Post with id 13 does not exists'
    

# def test_delete_other_users_post(authorized_client,test_user, test_post):
#     res = authorized_client.delete(f'/posts/{test_post[3].id}')
#     assert res.status_code == 403
#     assert res.json().get('detail') == 'Request Unauthorized'


def test_update_post(authorized_client, test_user, test_post):
    data ={
        'title':'updated title',
        'content':'updated content',
        'id': test_post[0].id
    }

    res= authorized_client.put(f'/posts/{test_post[0].id}', json= data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title== data['title']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_post):
        data ={
        'title':'updated title',
        'content':'updated content',
        'id': test_post[3].id
    }
        res= authorized_client.put(f'/posts/{test_post[3].id}', json= data)
        assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user,test_post):
    data ={
        'title':'updated title',
        'content':'updated content',
        'id': test_post[0].id
    }
   
   
    res = client.put(
        f'/posts/{test_post[0].id}',json=data
    )
    assert res.status_code == 401
    