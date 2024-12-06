import  asyncpg

async def  async_get_db():
    connect=await asyncpg.connect(database="bookblogdb",host="localhost",user="postgres",password="@@sl8998",port="5432")
    return connect
    


    

