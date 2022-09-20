import functools

import math
from tokenize import String
from traceback import format_tb
from urllib.parse import urlparse
from flask import  Blueprint
from flask import Flask, render_template, url_for, request, redirect

#from fieldBuilder import updateFldTerms
#from fieldBuilder import updateData,saveFilter
from . import formInfoGetter
from .commonTool import  updateFilter, setFormParam, setUrl, setPageButton,buildUpdateFldTerms,updateData
from . import trailKeeper

navi_app = Blueprint('navi', __name__)
lineNumPerPage = 8 
numOfFilters =5

class renderTemplate:
    def __init__(self, f='',d=[],o=0,v=0):
        self.formType = f
        self.DFcpath  = d
        self.offsetValue = o
        self.viewID   = v


    def render(self):
        # url path of the current form
        urlPath = setUrl(self.DFcpath)

        # BUILD FORM
        formParam = setFormParam(self.DFcpath, lineNumPerPage, self.offsetValue, self.viewID)
        btnList = []
        for b in formParam[3]:
            btnList.append(b['actionType'])
        #return [formPrpty,formColumns,formData,formButton,fldList,fldVal,idList]
        pagenation =  setPageButton(self.DFcpath,lineNumPerPage, self.offsetValue, self.viewID)
        #return [pageOffset, pageBtnOnOff]
        
        if self.formType != 's':
            return render_template(
            #    'dframe_' + DFtemplateType + '.html',
                'list1.html',
                urlPath = urlPath,
                formID = self.DFcpath[0],
                roleID = self.DFcpath[1],
                baseFormID =  formParam[0][0]['baseFormID'],
                formPrpty=    formParam[0],
                formColumns = formParam[1],
                formData=     formParam[2],
                formButton=   formParam[3],
                fldList =     formParam[4],
                idList =      formParam[6],
                listViewName = formInfoGetter.getListViewName(self.DFcpath[0]),
                viewID = self.viewID,
                pageOffset =   pagenation[0],
                pageBtnOnOff = pagenation[1],
                pageButton =['t', 'p', 'n', 'l'],    # pageTop, pagePrev, pageNext, pageLast
                pageBtnCap = ['Top', 'Prev', 'Next', 'Last']
            )
        else:
            return render_template(
        #    'dframe_' + DFtemplateType + '.html',
            'sForm.html',
            urlPath = urlPath,
            formID = self.DFcpath[0],
            roleID = self.DFcpath[1], 
            baseValueList = formInfoGetter.getSelectList('lookup', 'base_value', 0 ),
            formPrpty=formParam[0],
            formColumns=formParam[1],
            formButton=formParam[3],
            btnList = btnList,
            fldVal  = formParam[5]
        )


@navi_app.route('/dframe/navi/form/<int:formID>/<int:roleID>/<int:objID>/', methods=['GET', 'POST'])
def deployForm(formID, roleID, objID):
    DFcpath = [formID, roleID, objID]
    ft = formInfoGetter.getFormInfo(None, None, 
        'SELECT formType FROM form WHERE id=' + str(formID))
    formType = ft[0]['formType']
    viewID = 0
    viewSelID = request.form.get('viewSelID')  # selected in List Form
    offsetValue = 0   
    if formType != 's':
        offset = request.args.get('offset')
        # when pagenation selected
        if offset is not None:
            offsetValue = int(offset)

        # is a view selected? 
        if viewSelID is None:           # No, transit other form
            trailKeeper.pushTrail(DFcpath)
        else:                           # Yes, stay the current form with new view
            DFcpath = trailKeeper.getCurrPath()
            viewID = int(viewSelID)
            offsetValue = 0
    else:
        trailKeeper.pushTrail(DFcpath)
    print ('n101:trail ', ' cpath:', DFcpath, formType, 'viewID:', viewID, viewSelID)
    #renderTemplate(formType, DFcpath, offsetValue, viewID)
    render = renderTemplate(formType, DFcpath, offsetValue, viewID)
    render.render()

    urlPath = setUrl(DFcpath)
    if viewID > 0:
        urlPath += '?viewID=' + str(viewID)

    # BUILD FORM
    formParam = setFormParam(DFcpath, lineNumPerPage, offsetValue, viewID)
    #return [formPrpty,formColumns,formData,formButton,fldList,fldVal,idList]

    btnList = []
    for b in formParam[3]:       # formButton
        btnList.append(b['actionType'])

    pagenation =  setPageButton(DFcpath,lineNumPerPage, offsetValue, viewID)
    listViewName = formInfoGetter.getListViewName(DFcpath[0])
    print('n120:', viewID,listViewName, urlPath)
    
    if formType != 's':
        return render_template(
        #    'dframe_' + DFtemplateType + '.html',
            'list1.html',
            urlPath = urlPath,
            formID = DFcpath[0],
            roleID = DFcpath[1],
            baseFormID =  formParam[0][0]['baseFormID'],
            formPrpty=    formParam[0],
            formColumns = formParam[1],
            formData=     formParam[2],
            formButton=   formParam[3],
            fldList =     formParam[4],
            idList =      formParam[6],
            listViewName = listViewName,
            viewID = viewID,
            pageOffset =   pagenation[0],
            pageBtnOnOff = pagenation[1],
            pageButton =['t', 'p', 'n', 'l'],    # pageTop, pagePrev, pageNext, pageLast
            pageBtnCap = ['Top', 'Prev', 'Next', 'Last']
        )
    else:
        return render_template(
    #    'dframe_' + DFtemplateType + '.html',
        'sForm.html',
        urlPath = urlPath,
        formID = DFcpath[0],
        roleID = DFcpath[1], 
        baseValueList = formInfoGetter.getSelectList('lookup', 'base_value', 0 ),
        formPrpty=formParam[0],
        formColumns=formParam[1],
        formButton=formParam[3],
        fldVal  = formParam[5],
        btnList = btnList
    )


@navi_app.route('/dframe/navi/btn/<string:actType>/<int:formID>/<int:roleID>/', methods=['GET', 'POST'])
def naviButton(actType, formID, roleID):
    filterSpec = []     #each Detail Line on  Filter Editing Form
    filterItem = []     #Whole Filter Editing Lines
    viewID = 0
    viewNm = ''    
    view = request.args.get('viewID')  # to get ViewID on the Filter Editing Form
    if view is not None:
        viewID = int(view)

    DFcpath = []
    viewSelID = request.form.get('viewSelID')  # selected in List Form
    if viewSelID is not None:
        # Yes, stay the current form with new view
        DFcpath = trailKeeper.getCurrPath()
        viewID = int(viewSelID)
        print('v166:',viewID, DFcpath)
    else:
        # save the current data then Back to the previous form ?
        if actType == 'b':    # backward form
            if view is None:    # via single form not view edit form
                DFcpath = trailKeeper.getCurrPath()
                print('n159:',view,request.form.get('0_value'),request.form.get('0_andOr'),DFcpath)
                updateData(request.form, DFcpath, lineNumPerPage, 0)
                DFcpath = []
            else:               # via view edit form
                viewNm = request.form.get('viewName')
                for d in range(5):
                    if len(request.form.get(str(d) + '_fieldOperator')) > 0:
                        print('v246:',d,request.form.get(str(d) + '_andOr'))
                        for i in ['_id', '_fieldName', '_fieldOperator', '_value', '_andOr']:
                            #if i == '_andOr':                     # 臨時の逃げ：　andOrのデータ取得ができない
                            #    filterItem.append('or')
                            #else:                            
                                filterItem.append(request.form.get(str(d) + i))

                        filterSpec.append(filterItem)
                        filterItem = []
                filterSpec[-1][4] = ''    #delete "andOr" ont the last filter data line
                print('v251:',filterSpec, request.form['0_andOr'], request.form.get('1_andOr'))
                # to update Filter Data
                updateFilter(formID, viewID, viewNm, filterSpec, roleID)
            DFcpath = []

        # was Cacel button pressed?
        elif actType == 'c':   # cancel 
            DFcpath = []     
        # was to make New record button pressed?
        elif actType == 'n':   # make new record
            DFcpath = trailKeeper.getCurrPath()
            if formID != DFcpath[0] or formID == None:            # when single form, they have same formID
                trailKeeper.pushTrail(DFcpath)  # via list form , then push trail
                DFcpath[0] = formID     # formID
            DFcpath[2] = 0          # objID
        # was the delete button on the Filter Editing Form pressed?
        elif actType == 'd':
            formInfoGetter.deleteData('list_view', viewID, dframe=1)
            DFcpath = []     
            print('v206:', viewID)

    # SWITCHER
    if DFcpath == []:
        DFcpath = trailKeeper.popUpTrail()
        formID = DFcpath[0]
    ftyp = formInfoGetter.getFormInfo(None, None, 
        'SELECT formType FROM form WHERE id=' + str(formID))
    formType = ftyp[0]['formType']
    offsetValue = 0
    # url path of the current form
    urlPath = setUrl(DFcpath)
    if viewID != 0:
        urlPath = urlPath + '?viewID=' + str(viewID)
    print ('V226:trail ', urlPath,' cpath:', DFcpath, 'formType:', formType)

    # BUILD FORM
    formParam = setFormParam(DFcpath, lineNumPerPage, offsetValue, viewID)
    btnList = []
    for b in formParam[3]:
        btnList.append(b['actionType'])
    #return [formPrpty,formColumns,formData,formButton,fldList,fldVal,idList]
    pagenation =  setPageButton(DFcpath,lineNumPerPage, offsetValue, viewID)
    #return [pageOffset, pageBtnOnOff]
    
    if formType != 's':
        return render_template(
        #    'dframe_' + DFtemplateType + '.html',
            'list1.html',
            urlPath = urlPath,
            formID = DFcpath[0],
            roleID = DFcpath[1],
            baseFormID =  formParam[0][0]['baseFormID'],
            formPrpty=    formParam[0],
            formColumns = formParam[1],
            formData=     formParam[2],
            formButton=   formParam[3],
            fldList =     formParam[4],
            idList =      formParam[6],
            listViewName = formInfoGetter.getListViewName(DFcpath[0]),
            viewID = viewID,
            pageOffset =   pagenation[0],
            pageBtnOnOff = pagenation[1],
            pageButton =['t', 'p', 'n', 'l'],    # pageTop, pagePrev, pageNext, pageLast
            pageBtnCap = ['Top', 'Prev', 'Next', 'Last']
        )
    else:
        return render_template(
    #    'dframe_' + DFtemplateType + '.html',
        'sForm.html',
        urlPath = urlPath,
        formID = DFcpath[0],
        roleID = DFcpath[1], 
        baseValueList = formInfoGetter.getSelectList('lookup', 'base_value', 0 ),
        formPrpty=formParam[0],
        formColumns=formParam[1],
        formButton=formParam[3],
        btnList = btnList,
        fldVal  = formParam[5]
    )


@navi_app.route('/dframe/navi/viewBtn/<string:actType>/<int:viewID>/', methods=['GET', 'POST'])
def viewButton(actType, viewID):
    # get the DFcpath of mom-form
    DFcpath = trailKeeper.popUpTrail()
    viewNm = request.form.get('viewName')
    #  save Filter Data then Back to the list form?
    if actType == 'b' :    # backward form
        filterSpec = []     #each Detail Line on  Filter Editing Form
        filterItem = []     #Whole Filter Editing Lines
        for d in range(numOfFilters):
            if len(request.form.get(str(d) + '_fieldOperator')) > 0:
                print('v246:',d,request.form.get(str(d) + '_andOr'))
                for i in ['_id', '_fieldName', '_fieldOperator', '_value', '_andOr']:
                    #if i == '_andOr':                     # 臨時の逃げ：　andOrのデータ取得ができない
                    #    filterItem.append('or')
                    #else:
                    if request.form.get(str(d) + i) == 'None':
                        filterItem.append(0)  
                    else:                          
                        filterItem.append(request.form.get(str(d) + i))

                filterSpec.append(filterItem)
            print('v251:',filterSpec, request.form['0_andOr'], request.form.get('1_andOr'))
            if len(filterSpec) > 0:
                filterSpec[-1][4] = ''    #delete "andOr" ont the last filter data line
                # to update Filter Data
                updateFilter(DFcpath[0], viewID, viewNm, filterSpec, DFcpath[1])

    # was Cacel button pressed?
    elif actType == 'c':   # cancel 
        DFcpath = []     

    # was Delete button pressed?
    elif actType == 'd':
        formInfoGetter.deleteData('list_view', viewID, dframe=1)
        DFcpath = []     
    
    
    formType = formInfoGetter.getFormInfo(None, None, 
        'SELECT formType FROM form WHERE id=' + str(DFcpath[0]))

    # url path of the current form
    urlPath = setUrl(DFcpath)

    # BUILD FORM
    formParam = setFormParam(DFcpath, lineNumPerPage, 0, viewID)
    #return [formPrpty,formColumns,formData,formButton,fldList,fldVal,idList]
    pagenation =  setPageButton(DFcpath,lineNumPerPage, 0, viewID)
    #return [pageOffset, pageBtnOnOff]
    
    if formType != 's':
        return render_template(
        #    'dframe_' + DFtemplateType + '.html',
            'list1.html',
            urlPath = urlPath,
            formID = DFcpath[0],
            roleID = DFcpath[1],
            baseFormID =  formParam[0][0]['baseFormID'],
            formPrpty=    formParam[0],
            formColumns = formParam[1],
            formData=     formParam[2],
            formButton=   formParam[3],
            fldList =     formParam[4],
            idList =      formParam[6],
            listViewName = formInfoGetter.getListViewName(DFcpath[0]),
            viewID = viewID,
            pageOffset =   pagenation[0],
            pageBtnOnOff = pagenation[1],
            pageButton =['t', 'p', 'n', 'l'],    # pageTop, pagePrev, pageNext, pageLast
            pageBtnCap = ['Top', 'Prev', 'Next', 'Last']
        )
    else:
        return render_template(
    #    'dframe_' + DFtemplateType + '.html',
        'sForm.html',
        urlPath = urlPath,
        formID = DFcpath[0],
        roleID = DFcpath[1], 
        baseValueList = formInfoGetter.getSelectList('lookup', 'base_value', 0 ),
        formPrpty=formParam[0],
        formColumns=formParam[1],
        formButton=formParam[3],
        fldVal  = formParam[5]
    )

