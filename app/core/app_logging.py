import logging


class HTTPContextFilter(logging.Filter):

    def filter(self, record):
        if not hasattr(record, "method"):
            record.method = "-"
        if not hasattr(record, "path"):
            record.path = "-"
        if not hasattr(record, "statuscode"):
            record.statuscode = "-"
        return True

def logging_setup():

    logging.basicConfig(
        level = logging.INFO,
        force=True,
        format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(message)s"
    )
    )
