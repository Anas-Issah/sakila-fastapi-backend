import logging


def logging_setup():

    logging.basicConfig(
        level = logging.INFO,
        format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(message)s - %(method)s - %(path)s - %(statuscode)s"
    )
    )
