#!/usr/bin/env python
# encoding: utf-8

class BaseConfig(object):
    'Base Config class'
    SECURTY_KEY='A random secret key'
    DEBUG = True
    TESTING = False
    NEW_CONFIG_VARIABLE ='my value'


class ProductionConfig(object):
    'Production kConfig class'
    SECURTY_KEY=open('/path/to/secret/file')
    DEBUG = False
    TESTING = False
    NEW_CONFIG_VARIABLE ='my value'

class StagingConfig(object):
    DEBUG = True

class DevelopmentConfig(object):
    DEBUG = True
    TESTING = True
    SECURITY_KEY= 'A random secret key'
