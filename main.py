from fastapi import FastAPI, UploadFile, Form, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()


app = FastAPI()

@app.post('/items')
async def create_item(image:UploadFile, 
                title:Annotated[str, Form()],
                price:Annotated[int, Form()],
                description:Annotated[str, Form()],
                place:Annotated[str, Form()],
                insertAt:Annotated[int, Form()]):
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
async def get_items():
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
    
    return Response(content=bytes.fromhex(image_bytes))
    

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

