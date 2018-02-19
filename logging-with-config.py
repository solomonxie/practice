import logging
import logging.config
import python_logging_submodule
 
#----------------------------------------------------------------------
def main():
    """
    Based on http://docs.python.org/howto/logging.html#configuring-logging
    """
    logging.config.fileConfig('logging-config.ini')
    logger = logging.getLogger("exampleApp")
 
    logger.info("Program started")
    result = python_logging_submodule.add(7, 8)
    logger.info("Done!")
 
if __name__ == "__main__":
    main()
