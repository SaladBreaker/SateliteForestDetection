import os
import logging
from .exceptions import FileNotFoundException


class BaseObject(object):
    def __init__(self) -> None:
        super().__init__()
        self.__configure_logging()

        self.log = logging.getLogger(str(self.__class__.__name__))

    def __configure_logging(self):
        """configure logging module"""
        logging.basicConfig(
            # filename=CONFIG["LOGGING_FILE"],
            level=logging.INFO,
            format="%(asctime)s: %(levelname)7s: [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def create_dir(self, path):
        try:
            os.mkdir(path)
        except OSError:
            self.log.error("Creation of the directory %s failed" % path)
        else:
            self.log.debug("Successfully created the directory %s " % path)

    def check_if_file_exists(self, path):
        try:
            os.path.isfile(path)
        except Exception as e:
            self.log.error(f"Could not fild file {path}. Error: {e}")
            raise FileNotFoundException()
