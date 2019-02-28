# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 22:26:37 2018

@author: Eric Bell
"""


from psycopg2 import connect


BlueDream = connect(dbname="BlueDreamDB", user="postgres",  password = 'ew1234')
BlueDream.autocommit = True
