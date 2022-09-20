import copy, math
import tkinter as tk
from tkinter.constants import W
import tkinter.messagebox as tkm
from tkinter import StringVar, ttk
from flask import Flask, render_template, url_for, request, redirect
from tokenize import String
from . import formInfoGetter

def setFormParam(DFcpath, lineNumPerPage, offsetValue, viewID):
    formPrpty =   formInfoGetter.getFormInfo('FormPrpty',   DFcpath, '', lineNumPerPage, offsetValue, viewID)
    formColumns = formInfoGetter.getFormInfo('FormColumns', DFcpath, '', lineNumPerPage, offsetValue, viewID)
    formData =    formInfoGetter.getFormInfo('FormData',    DFcpath, '', lineNumPerPage, offsetValue, viewID)
    formButton =  formInfoGetter.getFormInfo('FormXmit',    DFcpath, '', lineNumPerPage, offsetValue, viewID)
        
    fldList = []
    for c in formColumns :
        fldList.append(c['name'])
       
    fldVal = []       #field values for single form deployment
    if len(formData) > 0:
        for fldNm in fldList  :
            fldVal.append(str(formData[0][fldNm]))
        #else:
        #    fldVal.append(None)

    idList = []
    for d in formData :
        idList.append(d['id'])

    return [formPrpty,formColumns,formData,formButton,fldList,fldVal,idList]


def setUrl(DFcpath):
    # url path of the current form
    urlPath = ''
    for p in DFcpath:
        #print('v95:',p,type(p),urlPath)
        urlPath += '/'
        if type(p) is int :
            urlPath += str( p ) 
        elif type(p) is String:
            urlPath += p 
        else:
            urlPath += "%27%27"
    return urlPath + '/'


def setPageButton(DFcpath, lineNumPerPage, offsetValue, viewID):
    volOfLines=0
    pageBtnOnOff = ['', '', '', '']     # html: 'disabled' vs ''
    pageOffset = [0,0,0,0]

    formData = formInfoGetter.getFormInfo('FormData', DFcpath,'', offset=0, viewID=viewID) 
    volOfLines = len(formData)
    volOfPages = math.ceil(volOfLines / lineNumPerPage) 
    pageOffset = [0,                            # top page
                max(0,offsetValue - lineNumPerPage),     # prev page
                offsetValue + lineNumPerPage,     # next page
                (volOfPages -1 ) * lineNumPerPage] # last page
    if offsetValue < lineNumPerPage:
        pageBtnOnOff[0] = 'disabled'
        pageBtnOnOff[1] = 'disabled'
    if offsetValue >= volOfLines - lineNumPerPage:
        pageBtnOnOff[2] = 'disabled'
        pageBtnOnOff[3] = 'disabled'

    return [pageOffset, pageBtnOnOff]

def lapFld(dataType, value):
    fld = ""
    #print('ct11: ',dataType,len(value))
    if value == None:
        None
    elif dataType in ('text', 'int'):
        fld = '"' + value  + '"'                
    elif dataType in ('date'):
        if len(value) >= 10:
            #fld = '"' + value.strftime('%y-%m-%value')   + '"'
            fld = '"' + value + '"'
        else:
            fld = '"0000-00-00"'             
    elif dataType in ('datetime'):
        if len(value) > 10:
            #fld = '"' + value.strftime('%y-%m-%value %H;%M:%S')   + '"'
            fld = '"' + value + '"'
        else:
            fld = '"0000-00-00 00:00:00"'             
    else:
        fld =  str(value)
    return fld


def destroyFields(self, hdr_frm, page_frm, navi_frm):
    #frameを初期化
    myFields = self.data_frm.winfo_children()
    for field in myFields:
        field.destroy()

    myHdr = hdr_frm.winfo_children()
    for hdr in myHdr:
        hdr.destroy()

    myButtons = navi_frm.winfo_children()
    for button in myButtons:
        button.destroy()
    btnGridInfo = tk.Button.grid_info(self.data_frm)
    tk.Button.grid_forget(self.data_frm)

    return len(myFields.field)

# build a SQL phrase like ' field-name = data ' for update operation, 
#                         ' field-name1, field-name2... and field-data1, field-data2... for insert operation
# note: data to be presented as int, text, datetime etc
def buildUpdateFldTerms(isUpdate, colNm, data, dtType):
    print('c116:',isUpdate, colNm, data, dtType)
    if isUpdate == True:   # if update operation , formurate (col-name = input value)
        body = colNm + '=' + lapFld(dtType, data) + ' ,' 
        print('c119:',isUpdate, colNm, dtType, data, body)
        return body
    # if create data, formurate field-name-string and input value string
    else: 
        if data != None and len(data) > 0:
            fld = colNm + ','
            data = lapFld(dtType,data )+ ','
        else:
            fld = ''
            data = ''
        print('c129:', fld, data)
        return fld,data



#更新ボタン押下で呼び出される        
def updateData(reqForm, DFcpath, lineNumPerPage, offset):
    formColumns = formInfoGetter.getFormInfo('FormColumns', DFcpath)
    formData = formInfoGetter.getFormInfo('FormData', DFcpath, '', lineNumPerPage, offset, 0)
    formPrpty = formInfoGetter.getFormInfo('FormPrpty', DFcpath)
    dataTableNm = formPrpty[0]['baseTableNm']
    print('c140:', DFcpath,len(formData),'formCol:',formColumns[1])
    modeSearch = 'n'
    body = ''
    fld = ''
    data = ''
    isUpdate = bool
    #y:データ表示開始行　単票；１行目　一覧：２行目  ViewForm:０行目
    y = 1
    if formPrpty[0]['formType'] == 'lf':
        y = 0
    elif formPrpty[0]['formType'] != 's':
        y = 2
    #Update
    if len(formData) > 0:
        isUpdate = True
        for line in formData:   #update
            id = int
            for c in formColumns:
                if c['name'] == 'id':
                    id = line['id']
                elif c['baseTable'] != None and c['isReadOnly']==0 and c['foreignKeyFldNm']==None:
                    if formPrpty[0]['formType'] == 's':
                     d = reqForm.get(c['name'])
                    else:
                     d = reqForm.get(str(y) + '_' + c['name'])

                    print('c161: ',y, id,c['name'],d)
                    result = buildUpdateFldTerms(isUpdate, c['name'], d, c['dataType'])
                    body += result
                    print('c162: ','result:',result,'body:',body,'lineNo:',y,formPrpty[0])
                
            body = body.rstrip(',') 
            #print('c167:', dataTableNm, id, body)
            formInfoGetter.updDataLine(dataTableNm, id, body)
            id = ''
            body = ''
            if formPrpty[0]['formType'] != 's' :   #for list form or view form, increase line no
                y += 1

    #insert  :it always be single form
    else:
        isUpdate = False
        print('***',reqForm.get('fieldName'))
        for c in formColumns:
            if c['name'] != 'id' and c['baseTable'] != None and c['isReadOnly']==0 and c['foreignKeyFldNm']==None:
                d = reqForm.get(c['name'])
                if d > "" :
                    result = buildUpdateFldTerms(isUpdate, c['name'], d, c['dataType'])
                    fld += result[0] 
                    data +=  result[1] 
                    print('c182: ',c['name'],'d:',d,' fld:',fld,' data:',data,'result:',result,'lineNo:',y)
            y += 1
        body = body.rstrip(',') 
        print('c185:', fld,data)
        if len(fld) > 0:
            formInfoGetter.insDataLine(dataTableNm, fld, data)


def updateFilter(formID, viewID, viewNm, filterSpec, roleID):
    print('v528:', filterSpec)    
    # upsert list_view table
    fieldNm = 'id,name,formID,modifiedBy,modifiedAt'
    dataValue = str(viewID) + ',"' + viewNm + '",' + str(formID) + ',' + str(roleID)
    dataValue += ', CURRENT_TIMESTAMP'
    setBody = 'name="' + viewNm + '",formID=' + str(formID)
    setBody += ', modifiedBy=' + str(roleID) + ',modifiedAt=CURRENT_TIMESTAMP'
    if viewID >=1:
        formInfoGetter.upsertDataLine('list_view', fieldNm, dataValue, setBody, dframe=1)
    else:
        viewID = formInfoGetter.insDataLine('list_view', fieldNm, dataValue)

    # upsert list_view_filter table
    # ['_id', '_fieldName', '_fieldOperator', '_value', '_andOr']
    filterFieldNm = ''
    
    fieldDataType = ['','"','"','"','"']  #int or string
    for s in range(len(filterSpec)):
        dataValue = str(viewID) 
        setBody = ''
        # filterSpec: [[list_view_filter line_no],[id,fieldNm,fieldOp,value,andOr]]
        for d in range(len(filterSpec[s])):
            if filterSpec[s][0] > '' or d > 0:    #for new line to skip 'id' term
                dataValue += ',' + fieldDataType[d] + filterSpec[s][d] + fieldDataType[d]
        
        if filterSpec[s][0] > '':       # if not new line
            for i in range(4):
                if len(filterSpec[s][i]) == 0:
                    formInfoGetter.deleteData('list_view_filter',filterSpec[s][0], dframe=1)
                    print('c159:', s, filterSpec[s][0])
                    break
            else:
                filterFieldNm = 'listViewID,id,fieldName,fieldOperator,value,andOr'
                setBody = 'fieldName="' + filterSpec[s][1] + '"'
                setBody += ', fieldOperator="' + filterSpec[s][2] + '"'
                setBody += ', value="' + filterSpec[s][3] + '"'
                setBody += ', andOr="' + filterSpec[s][4] + '"'
                print('c166:', s, d, setBody)
                formInfoGetter.upsertDataLine('list_view_filter', filterFieldNm, dataValue, setBody, dframe=1)
        else:                           # new line
            filterFieldNm = 'listViewID,fieldName,fieldOperator,value,andOr'
            formInfoGetter.insDataLine('list_view_filter', filterFieldNm, dataValue)
            print('c171:', filterSpec[s][0], dataValue)
 