#!/usr/bin/env pyhton3
# -*- coding: utf-8 -*-
"""
@Author         :  $$$$$$$ ($$$$$$$@mails.ucas.ac.cn)
@Created time   :  2021/9/7 $$$$$$$$

@Last modified  :  2021/9/  $$$$4:36
"""
import app
from app import db
from app.models import Class, Course

# import torch
# from sklearn import metrics
# from .base_metric import BaseMetric
# __all__ = ["Accuracy", "Precision", "Recall"]
# class Accuracy(BaseMetric):
#     def __init__(self, name="acc"):
#         super().__init__(name=name)
#         def calculate(self, y_true, y_pred):
#             return metrics.accuracy_score(y_true, y_pred)
#             self._calculate = calculate
#             class Precision(BaseMetric):
#                 def __init__(self, name="precision"):
#                     super().__init__(name=name)
#                     def calculate(self, y_true, y_pred):
#                         return metrics.precision_score(y_true, y_pred, average='weighted')
#                         self._calculate = calculate
#                         class Recall(BaseMetric):
#                             def __init__(self, name="recall"):
#                                 super().__init__(name=name)
#                                 def calculate(self, y_true, y_pred):



# List of courses and their associated class names
courses_data = [
    {
        "course_name": "Mathematics",
        "class_names": ["Math Class A", "Math Class B"]
    },
    {
        "course_name": "Science",
        "class_names": ["Science Class A", "Science Class B"]
    },
    {
        "course_name": "Beauty & Hair",
        "class_names": ["Beauty & Hair Class A", "Beauty & Hair Class B"]
    },
    {
        "course_name": "Graphics",
        "class_names": ["Graphics Class A", "Graphics Class B"]
    },
    {
        "course_name": "Programming",
        "class_names": ["Programming Class A", "Programming Class B"]
    },
    {
        "course_name": "Video Editing",
        "class_names": ["Video Editing Class A", "Video Editing Class B"]
    },
    {
        "course_name": "Camera Operation",
        "class_names": ["Camera Operation Class A", "Camera Operation Class B"]
    },
    {
        "course_name": "Computer Packages",
        "class_names": ["Computer Packages Class A", "Computer Packages Class B"]
    },
    {
        "course_name": "Football",
        "class_names": ["Football Class A", "Football Class B"]
    },
    {
        "course_name": "Taekwondo",
        "class_names": ["Taekwondo Class A", "Taekwondo Class B"]
    },
    {
        "course_name": "Sign Language",
        "class_names": ["Sign Language Class A", "Sign Language Class B"]
    },
    {
        "course_name": "Dance",
        "class_names": ["Dance Class A", "Dance Class B"]
    },
    {
        "course_name": "Korean",
        "class_names": ["Korean Class A", "Korean Class B"]
    },
    {
        "course_name": "Chinese",
        "class_names": ["Chinese Class A", "Chinese Class B"]
    },
    {
        "course_name": "Japanese",
        "class_names": ["Japanese Class A", "Japanese Class B"]
    },
    {
        "course_name": "French",
        "class_names": ["French Class A", "French Class B"]
    },
    {
        "course_name": "Mind Education",
        "class_names": ["Mind Education Class A", "Mind Education Class B"]
    },
    {
        "course_name": "Theology",
        "class_names": ["Theology Class A", "Theology Class B"]
    },
    {
        "course_name": "Music",
        "class_names": ["Music Class A", "Music Class B"]
    }
]


# Use the app context to work within the application
with app.app_context():
    
    # Initialize courses and classes in the database
    for course_info in courses_data:
        course_name = course_info["course_name"]
        class_names = course_info["class_names"]
        
        # Create the course
        course = Course(course_name=course_name)
        db.session.add(course)
        db.session.commit()  # Commit course to get the course ID
        
        # Create classes for the course
        for class_name in class_names:
            class_obj = Class(class_name=class_name, course=course)
            db.session.add(class_obj)

        # Commit the changes for classes related to the current course
        db.session.commit()

    # Commit the final changes to the database
    db.session.commit()
                                                                                                                                                                                                             
                                                                                                                                                                                                             
print("Courses and classes initialized successfully.")
