from fastapi import FastAPI, UploadFile, Form, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                image BLOB,
                title TEXT NOT NULL,
                price INTEGER NOT NULL,
                description TEXT,
                place TEXT NOT NULL,
                insertAt INTEGER NOT NULL
            );
            """)

app = FastAPI()

#SECRET: access token을 어떻게 인코딩 할지 정하는 것, 언제든지 디코딩도 가능 즉, SECRET이 노출되었을때 언제든지 알 수 있음
SECRET = "super-coding"
manager = LoginManager(SECRET, "/login")

#로그인 매니저가 키를 같이 조회함
@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data['id']}"'''
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * FROM users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

@app.post("/login")
def login(id:Annotated[str, Form()],
         password:Annotated[str, Form()]):
    user = query_user(id)
    if not user:
        raise InvalidCredentialsException # 401을 자동으로 생성
    elif password != user["password"]:
        raise InvalidCredentialsException
    #200으로 리턴을안줘도 status는 200이 된다.
    
    #jWT방식은 토큰안에 정보가 담겨있음
    #즉, 서버가 토큰이 맞는지 안맞는지만 검증하고 토큰이 맞으면 
    #그 사람의 정보가 들어있다! 굳이 db를 조회할 필요 x 
    access_token = manager.create_access_token(data={
        "sub":{
            "id":user["id"],
            "name":user["name"],
            "email":user["email"]
        }
    })
    return {"access_token":access_token}
    

@app.post("/signup")
#항상 회원가입이 되기때문에 회원이 아니면 회원가입 하는 로직 짜기
def signup(id:Annotated[str, Form()],
           password:Annotated[str,Form()],
           name:Annotated[str, Form()],
           email:Annotated[str, Form()]):
    
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES('{id}', '{name}', '{email}', '{password}')
                """)
    con.commit()
    return "200"

@app.post("/items")
async def create_item(image:UploadFile, 
                title:Annotated[str, Form()],
                price:Annotated[int, Form()],
                description:Annotated[str, Form()],
                place:Annotated[str, Form()],
                insertAt:Annotated[int, Form()],
                user=Depends(manager)):
    #image는 크기가 너무 커서 이미지를 읽을때까지 await
    image_bytes = await image.read()
    #hex는 16진법으로 바꾸어줌 
    #items라는 테이블의 title, image.......place라는 컬럼에 VALUES에 정의된 것들을 넣어준다는 의미
    #'':문자열
    cur.execute(f"""
                INSERT INTO 
                items(title,image,price,description,place,insertAt)
                VALUES ('{title}', '{image_bytes.hex()}', {price}, '{description}', '{place}',{insertAt})
                """)
    con.commit()
    return '200'

@app.get("/items")
async def get_items(user=Depends(manager)): # user가 인증된 상태에서만 가능
    # 컬럼명도 같이 가져옴 
    con.row_factory = sqlite3.Row
    # db의 커서 갱신?? 느낌 
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * FROM items
                       """).fetchall()
    # rows = [[id: 1], [title:"식칼"]......]
    # 이런식으로 가져오기 위해 오브젝트 객체로 만들기 위해dictionary 이용 
    # dict(row) for row in rows 를 하면 아래와 같은 dictionary로 바꿔줌 
    # {id:1, title:"식칼".......}
    # jsonable_encoder은 json객체로 만들어줌 
    return JSONResponse(jsonable_encoder
        (dict(row) for row in rows)
        ) 
    
    
@app.get("/images/{item_id}")
def get_image(item_id):
    cur = con.cursor()
    #16진법 
    image_bytes = cur.execute(f"""
                              SELECT image FROM items 
                              WHERE id={item_id}
                              """).fetchone()[0]
    
    return Response(content=bytes.fromhex(image_bytes), media_type="image/*")
    


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

