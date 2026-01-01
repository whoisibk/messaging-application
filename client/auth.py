import httpx

API_BASE_URL = "http://127.0.0.1:8000"



def Login(userName, password):
    data  = {
        "userName": userName,
        "password": password
    }

    
    response = httpx.post(url=f"{API_BASE_URL}/login", data=data)