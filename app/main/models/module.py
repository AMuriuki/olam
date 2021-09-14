import enum
import os
import csv
from config import basedir
from app import db, current_app
import logging


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    technical_name = db.Column(db.String(128), index=True)  # technical name
    official_name = db.Column(db.String(128), index=True)  # technical name
    installed_version = db.Column(db.String(60))
    auto_install = db.Column(db.Boolean, default=False)
    state = db.Column(db.String(60))
    icon = db.Column(db.String(60))  # icon url
    enable = db.Column(db.Boolean, default=True)
    summary = db.Column(db.String(350))
