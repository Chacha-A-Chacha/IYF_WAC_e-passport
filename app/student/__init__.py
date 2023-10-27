#!/usr/bin/env python3
from flask import Blueprint

student_bp = Blueprint('student', __name__)

from . import routes
