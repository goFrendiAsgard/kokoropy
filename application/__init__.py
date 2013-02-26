# -*- coding: utf-8 -*-

#########################################################################
#
# MAIN KOKOROPY PROGRAM
# * This will load all of your controllers and views
# * Normally there is no need to edit this file
#
#########################################################################

__version__ = '0.1'
from kokoropy.bottle import Bottle
import os

#########################################################################
# initialize bottle
#########################################################################
app = Bottle()