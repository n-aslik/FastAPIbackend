import psycopg2 # type: ignore

def async_get_db():
    connect=psycopg2.connect(dbname="userauthdb",host="localhost",user="postgres",password="@@sl8998",port="5432")
    return connect
    
    


    

