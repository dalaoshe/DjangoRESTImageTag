# React-Multi-Cropper

A `Django` REST Web Server Based On `djangorestframework` [Home-Django REST framework](http://www.django-rest-framework.org/)  

## Feature
- Support Token Authen By JWTToken
- REST API
- `sqlite3` Database (can change to other)


## Require
- `python2.7`
- `Django` >= 1.11.0  
- `djangorestframework` >= 5.0


## Getting Start

### Install
First, Install `python2.7` and `pip`, then git clone our project
```
git clone https://git.chaomy.com/dalaoshe/Image-Django-Server.git
```
Second, Install all the Requires by `pip`
```
:~$ cd Image-Django-Server
:~$ ./init.sh # install all the requires
```
Third, start the server and init the `db.sqlite3` test data
```
:~$ ./run.sh # start server
:~$ curl http://localhost:48080/user/init/ # create test data, include a admin user and a test user, two projects and three images
``` 
### Test REST API
Then, you can use `httpie` to test the REST API, for `example`:  
1.fetch the jwt login token of admin user 
```
:~$ http http://localhost:48080/user/obtainjwttoken/ "username=admin" "password=dalaoshe" 
```
then, you will get:
```
HTTP/1.0 200 OK
Allow: POST, OPTIONS
Content-Length: 185
Content-Type: application/json
Date: Thu, 30 Nov 2017 08:16:54 GMT
Server: WSGIServer/0.1 Python/2.7.12
Vary: Accept
X-Frame-Options: SAMEORIGIN

{
    "role": "admin", 
    "status": "ok", 
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIiwidXNlcl9pZCI6Mn0.1pTTHYtOmycYNtLOEHZJEwhgekdw8gGAgJYt1EF5pn0"
}

```
2.fetch all the project info by admin token(fetch token first)
```
http http://localhost:48080/user/projects/ "Authorization:JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIiwidXNlcl9pZCI6Mn0.1pTTHYtOmycYNtLOEHZJEwhgekdw8gGAgJYt1EF5pn0"
```
then, you will get:
```
HTTP/1.0 200 OK
Allow: POST, OPTIONS, GET
Content-Length: 1661
Content-Type: application/json
Date: Thu, 30 Nov 2017 08:21:37 GMT
Server: WSGIServer/0.1 Python/2.7.12
Vary: Accept
X-Frame-Options: SAMEORIGIN

[
    {
        "creater": "admin", 
        "images": [
            {
                "height": 256, 
                "image_id": "2017-11-30T08:12:40.035503Z", 
                "image_src": "http://img14.360buyimg.com/n5/s500x640_jfs/t10270/263/1662108454/94989/e9c4a3fb/59e44eabNc1cbd5ef.jpg", 
                "projects": [
                    1, 
                    2
                ], 
                "width": 128
            }, 
            {
                "height": 256, 
                "image_id": "2017-11-30T08:12:40.039232Z", 
                "image_src": "https://img10.360buyimg.com/n5/s500x640_jfs/t8080/336/277921481/355263/bbdf4bc2/59a51616Nde18895a.jpg!cc_50x64.jpg", 
                "projects": [
                    1, 
                    2
                ], 
                "width": 128
            }, 
            {
                "height": 256, 
                "image_id": "2017-11-30T08:12:40.043789Z", 
                "image_src": "https://img10.360buyimg.com/n5/s500x640_jfs/t7687/164/1418188723/543130/fd1af88e/599ce253N071b3037.png!cc_50x64.jpg", 
                "projects": [
                    1, 
                    2
                ], 
                "width": 128
            }
        ], 
        "owner": "dalaoshe", 
        "params": "{\"types\": [\"woman\", \"dog\", \"snack\"]}", 
        "project_id": "2017-11-30T08:12:40.047017Z", 
        "project_type": "cropper", 
        "title": "cropper_project"
    },
    ...
]
```
### Confirgure By Nginx 
1.Install `nginx` by `apt-get` first:   
```
:~$ sudo apt-get install nginx
```
2.modify the `chdir` and `socket` in file `uwsgi.ini`, according to your setting:
```
[uwsgi]
#the local unix socket file than commnuincate to Nginx, change to the port your like
socket = 127.0.0.1:48080
# the base directory (full path), change to your path
chdir = /home/dalaoshe/DjangoREST 

# Django's wsgi file
wsgi-file = DjangoREST/wsgi.py
# maximum number of worker processes
processes = 4
#thread numbers startched in each worker process
threads = 2
 
#monitor uwsgi status
stats = 127.0.0.1:9191
# clear environment on exit
vacuum          = true
```
3.add follow nginx setting to you `nginx.conf`:
```
server {
        listen       58080;
        server_name  localhost;
        
        location / {            
            uwsgi_pass  127.0.0.1:48080;              #必须和uwsgi中的设置一致
            include uwsgi_params;
			index  index.html index.htm;
            client_max_body_size 35m;
        }
		location /static {
			alias /path/to/your/project/DjangoREST/collected_static;
		}
    }
```
4.restart `nginx` and start `uwsgi`:
```
~:$ sudo service nginx restart
~:$ ./run_as_server.sh # start uwsgi by `uwsgi.ini`
```
5.then, you can check the REST API and login `Django admin` in browser



