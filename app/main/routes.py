#!/src/bin/env python3
from flask import Flask, request, render_template, flash, redirect, url_for
from .forms import ProfileForm
from ..models import db, Teacher, Student, Class, Course
from . import main
from .utils import generate_temp_password, send_temp_password_email