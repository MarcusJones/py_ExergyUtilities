#===============================================================================
#--- SETUP Config
#===============================================================================
#from ..config import *
from path_config import *
import unittest

#===============================================================================
#--- SETUP Logging
#===============================================================================
import logging.config
#print(ABSOLUTE_LOGGING_PATH)
#logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
#--- SETUP Add parent module
#===============================================================================
# from os import sys, path
# # Add parent to path
# if __name__ == '__main__' and __package__ is None:
#     this_path = path.dirname(path.dirname(path.abspath(__file__)))
#     sys.path.append(this_path)
#     logging.debug("ADDED TO PATH: ".format(this_path))


#===============================================================================
#--- SETUP Standard modules
#===============================================================================


#===============================================================================
#--- SETUP external modules
#===============================================================================

#===============================================================================
#--- SETUP Custom modules
#===============================================================================
from ..ExergyUtilities.util_inspect import get_self

#===============================================================================
#--- Directories and files
#===============================================================================
#curr_dir = path.dirname(path.abspath(__file__))
#DIR_SAMPLE_IDF = path.abspath(curr_dir + "\..\.." + "\SampleIDFs")
#print(DIR_SAMPLE_IDF)

#===============================================================================
#--- MAIN CODE
#===============================================================================
def run():
    pass


if __name__ == "__main__":
    run()
