'''
It is the module that create the SQLite syntaxis
'''


'''
#Lists to tests
columns = [["id","Integer","PRIMARY KEY",""],["nombre","text","","NOT NULL"],["email","text","UNIQUE","NOT NULL"]]
columnsfk = [["campomio","tablasuya","camposuya"]]
columnsSel = ["id","nombre","email","campomio"]
columnsCl  = [["id","=","a"],["id",">=","5"]]
columnsOr  = [["id","DESC"],["nombre","ASC"]]
#columnsCl  = []
#columnsOr  = []
columnsIns = ["nombre","email"]
columnsVl  = [['pepito','pepito@'],["pepita","pepita@"],["fulanita","fulanita@"]]

sqltxt2 = sqlCreate_table("usuarios",columns,columnsfk)
sqltxt3 = sqlSelect_columns("usuarios", columnsSel, columnsCl, columnsOr)
sqltxt4 = sqlInsert_values("usuarios", columnsIns, columnsVl)
sqltxt5 = sqlDelte_rows("usuarios", columnsCl,limit=5)

print(sqltxt2)
print(sqltxt3)
print(sqltxt4)
print(sqltxt5)
'''

# TRADUCTOR TO SQL CREATE
def sqlCreate_table (table,columns,fkeys):
    
    sqlcreate_header = 'CREATE TABLE IF NOT EXISTS '
    sqlcreate_table  = table
    y = len(fkeys)
    
    #Ini query
    sql = 'Id INTEGER PRIMARY KEY,\n'
    
    #Columns lines
    for i,k in enumerate(columns):
        if (i == len(columns) - 1) & (0 == len(fkeys)):
            sql = sql + '    ' + k[0] + " " + k[1] + " " + k[2] + " " + k[3]
        else:
            sql = sql + '    ' + k[0] + " " + k[1] + " " + k[2] + " " + k[3] + ',\n'
    
    #Foreign key lines
    
    ##No Foreign key
    if y == 0:
        sql = sql
    ##The rest of the cases
    else:
        for i,k in enumerate(fkeys):
            if i ==  len(fkeys) - 1:
                sql = sql + '    ' + "FOREIGN KEY(" + fkeys[0][0] + ") REFERENCES " + fkeys[0][1] + "(" + fkeys[0][2] + ")"
            else:
                sql = sql + '    ' + "FOREIGN KEY(" + k[0] + ") REFERENCES " + k[1] + "(" + k[2] + ")" + ","
                sql = sql + '\n'
    
    
    #Create SQL query
    sql = sqlcreate_header + sqlcreate_table + ' (' + '\n' + sql + '\n);'

    return sql

# TRADUCTOR TO SQL INSERT
def sqlInsert_values (table,columns,values):
    
    sqlinsert_header = 'INSERT INTO '
    sqlinsert_table  = table + ' (\n'
    sqlinsert_value  = 'VALUES\n'
    
    #Ini Querys
    sqlColumns = ''
    sqlValues  = ''
    
    #Columns to insert
    for i,k in enumerate(columns):
        if (i == len(columns) - 1):
            sqlColumns = sqlColumns + '    ' + k + '\n'
        else:
            sqlColumns = sqlColumns + '    ' + k + ',\n'
   
    #Values to insert
    for i,k in enumerate(values):
        if (i == len(values) - 1):
            sqlValues = sqlValues + '    ('
            for j,v in enumerate(k):
                if (j == len(k) - 1):
                    sqlValues = sqlValues + "'" + v + "'" + ')'
                else:
                    sqlValues = sqlValues + "'" + v + "'" + ','
        else:
            sqlValues = sqlValues + '    ('
            for j,v in enumerate(k):
                if (j == len(k) -1):
                    sqlValues = sqlValues + "'" + v + "'" + '),\n'
                else:
                    sqlValues = sqlValues + "'" + v + "'" + ','
                    
    sqlValues = sqlValues + '\n' 
    
    #Create SQL query        
    sql = sqlinsert_header + sqlinsert_table + sqlColumns + ')\n' + sqlinsert_value + sqlValues + ';'
     
    return sql


# TRADUCTOR TO SQL DELETE
def sqlDelte_rows (table,clasules=[],orderBy=[],limit=0):
    
    sqlDelete_header = 'DELETE'
    sqlDelete_from   = 'FROM'
    sqlDelete_where  = 'WHERE\n' if len(clasules) != 0 else 'WHERE 1 = 1\n'
    sqlDelete_order  = 'ORDER BY\n' if len(orderBy) != 0 else ''
    sqlDelete_limit  = 'LIMIT ' + str(limit) + '\n' if limit != 0 else ''
    
    #Ini query
    sqlWhere  = ''
    sqlOrder  = ''
        
    #columns to filter
    
    ##No WHERES
    if len(clasules) == 0:
        sqlWhere = sqlWhere
    ##Rest of cases
    else:
        for i,k in enumerate(clasules):
            if i ==  len(clasules) - 1:
                sqlWhere = sqlWhere + '    ' + k[0] + " " + k[1] + " " + k[2]
            else:
                sqlWhere = sqlWhere + '    ' + k[0] + " " + k[1] + " " + k[2] + ',\n'
                
        sqlWhere = sqlWhere + '\n'
            
    #Order By
    
    #No Order
    if len(orderBy) == 0:
        sqlOrder = sqlOrder
    ##Rest of cases
    else:
        for i,k in enumerate(orderBy):
            if i ==  len(orderBy) - 1:
                sqlOrder = sqlOrder + '    ' + k[0] + " " + k[1]
            else:
                sqlOrder = sqlOrder + '    ' + k[0] + " " + k[1] + ',\n'
        sqlOrder = sqlOrder + '\n'
    
    #Create SQL query
    sql = sqlDelete_header + '\n' + sqlDelete_from + '\n    ' + table + '\n' + sqlDelete_where + sqlWhere + sqlDelete_order + sqlOrder + sqlDelete_limit + ';'

    return sql

# TRADUCTOR TO SQL SELECT
def sqlSelect_columns (table,columns,clasules=[],orderBy=[],limit=0):
    
    sqlSelect_header = 'SELECT'
    sqlSelect_from   = 'FROM'
    sqlSelect_where  = 'WHERE\n' if len(clasules) != 0 else 'WHERE 1 = 1\n'
    sqlSelect_order  = 'ORDER BY\n' if len(orderBy) != 0 else ''
    sqlSelect_limit  = 'LIMIT ' + str(limit) + '\n' if limit != 0 else ''
    
    #Ini query
    sqlSelect = ''
    sqlWhere  = ''
    sqlOrder  = ''
    
    #columns to select
    for i,k in enumerate(columns):
        if (i == len(columns) - 1):
            sqlSelect = sqlSelect + '    ' + k
        else:
            sqlSelect = sqlSelect + '    ' + k + ',\n'
            
    sqlSelect = sqlSelect + '\n'
    
    #columns to filter
    
    ##No WHERES
    if len(clasules) == 0:
        sqlWhere = sqlWhere
    ##Rest of cases
    else:
        for i,k in enumerate(clasules):
            if i ==  len(clasules) - 1:
                sqlWhere = sqlWhere + '    ' + k[0] + " " + k[1] + " " + k[2]
            else:
                sqlWhere = sqlWhere + '    ' + k[0] + " " + k[1] + " " + k[2] + ' AND\n'
                
        sqlWhere = sqlWhere + '\n'
            
    #Order By
    
    #No Order
    if len(orderBy) == 0:
        sqlOrder = sqlOrder
    ##Rest of cases
    else:
        for i,k in enumerate(orderBy):
            if i ==  len(orderBy) - 1:
                sqlOrder = sqlOrder + '    ' + k[0] + " " + k[1]
            else:
                sqlOrder = sqlOrder + '    ' + k[0] + " " + k[1] + ',\n'
        sqlOrder = sqlOrder + '\n'
    
    #Create SQL query
    sql = sqlSelect_header + '\n' + sqlSelect + sqlSelect_from + '\n    ' + table + '\n' + sqlSelect_where + sqlWhere + sqlSelect_order + sqlOrder + sqlSelect_limit + ';'
    
    return sql
