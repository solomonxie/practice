import logging
import logging_submodule 


def main():
    
    log = define_logging('exampleClass', 'log.log')
    log.info('initttttt from main()')
    result = logging_submodule.add(7, 8)
    log.warn('warning from main()')


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
