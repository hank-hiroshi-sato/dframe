# DataSet Test
# getFormColumne/
#from tkinter import StringVar
import dataset
import collections
from collections import OrderedDict
from dframe.db import get_db, init_db

from sqlalchemy import sql, values

def getAppName():
    db = init_db()
    sql = 'select appName from systemini limit 1'
    result = db.query(sql)
    for row in result:
        rowDict = dict(row)    
        
    return rowDict['appName']
    
def getFormInfo(kindOfInfo, cpath, sql_app='', lineNumPerPage=100000, offset=0, viewID=0):
    db = get_db()
    sql = '' 
    if len(sql_app) == 0:
        path = str(cpath[0])                #formID
        if kindOfInfo != 'FormPrpty':    
            path += ',' + str(cpath[1])     #acctRoleID
            if kindOfInfo == 'FormData':
                path += ',' + str(cpath[2]) #objectID
                path += ','  + str(lineNumPerPage)
                path += ','  + str(offset)
                path += ','  + str(viewID)

        sql = 'call dframe.get' + kindOfInfo + '(' + path + ')'
    else:
        sql = sql_app
    print('fg45:', sql_app, ':',sql, cpath)
    results=db.query(sql)

    formInfo = []
    i = 0
    for row in results:
        rowDict = dict(row)

        formInfo.insert(i,rowDict)
        i += 1
        
    if kindOfInfo == 'LineNum':
        return len(formInfo)  
    else:  
        return formInfo


# to get Search Results Data Set (view of the terget object)
# kindOfInfo : Columns, Data  --> FormColumns, FormData for the search form
def getSubFormInfo(kindOfInfo, baseTableName, fieldNm, fieldCaption, derivedTerm='', searchWord='',  
                   lineNumPerPage=10000, offset=0 ):

    db = get_db()
    sql = 'call ' + getAppName() + '.getListSearch' + kindOfInfo
    sql += '("' + baseTableName + '","' +fieldNm +'","'  + fieldCaption + '"' 
    if kindOfInfo == 'Data':
        sql += ',"' + derivedTerm +  '","'+ searchWord + '",' +str(lineNumPerPage) + ',' +str(offset)
    sql +=  ')'
    print('ig75: ',sql)
    results=db.query(sql)

    formInfo = []

    i = 0
    for row in results:
        rowDict = dict(row)

        formInfo.insert(i,rowDict)
        i += 1

    #print('79: ',kindOfInfo,formInfo)    
    return formInfo

#to provide the combobox list Data
#slctStyle: "lookup"-combobox sourceName=list data to provied the selection list data, 
#           "view"- formID = to provide the field name of the formID Object
def getSelectList(slctStyle, sourceName, formID):
    #print('fg80:',slctStyle, sourceName, formID)
    dbNm = getAppName()
    db = get_db()
    sql = 'call ' + dbNm + '.getSelectList'
    sql += '("' + dbNm + '","' + slctStyle +'","'  + sourceName + '",' + str(formID) + ')'
    
    #print('fg93:getSelectList ',sql)
    results=db.query(sql)
    sList = []
    sDict = {}
    i = 0
    
    for row in results:
        rowDict = dict(row)
        sList.insert(i,rowDict)
        i += 1
            
        ''' not used ?
        for row in results:
            rowDict = dict(row)
            sList.insert(i,rowDict['caption'])
            sDict[rowDict['caption']] = rowDict['value']
            i += 1
        '''
        
    return sList
'''  not used
def getLookUpValue(fieldNm, sourceName, strainName, capName, dataType, value):
    dbNm = getAppName()
    db = get_db()
    if dataType in ('int', 'tinyInt'):
        value = str(value)

    sql = 'select ' + fieldNm + ' from ' + dbNm + '.' + sourceName 
    sql += ' where catName ="' + strainName + '" and ' + capName + ' = "' + value + '"'
    #print('115: ',sql)
    results=db.query(sql)
    selList = []

    i = 0
    for row in results:
        rowDict = dict(row)
        selList.insert(i,rowDict[fieldNm])
        i += 1
    #print('124: ', dataType, ' : ',selList, fieldNm,':', value)
    return selList
'''

def getListViewName(formID):
    db = get_db()
    sql = 'select id, name from dframe.list_view where formID=' + str(formID)
    sql += ' UNION select 0 AS id, " " AS NAME ORDER BY id '
    results=db.query(sql)
    selList = []

    i = 0
    for row in results:
        rowDict = dict(row)
        selList.insert(i,rowDict)
        i += 1
    
    #print('fg159: ', formID, selList)    
    return selList

def getViewInfo(viewID):
    db = get_db()
    sql = 'select f.id, f.listViewID, v.name, v.formID, f.fieldNameCpt, f.fieldName '
    sql += ', f.fieldOperatorCpt, f.fieldOperator, f.value, f.andOr, strOrderBy '
    sql += ' from dframe.list_view v left join dframe.list_view_filter f on f.listViewID=v.id '
    sql += ' where v.id = ' + str(viewID)
    sql += ' order by f.id '
    results=db.query(sql)
    viewFltrList = []

    i = 0
    for row in results:
        rowDict = dict(row)
        viewFltrList.insert(i,rowDict)
        i += 1
    print('fg163:', viewFltrList)
    return viewFltrList

# to provide the form title string
def getFormCaption(formID, baseTableNm):
    db = get_db()
    sql = 'select caption from dframe.form '
    sql += ' where (' + str(formID) + '>0 AND id =' + str(formID) + ')'
    sql += '  OR (name="' + baseTableNm + '") LIMIT 1'
    results=db.query(sql)
    selList = []

    i = 0
    for row in results:
        rowDict = dict(row)
        selList.insert(i,rowDict)
        i += 1
    if len(selList) > 0:
        return selList[0]['caption']
    else:
        return ''

def getObjFldVal(tableNm, id, fldNm, dframe = 1):

    db = get_db()
    sql = 'select ' + fldNm + ' as name from '     
    if dframe !=1:
        sql += getAppName() + '.' 
    sql += tableNm + ' where id =' + str(id) 
    results=db.query(sql)
    selList = []

    i = 0
    for row in results:
        rowDict = dict(row)
        selList.insert(i,rowDict['name'])
        i += 1
    if len(selList) > 0:
        print(selList)
        return selList[0]
    else:
        return ''


'''    not used
def getObjFldVal(tableNm, id, fldNm):
    print('fg220: ', tableNm, id, fldNm)
    dbNm = getAppName()
    db = get_db()
    sql = 'select ' + fldNm + ' as name from ' + dbNm + '.' + tableNm
    sql += ' where id =' + str(id) 
    print('fg225: ', sql)
    results=db.query(sql)
    selList = []

    i = 0
    for row in results:
        rowDict = dict(row)
        selList.insert(i,rowDict['name'])
        i += 1
    if len(selList) > 0:
        print(selList)
        return selList[0]
    else:
        return ''

def getBaseValueList__notUsed():
    dbNm = getAppName()
    db = get_db()
    sqlCat = 'select catName from ' + dbNm + '.base_value '
    sqlCat += ' group by catName order by catName, seq'
    cursorCat = db.query(sqlCat)
    
    sqlVal = 'select catName, caption, value from ' + dbNm + '.base_value '
    sqlVal += ' order by catName, seq'
    cursorVal = db.query(sqlVal)
    # selList = [[catNm1, [ [[caption],[value]], [[],[]] ] ],... ]
    rowList = []   # [ row1, row2, ...]
    selDict = {}   # { catName1:rowList1, catName:rowList2, ..}
    catNm = ''

    for row in cursorVal:
        if catNm != row['catName'] and catNm > '':
            selDict[catNm] = rowList
            rowList = []

        aRow = [row['caption'],row['value']]
        rowList.append(aRow)
        catNm = row['catName']
    #print('fg217:', selDict)
    return selDict
'''  

def updDataLine(dataTableNm, id, setBody):
    dbNm = getAppName()
    db = get_db()
   
    sql = 'UPDATE ' + dbNm + '.' + dataTableNm + ' SET ' + setBody + ' WHERE id =' + str(id)

    db.query(sql)


def insDataLine( dataTableNm, flddNmChain, dtValChain):
    dbNm = getAppName()
    db = get_db()
    
    sql = 'INSERT INTO ' + dbNm + '.'  + dataTableNm + ' (' + flddNmChain.rstrip(',') + ') VALUES (' + dtValChain.rstrip(',') + ')'
    db.query(sql)

    sql = 'SELECT LAST_INSERT_ID() AS id'
    results = db.query(sql)
    
    for row in results:
        rowDict = dict(row)
    #print('ig290:',rowDict, rowDict['id']) 
    return rowDict['id']


def upsertDataLine(dataTableNm, fieldNm, dataValue, updtFormula, dframe = 1):

    dbNm = 'dframe'
    if dframe == 0:
        dbNm = getAppName()
    db = get_db()
   
    sql = 'INSERT INTO ' + dbNm + '.' + dataTableNm 
    sql += ' (' + fieldNm.rstrip(',') + ')'
    sql += ' VALUES (' + dataValue.rstrip(',') + ')'
    sql += ' ON DUPLICATE KEY UPDATE ' + updtFormula
    print('fg302:', sql)
    
    db.query(sql)

    sql = 'SELECT LAST_INSERT_ID() AS id'
    results = db.query(sql)
    
    for row in results:
        rowDict = dict(row)
    return rowDict['id']

def deleteData(dataTableNm, id, dframe = 1):
    
    db = get_db()
    sql = 'DELETE FROM '
    if dframe == 0:
        sql += getAppName() + '.'
    sql += dataTableNm + ' WHERE id =' + str(id)
    print('fg309:', sql)
    db.query(sql)

def execDb(sql):
    
    db = get_db()
    
    results = db.query(sql)
    #results = db.query('select LAST_INSERT_ID() id')
    selList = []

    i = 0
    for row in results:
        rowDict = dict(row)
        selList.insert(i,rowDict['id'])
        i += 1
    if len(selList) > 0:
        return selList[0]
    else:
        return ''