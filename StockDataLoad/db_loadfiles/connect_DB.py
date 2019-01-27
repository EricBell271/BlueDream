# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 22:26:37 2018

@author: Eric Bell
"""


from psycopg2 import connect
    
BlueDream = connect(dbname="", user="",  password = '')
BlueDream.autocommit = True
