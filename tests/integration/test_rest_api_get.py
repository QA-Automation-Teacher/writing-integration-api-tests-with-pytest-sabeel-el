import requests
import json
import pytest


@pytest.fixture
def base_url():
    return "http://localhost:5000"

@pytest.fixture
def data():
    with open('src/data.json', 'r', encoding='utf-8') as file:
        return json.load(file)



def test_get_posts(base_url):
    response = requests.get(f"{base_url}/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_post_by_id(base_url):
    post_id = 56
    response = requests.get(f"{base_url}/posts/{post_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert int(response.json().get('id')) == post_id

def test_get_nonexistent_post(base_url):
    post_id = 9999
    response = requests.get(f"{base_url}/posts/{post_id}")
    assert response.status_code == 404


def test_get_status(base_url):
    endpoint=f"{base_url}/posts"
    response = requests.get(endpoint)
    assert response.status_code == 200

def test_get_response_type(base_url):
    response = requests.get(f"{base_url}/posts")
    assert isinstance(response.json(), list)
           
def test_get_response_length(base_url):
    response = requests.get(f"{base_url}/posts")
    assert len(response.json()) > 0, "No posts returned"

def test_get_post_type(base_url):
    post_id = 1
    response = requests.get(f"{base_url}/posts/{post_id}")
    post = response.json()
    assert isinstance(post, dict)
           

def test_get_post_count(base_url):
    post_id = 1
    response = requests.get(f"{base_url}/posts")
    posts = response.json()
    assert len(posts)>=1
        
#--------------------------------POST---------------------------------
     
def test_post_status(base_url,data):
    payload=data[1]
    response = requests.post(f"{base_url}/posts", json=payload)
    assert response.status_code == 201
        
    
def test_post_id_present( base_url,data):
    payload = data[2]
    response = requests.post(f"{base_url}/posts", json=payload)
    created_post = response.json()
    assert "id" in created_post
        

def test_post_title( base_url,data):
    payload = data[0]
    response = requests.post(f"{base_url}/posts", json=payload)
    created_post = response.json()
    assert created_post["title"] == payload["title"]
        
def test_post_header( base_url,data):
    payload = data[0]
    response = requests.post(f"{base_url}/posts", json=payload)
    assert response.headers["Content-Type"] == "application/json"  

#---------------------------------PUT---------------------------------------------
    
def test_put_update_post(base_url,data):
    post_id = 4
    payload = data[1]
    response = requests.put(f"{base_url}/posts/{post_id}", json=payload)
    updated_post = response.json()
    assert updated_post["title"] == payload["title"]

def test_put_key_post(base_url,data):
    post_id = 4
    payload = data[1]
    response = requests.put(f"{base_url}/posts/{post_id}", json=payload)
    updated_post = response.json()
    for key, value in payload.items():
        assert updated_post[key] == value
        
def test_put_post_id( base_url,data):
    post_id = 45
    payload = data[1]
    response = requests.put(f"{base_url}/posts/{post_id}", json=payload)
    post = response.json()
    assert post["id"] == post_id

def test_put_server_header(base_url,data):
    post_id = 1
    payload = data[1]
    response = requests.put(f"{base_url}/posts/{post_id}", json=payload)
    assert "Server" in response.headers 

def test_put_cookies( base_url,data):
    post_id = 1
    payload = data[1]
    response = requests.put(f"{base_url}/posts/{post_id}", json=payload)
    assert "session_id" in response.cookies  
        
def test_put_response_keys( base_url,data):
    post_id = 59
    payload = data[1]
    response = requests.put(f"{base_url}/posts/{post_id}", json=payload)
    res=response.json()
    assert set(res.keys()) == {"id", "title", "body", "userId"}


#---------------------------------DELETE----------------------------------------------
    
def test_delete_post(base_url):
    post_id = 3
    response = requests.delete(f"{base_url}/posts/{post_id}")
    assert (response.json()) == {'message': 'Post deleted', 'status': 'success'}
       

def test_delete_response_time(base_url):
    post_id=2
    response = requests.delete(f"{base_url}/posts/{post_id}")
    assert response.elapsed.total_seconds() < 4  
        

def test_delete_content_type(base_url):
    post_id=10
    response = requests.delete(f"{base_url}/posts/{post_id}")
    assert response.headers["Content-Type"] == "application/json"  

def test_delete_post_status(base_url):
    post_id = 78
    response=requests.delete(f"{base_url}/posts/{post_id}")
    assert response.status_code == 200

def test_delete_post_not_found(base_url):
    post_id = 1
    requests.delete(f"{base_url}/posts/{post_id}")
    response= requests.get(f"{base_url}/posts/{post_id}")
    assert response.status_code == 404




        

        


        

            
