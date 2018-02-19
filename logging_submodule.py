#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


#----------------------------------------------------------------------
def add(x, y):
    """"""
    logger = logging.getLogger("exampleApp.submodule.add")
    logger.info("added %s and %s to get %s" % (x, y, x+y))
    return x+y

