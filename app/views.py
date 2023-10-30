from flask import Flask, request, render_template, flash, redirect, url_for

from . import app

app.route("/")
def index():
    return render_template("landing_page.html")