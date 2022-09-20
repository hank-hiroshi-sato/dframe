import functools

from flask import  Blueprint
from flask import Flask, render_template, url_for, request, redirect
index_app = Blueprint('index', __name__)

@index_app.route('/')
def index():
    roleID = 1
    path = '/dframe/navi/form/0/' + str(roleID) + '/0/'
    #print('v46:', path)
    return redirect(path)