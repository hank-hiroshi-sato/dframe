import math
from tokenize import String
from flask import  Blueprint
from flask import Flask, render_template, url_for, request, redirect
from . import formInfoGetter

search_app = Blueprint('search', __name__)

# from the single data form(mom): after request to select its upper class object id term
#    --param: "formID"(mom's),"formFldNo", "roleID"  
#    --function: to build form containg the search word input area
# form the serach forn(child): after input serch word on the Search Form
#    --param: "formID"(search tatget object), "serarch" , "roleID"
#    --function: to build the list of data containing the search word
@search_app.route('/dframe/fsel/<int:momFormID>/<int:formFldNo>/<int:roleID>',  methods=['GET','POST'])
def searchForm(momFormID,formFldNo,roleID):
    
    offsetValue = 0   
    numOfFilters = 5
    lineNumPerPage = 8      # max number of lines per Page 
    searchFormID = 9200    
    # momFormID: mom's formID (from mom)   search object's formID(from search form)
    #momFormID = request.args.get('formID')   # the formID of the targer object
    #roleID =  int(request.args.get('roleID'))   # the roleID of the current session
    #formID = request.args.get('formID')

    # if comes from mom form , get the upper object's formID
    #formFldNo = request.args.get('formFldNo')   # the field position of the terger object
    #if formFldNo is not None:
    #    formFldNo = int(formFldNo)
    momFormPath = [momFormID, roleID, "'", 0, 0]
    formColumns = formInfoGetter.getFormInfo('FormColumns', momFormPath) 
    tableNm = formColumns[formFldNo]['cmbDataSource']
    #tableNm = tableNm.split(' ')[0]  # cutoff alias on the colum definition
    formID = formInfoGetter.execDb('SELECT id FROM form WHERE name="' + tableNm.split(' ')[0] + '"')
    derivedTerm = formColumns[formFldNo]['derivedTerm']
    fieldCaption = formColumns[formFldNo]['caption']
    fieldNm = formColumns[formFldNo]['name']
    print('v74:',formID,tableNm,derivedTerm,fieldCaption,fieldNm)
    formID = int(formID)
    formCaption = formInfoGetter.getFormCaption(formID,'""') 
    # child info:
    searchWord = request.form.get('search')    # search word input on the child form
    if searchWord is None:
        searchWord = '%'

    print('v60:',searchWord, formFldNo)
    
    # searchForm structure: formType= 'ｌ1', data = mom's upper object data items
    # BUILD FORM
    searchPath = [searchFormID, roleID, '""', 0, 0]  
    formPrpty = formInfoGetter.getFormInfo('FormPrpty', searchPath)
    formColumns = formInfoGetter.getSubFormInfo('Columns', tableNm, fieldNm, fieldCaption )
    formData = formInfoGetter.getSubFormInfo('Data', tableNm, fieldNm, fieldCaption, derivedTerm=derivedTerm, 
                            searchWord=searchWord, lineNumPerPage=10000, offset=0)
    #print('v95:',formData[0],formColumns)
    formCaption = formInfoGetter.getFormCaption(0,tableNm)  

    volOfLines = len(formData)
    volOfPages = math.ceil(volOfLines/lineNumPerPage) 
    offset = 0   # ??
    if offset == -1:
        offset = (volOfPages -1) * lineNumPerPage 

    fldList = []
    for c in formColumns :
        fldList.append(c['name'])

    return render_template(
        'searchForm.html',
            html_title='dFrame', dframe_title='dFrame' if not formPrpty[0]['Title'] else formPrpty[0]['Title'],
            momFormID=momFormID,
            fieldNm=fieldNm,
            formCaption=formCaption,
            formColumns=formColumns,
            formFldNo = formFldNo,
            fldList = fldList,
            formData=formData
    )
