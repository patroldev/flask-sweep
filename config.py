"""
File: config.py
Purpose: config for the app
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfiguration(object):
    # We disable CSRF because it interferes with logging in
    # from anywhere but the form on the login page.
    # We introduce very little risk by disabling this.
    WTF_CSRF_ENABLED = False
    # Make this random (used to generate session keys)
    SECRET_KEY = '123456789abcdef123456789'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sweep.sqlite3')
    DEBUG = True

class TestConfiguration(BaseConfiguration):
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True
