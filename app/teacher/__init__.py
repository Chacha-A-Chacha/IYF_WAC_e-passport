#!/usr/bin/env python3
from flask import Blueprint

teacher_bp = Blueprint('teacher', __name__)

from . import routes
