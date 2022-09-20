from flask import Flask

globals()['trail'] = []

def pushTrail(cpath):
    if len(globals()['trail']) == 0 or cpath != globals()['trail'][-1]:
        globals()['trail'].append(cpath)           # push the trail
    print('**push**', globals()['trail'])
    return globals()['trail']

def popUpTrail():
    del globals()['trail'][-1]
    print('**popUp**', globals()['trail'])
    if len(globals()['trail']) > 0:
        return globals()['trail'][-1]
    else:
        return []

def getCurrPath():
    print('**currPath**', len(globals()['trail']) ,globals()['trail'])
    if len(globals()['trail']) > 0:
        return globals()['trail'][-1]
    else:
        return []

