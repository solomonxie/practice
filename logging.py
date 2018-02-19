#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging_submodule

#----------------------------------------------------------------------
def main():
    """
    The main entry point of the application
    """
    logger = logging.getLogger('exampleApp')
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler("log.log")

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)

    logger.info("Program started")
    result = logging_submodule.add(7, 8)
    logger.info("Done!")

if __name__ == "__main__":
    main()
