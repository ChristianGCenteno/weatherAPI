'''
It is the module that manage the SQLite DataBase
'''
import weatherApi.SQLiteManagment.SqlSyntax as sqls
import sqlite3
import os

#Conect SQL and create cursor
def sql_conect(database='myweatherDB.db'):
    
    try:
        dbPath = os.path.join('..',database)
        
        conection = sqlite3.connect(dbPath)
        cursor = conection.cursor()
        
        return conection,cursor
    
    except Exception as e:
        print('ERROR DB CONNECTION: ', e)
    

#Disconect SQL
def sql_disconect(conection):
    
    conection.close()

#Show results in comand line(debuging)
def sql_show(result,showPrety=1):
    
    if showPrety == 1:
        for line in result:
            print(line)
    else:
        print(result)

#execute SQL and return result 
def sql_execute(query, display=0, isSelect=False):
    try:
        #print(query)
        conection, cursor = sql_conect()
        cursor.execute(query)
        
        #GET TYPO QUERY
        query_type = query.strip().split()[0].upper()

        if query_type == "SELECT":
            result = cursor.fetchall()
            if display == 1:
                sql_show(result)
            return result

        elif query_type == "INSERT":
            conection.commit()
            return cursor.lastrowid

        else:
            # CREATE, UPDATE, DELETE
            conection.commit()
            return True

    except Exception as e:
        print('ERROR IN DB CALL:', e)
        return None

    finally:
        sql_disconect(conection)

#Adapter to Create Tables
def sqlCreate(table,columns,fkeys):
    
    query = sqls.sqlCreate_table(table,columns,fkeys)
    sql_execute(query,1)
    
#Adapter to INSERT Tables
def sqlInsert(table,columns,values):
    
    query = sqls.sqlInsert_values(table,columns,values)
    return sql_execute(query,1)
    
#Adapter to Delete Rows    
def sqlDelete(table,clasules=[],orderBy=[],limit=0):
    
    query = sqls.sqlDelte_rows(table,clasules,orderBy,limit)
    sql_execute(query,1) 
    
#Adapter to Select Table
def sqlSelect(table,columns,clasules=[],orderBy=[],limit=0,show=0):
    
    query = sqls.sqlSelect_columns(table,columns,clasules,orderBy,limit)
    results = sql_execute(query,show,isSelect=True)
    
    return results


'''
EXAMPLES

sqlSelect("users",["name","rol"],[["name","LIKE","'%.%'"]],[["name","DESC"]],3)
sqlInsert("users", ["name","rol"],[["'t.test1'","'Guest'"],["'t.test2'","'Guest'"],["'t.test3'","'Guest'"]])
print("---")
sqlSelect("users",["name","rol"],[["name","LIKE","'%.%'"]],[["name","DESC"]])
sqlDelete("users", [["name","LIKE","'t.%'"]])
print("---")
sqlSelect("users",["name","rol"],[["name","LIKE","'%.%'"]],[["name","ASC"]])
print("---")
sqlCreate("tests",[["id","INTEGER","PRIMARY KEY",""],["name","VARCHAR(25)","","NOT NULL"],["age","INTEGER","","NOT NULL"],["email","VARCHAR(25)","","NULL"],["idUser","INTEGER","","NOT NULL"]],[["idUser","users","id"]])
#sqlInsert("tests", ["name","age","idUser"],[["'test1'","25","2"],["'test2'","34","1"]])
sqlSelect("tests", ['*'])
'''
