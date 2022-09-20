import math
from tokenize import String
from flask import  Blueprint
from flask import Flask, render_template, url_for, request, redirect
#from fieldBuilder import updateData,saveFilter
from . import formInfoGetter 
from . import trailKeeper

'''
select_app = Blueprint('select', __name__)

#filter editing form: a view definition file is consisted by ond/or more 
# filter definition lines, those are combined by ana/or to each other
@select_app.route('/dframe/view/<int:formID>/<int:roleID>/<int:viewID>/' ,
          methods=['GET','POST'])
def viewForm(formID, roleID, viewID):
    filterFormID = 9200
    offsetValue = 0   
    baseValueList = formInfoGetter.getSelectList('lookup', 'base_value', 0 )

    DFcpath = [filterFormID, roleID, '""', viewID, 0]
    print('v151:', DFcpath,  formID)
    trailKeeper.pushTrail(DFcpath)
    viewName = formInfoGetter.getObjFldVal("list_view", viewID, "name", dframe=1)
    tableNm = formInfoGetter.getObjFldVal('form', formID, 'name', dframe=1)
    #field selection list for view
    viewSelFldList = formInfoGetter.getSelectList('view','""',formID )
    
    formColumns = formInfoGetter.getFormInfo('FormColumns', DFcpath)
    formData = formInfoGetter.getFormInfo('FormData', DFcpath, '', 100, offsetValue, 0)

    fldList = []        #files names of filterBuilder Form(9200)
    for c in formColumns :
        fldList.append(c['name'])

    fldVal = []         #field values for filterBuilder Form(9200)
    fldRec = []         #field names 
    for d in range(len(formData)) :         # num of lines of filters
        for fldNm in fldList  :             # col name of filterBuilder Form(9200)
            fldRec.append(str(formData[d][fldNm])) # filter set(filter field values)
        fldVal.append(fldRec)               # [[1st filter set],[...]]
        fldRec = []
    #print('v174:', len(formData),fldVal, ' viewName:',viewName, viewID, viewSelFldList)
    #print('v175:', baseValueList)
    lenFormData = len(formData)
            
    formButton = formInfoGetter.getFormInfo('FormXmit', DFcpath)
    btnList = []
    for b in formButton:
        btnList.append(b['actionType'])
        
    return render_template(
        'filterBuild.html',
        viewID = viewID,
        viewName = viewName,
        formID=formID,
        roleID=roleID,
        formColumns=formColumns,
        formData=formData,
        lenFormData=lenFormData,
        fldVal=fldVal,
        formButton=formButton,
        viewSelFldList = viewSelFldList,
        baseValueList = baseValueList,
        btnList = btnList,
        message=''
    )
'''