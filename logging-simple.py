#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging_submodule

#----------------------------------------------------------------------
def main():
    """
    The main entry point of the application
    """
    log = define_logging('exampleeee', 'log.log')

    log.info("Program started")
    result = logging_submodule.add(7, 8)
    log.info("Done!")


def define_logging(name, path):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create the logging file handler
    fh = logging.FileHandler(path)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)

    return logger

if __name__ == "__main__":
    main()
