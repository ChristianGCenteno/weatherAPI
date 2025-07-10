'''
Module Aux to exe the city.txt load
'''
import weatherApi.ready_txtcities.tranlate_txt_to_csv as tt
import weatherApi.SQLiteManagment.SqLiteAdapter       as sqlAdapter

#Read a city text and load into csv files
def read_city():
    
    txt = input("Write de city.txt (case sensitive): ")
    
    if('.txt' in txt):
        
        tt.citytxt_to_csv(txt)
        
    else:
        
        txt = txt +  '.txt'
        tt.citytxt_to_csv(txt)
        
    return txt
    
#Return lists of values and columns
def csv_to_list(csvFile):
    
    values,columns = tt.extract_csv(csvFile)
    
    return values,columns

#load csv into SQLite
def load_csv_db(csvFiles):
    
    for csvFile in csvFiles:
        
        values,columns = csv_to_list(csvFile)
        tableName      = csvFile.split('.')[0] 
        columnsType    = []

        #Get column type (only first row is necessary)
        for x in values[0]:
            
            typo = str(type(x))
            typo = tt.type_to_sql(typo)
            columnsType.append(typo)
        
        #Create lists for each table
        declareCol = []
        declareFk  = []
        
        #Get columns to create table
        for i,v in enumerate(columns):
            
            declare   = []
            eleColumn = v
            eleType   = columnsType[i]
            decFk   = []
            
            if eleColumn == 'id':
                elePk = "PRIMARY KEY"
            else:
                elePk = ""
            
            if elePk != "":
                eleNulleable = ""
            elif 'Code' in eleColumn:
                eleNulleable = "NOT NULL"
            else:
                eleNulleable = "NULL"
                
            if 'Code' in eleColumn:
                
                tableFk = 'cat_' + eleColumn.replace('Code','')
                decFk = [str(eleColumn),str(tableFk),'id']
                
                declareFk = [sublist for sublist in declareFk if sublist]
                declareFk.append(decFk)
                
            declare = [str(eleColumn),str(eleType),str(elePk),str(eleNulleable)]
            
            declareCol.append(declare)
           
                    
        #CREATE TABLE
        sqlAdapter.sqlCreate(tableName,declareCol,declareFk)
        
        #Insert Values list
        rowsToInsert = []
        
        for value in values:
            
            v = list(map(str,value))
            v = list(map(lambda s: s.replace("'","").replace(" ","_"),v))
            
            rowsToInsert.append(v)
            
        #INSERT ROWS
        sqlAdapter.sqlInsert(tableName, columns,rowsToInsert)
        
        #SELECT TEST
        sqlAdapter.sqlSelect(tableName, ["*"])
        
        #UPDATE CSV FILES TO INDICATE THAT THE ROWS ARE ALREADY LOAD
        tt.update_load(csvFile)
            

#READ AND LOAD A CITY TXT
def read_load_city():
    read_city()
    csvFiles = ['cities.csv','cat_typeLand.csv','cat_country.csv']
    load_csv_db(csvFiles)

#NEW FEATURE[09/05/2025]: INLCUDE A NEW VARIABLE THAT DETERMINE IF IT WILL USE THE PREVIOUS FILTERS (ONLY TO SAVE A CSV WITH ALL THE 
#LOCATIONS, GOAL: HAVE A COMPLETE ALTITUDE MAP (NOT FOR THE WHEATER API)) 
def read_city_complete():
    
    txt = input("Write de city.txt (case sensitive): ")
    
    if('.txt' in txt):
        
        tt.citytxt_to_csv(txt,False)
        
    else:
        
        txt = txt +  '.txt'
        tt.citytxt_to_csv(txt,False)
        
    return txt
