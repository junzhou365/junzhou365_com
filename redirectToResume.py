from flask import Blueprint, redirect
home = Blueprint('home', __name__)

@home.route('/')
def redirectToResume():
    return redirect('/resume')
