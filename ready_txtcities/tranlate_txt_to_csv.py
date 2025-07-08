'''
MODULE TO CREATE CSV RAW CITIES TXT
'''
import os
import re    
from shutil import move
from pandas import read_csv,concat

#--= AUXILIAR =--#

#Sort by column and recreate index
def sort_and_index(dataFrame,column):
    dataFrame = dataFrame.sort_values(by=column)
    dataFrame.index = range(1,len(dataFrame)+1)
    #dataFrame.index.name = 'id'
    
    return dataFrame

#Cast DF column typo
def cast_column(dataFrame,column,typo):
    
    dataFrame[column] = dataFrame[column].astype(typo)
    
    return dataFrame

#Clean the aux DF
def getValue_DF(dfOrigin,column_to_extract):
    
    #Obtain only the values of one column
    dfValues = dfOrigin[[column_to_extract]].drop_duplicates()
    #Transform the column values name
    dfValues = dfValues.rename(columns={column_to_extract:"value"})
    #Sort and create the index
    dfValues = sort_and_index(dfValues, "value")
    
    return dfValues

#Transform values to code
def value_to_key(dFValues,dFMain,valCol,mainCol):
    
    #Transform the values of the DF Values to a dict
    valueDict = dFValues[valCol].to_dict()
    #Operator that obtain the key of each value
    k_valueDict = {v: k for k, v in valueDict.items()}
    #Trasnform DF Main to the keys of the DF Values
    dFMain[mainCol] = dFMain[mainCol].map(k_valueDict) 
    
    
#Return sql Type
def switch_sql_type(typePython):
    return {
        'int': "INTEGER",
        'str': "VARCHAR(255)",
        'float': "NUMERIC"
    }.get(typePython, "VARCHAR(255)")

    
#Transform python type in sql type
def type_to_sql(typeText):
    
    typeValue = re.search(r"'(.*?)'", typeText)
    #print(typeValue.group(1))
    
    return switch_sql_type(typeValue.group(1))
        

#--= =--#

#MAIN PROCEDURE TO LOAD IN CSV FILE CITIES.TXT
#NEW FEATURE[09/05/2025]: INLCUDE A NEW VARIABLE THAT DETERMINE IF IT WILL USE THE PREVIOUS FILTERS (ONLY TO SAVE A CSV WITH ALL THE 
#LOCATIONS, GOAL: HAVE A COMPLETE ALTITUDE MAP (NOT FOR THE WHEATER API)) 
def citytxt_to_csv(cityText='Nl.txt',population_filter=True):
    
    #Determine the columns name
    columns = ["geonameid","name","asciiname","alternatenames","latitude","longitude","feature class","feature code"
               ,"country code","cc2","admin1 code","admin2 code","admin3 code","admin4 code","population","elevation"
               ,"dem","timezone","modification date"]
    
    #Determine path of files
    path = os.path.join(os.getcwd(),"..")
    txtPath = os.path.join(path,cityText)
    dirPath = os.path.join(path,"ProcessedCities")
    path = os.path.join(path,"csv")
    
    try:
        
        #Create a Data Frame
        df = read_csv(txtPath, sep="\t", header=None)
        df.columns = columns
        #print(df)
        
    except (FileNotFoundError):
        
        print("The country.txt not exists")
        exit(2)
    
    #Change columns name and clean uninecesary columns
    df = df.rename(columns={"feature code":"typeLandCode","country code":"countryCode"})
    dClean = df[["name","latitude","longitude","typeLandCode","countryCode","population","dem"]]
    
    #Now, only I kept location with two filters:
    #-Only the population live areas
    #-Areas with a population >= 10,000
    #[09/05/2025]
    if population_filter:
        dClean = dClean[(dClean["typeLandCode"].isin(["PPL","PPLA","PPLA2","PPLC","PPLG"]))
                    &
                (dClean["population"] >= 10000)
                ]
    else:
        dClean = dClean[dClean["population"] > 0]
        dClean['name'] = dClean['name'].str.replace('Gemeente ','')
        ##Get the index with the max population by name
        idx_max = dClean.groupby('name')['population'].idxmax()
        ##Filter    
        dClean = dClean.loc[idx_max].reset_index(drop=True)
        
    
    #sorted & re-index 
    dClean = sort_and_index(dClean,'name')
    
    #Cast the corrects typo
    #dClean = cast_column(dClean, "latitude", float)
    #dClean = cast_column(dClean, "longitude", float)
    print(dClean['latitude'])
    
    #Ones clean the file, create all the csv for load into the DB ---------
    dMain = dClean
    dLandTp = getValue_DF(dMain, "typeLandCode")
    dCounTp = getValue_DF(dMain, "countryCode")
    
    #Transform values of DMain to keys of the others DF
    value_to_key(dLandTp, dMain, "value", "typeLandCode")
    value_to_key(dCounTp, dMain, "value", "countryCode")
    
    #Create a load DataBase columns check
    dMain['isLoad']   = 0 
    dLandTp['isLoad'] = 0
    dCounTp['isLoad'] = 0
    
    #----------------------------------------------------------------------
    
    #[09/05/2025]: Create alternative csv to the complete file
    if population_filter:
        #CSV Files
        citiesCsv    ='cities.csv'
        landTypeCsv  ='cat_typeLand.csv'
        countriesCsv ='cat_country.csv'
    else:
        #CSV Files
        citiesCsv    ='cities_complete.csv'
        landTypeCsv  ='cat_typeLand_complete.csv'
        countriesCsv ='cat_country_complete.csv'
    
    #CSV path
    citiesPath    = os.path.join(path,citiesCsv)
    landPath      = os.path.join(path,landTypeCsv)
    countriesPath = os.path.join(path,countriesCsv)
    
    #If exists, update the new files
    if os.path.exists(citiesPath):
        
        #Read existing csv
        dfCities    = read_csv(citiesPath,sep=';',decimal='.',index_col='id')
        dfLand      = read_csv(landPath,sep=';',decimal='.',index_col='id')
        dfCountries = read_csv(countriesPath,sep=';',decimal='.',index_col='id')
        
        #Create DF with only the new rows
        dfCities_news    = dMain[~dMain.index.isin(dfCities.index)]
        dfLand_news      = dLandTp[~dLandTp.index.isin(dfLand.index)]
        dfCountries_news = dCounTp[~dCounTp.index.isin(dfCountries.index)]
        
        ##Reindex the news rows
        dfCities_news.index    = range(dfCities.index.max()    + 1, dfCities.index.max()    + (len(dfCities_news)    + 1))
        dfLand_news.index      = range(dfLand.index.max()      + 1, dfLand.index.max()      + (len(dfLand_news)      + 1))
        dfCountries_news.index = range(dfCountries.index.max() + 1, dfCountries.index.max() + (len(dfCountries_news) + 1))
        
        ##Combine    
        dfCities_final    = concat([dfCities   , dfCities_news])
        dfLand_final      = concat([dfLand     , dfLand_news])
        dfCountries_final = concat([dfCountries, dfCountries_news])
        
        #Create de csv files Updating
        dfCities_final.to_csv(citiesPath,sep=";",decimal=".",index_label='id')
        dfLand_final.to_csv(landPath,sep=";",index_label='id')
        dfCountries_final.to_csv(countriesPath,sep=";",index_label='id')
        
        print("Csv files updated")
        
    else:
        
        #Create de csv files
        dMain.to_csv(citiesPath,sep=";",decimal=".",index_label='id')
        dLandTp.to_csv(landPath,sep=";",index_label='id')
        dCounTp.to_csv(countriesPath,sep=";",index_label='id')
        
        #Crear los csv
        print("Csv files created")
        
    #Move the txt processed to clean
    move(txtPath,dirPath)

#MAIN FUCTION THAT EXTRACT COLUMNS AND VALUES LIST BY A CSV FILE
def extract_csv(csvFile):
    
    #Path
    path = os.path.join(os.getcwd(),"..")
    path = os.path.join(path,'csv')
        
    #Read the csv file
    csvPath = os.path.join(path,csvFile)
    dfCsv   = read_csv(csvPath,sep=';',decimal='.',index_col='id')
    
    #Only we choose the rows with 'isLoad' column = 0
    dfCsv   = dfCsv[dfCsv["isLoad"] == 0]
    
    #Control, if there isn't any file, stop the load
    if dfCsv.size == 0:
        print("There isn't any row to load, stoping the process")
        exit(3)
    
    #Incluse de index values in the values rows
    dfCsv_withIndex = dfCsv.reset_index()
    
    #In the load process, is necesary to exlude the check load column
    dfCsv_withIndex = dfCsv_withIndex.drop(columns=['isLoad'])
    dfCsv           = dfCsv.drop(columns=['isLoad'])
    
    #List values and columns names
    listValues  = dfCsv_withIndex.values.tolist()
    listColumns = (['id'] + dfCsv.columns.to_list())
        
    return listValues,listColumns  

#MAIN FUCTION THAT UPDATE THE CSV ROWS TO CONTROL WHO ROWS ARE LOAD
def update_load(csvFile):
    
    #Path
    path = os.path.join('..','csv')
        
    #Read the csv file
    csvPath = os.path.join(path,csvFile)
    dfCsv   = read_csv(csvPath,sep=';',decimal='.',index_col='id')
    
    #Update the load columns to indicate that a row is already processed
    dfCsv.loc[dfCsv['isLoad']==0,'isLoad'] = 1
    
    dfCsv.to_csv(csvPath,sep=";",decimal=".",index_label='id')
    