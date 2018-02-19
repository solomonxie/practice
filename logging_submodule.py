#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


#----------------------------------------------------------------------
def add(x, y):
    """"""
    log = logging.getLogger("exampleClass.submodule.add")
    log.info("added %s and %s to get %s" % (x, y, x+y))
    return x+y

