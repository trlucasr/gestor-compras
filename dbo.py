import mysql.connector

def conectadb():
    mydb = mysql.connector.connect(
    host="sql139.main-hosting.eu",
    user="u781205362_gestorcompras",
    password="0xDm$$Df",
    database="u781205362_gestorcompras"
    )
        
    return(mydb)    

def insertdb(sql,values):

    #instancio Mydb
    mydb = conectadb()

    #Crio cursor
    cursorinto = mydb.cursor()

    #Executo Into
    cursorinto.execute(sql, values)

    #Commit de inclusões
    mydb.commit()

    return(cursorinto.rowcount)

def selectdb(sql):

    #instancio Mydb
    mydb = conectadb()

    #Crio cursor
    cursorsel = mydb.cursor()

    #Executo Into
    cursorsel.execute(sql)

    #Tras valores do banco
    values = cursorsel.fetchall()

    return(values)
