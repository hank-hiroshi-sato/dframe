import math
from tokenize import String
from flask import  Blueprint
from flask import Flask, render_template, url_for, request, redirect
#from fieldBuilder import updateData,saveFilter
from . import formInfoGetter 
from . import trailKeeper
from . import commonTool


viewEdit_app = Blueprint('select', __name__)

#filter editing form: a view definition file is consisted by ond/or more 
# filter definition lines, those are combined by ana/or to each other
@viewEdit_app.route('/dframe/view/<int:formID>/<int:roleID>/<int:viewID>/' ,
          methods=['GET','POST'])
def viewForm(formID, roleID, viewID):
    filterFormID = 9200

    DFcpath = [filterFormID, roleID, viewID]
    print('v151:', DFcpath,  formID)

    trailKeeper.pushTrail(DFcpath)
   
    # BUILD FORM
    formParam = commonTool.setFormParam(DFcpath, 100, 0, 0)
    #return [formPrpty,formColumns,formData,formButton,fldList,fldVal,idList]

    fldList = []        #files names of filterBuilder Form(9200)
    for c in formParam[1] :               # get Col name for formColumn
        fldList.append(c['name'])

    fldVal = []         #field values for filterBuilder Form(9200)
    fldRec = []         #field names 
    for d in range(len(formParam[2])) :      # num of lines of filters on formData
        for fldNm in fldList  :             # col name of filterBuilder Form(9200)
            fldRec.append(str(formParam[2][d][fldNm])) # filter set(filter field values)
        fldVal.append(fldRec)               # [[1st filter set],[...]]
        fldRec = []
    #print('v174:', len(formData),fldVal, ' viewName:',viewName, viewID, viewSelFldList)
    #print('v175:', baseValueList)
    lenFormData = len(formParam[2])

    btnList = []
    for b in formParam[3]:     # formButton
        btnList.append(b['actionType'])
        
    return render_template(
        'filterBuild.html',
        viewID = viewID,
        viewName = formInfoGetter.getObjFldVal("list_view", viewID, "name", dframe=1),
        formID=formID,
        roleID=roleID,
        formPrpty= formParam[0],
        formColumns = formParam[1],
        formData= formParam[2],
        formButton=formParam[3],
        fldList = formParam[4],
        idList = formParam[6],
        lenFormData=lenFormData,
        fldVal=fldVal,
        viewSelFldList =  formInfoGetter.getSelectList('view','""',formID ),
        baseValueList = formInfoGetter.getSelectList('lookup', 'base_value', 0 ),
        btnList = btnList,
        message=''
    )
