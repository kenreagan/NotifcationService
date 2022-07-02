import logging
import sys
import re
from utils import ColorBaseClass as Color

logger = logging.getLogger(__name__)


logger.setLevel(logging.INFO)


class ColorLogFormatter:
	logFormat = "%(prefix)s %(message)s %(suffix)s"
	
	
	LOG_LEVEL_COLOR = {
		"DEBUG": {'prefix': Color.BOLD_GREEN, 'suffix': ''},
		"INFO": {'prefix': Color.BOLD_GREEN, 'suffix': Color.END},
		"WARNING": {'prefix': Color.BOLD_YELLOW, 'suffix': Color.END},
		"ERROR": {'prefix': Color.BOLD_RED, 'suffix': Color.END},
		"CRITICAL": {'prefix': Color.BOLD_RED, 'suffix': Color.END},
	}
	
	def format(self, logobj):
		if not hasattr(logobj, 'prefix'):
			logobj.prefix = self.LOG_LEVEL_COLOR.get(logobj.levelname.upper()).get('prefix')
			
		if not hasattr(logobj, 'suffix'):
			logobj.suffix = self.LOG_LEVEL_COLOR.get(logobj.levelname.upper()).get('suffix')
			
		formatter = logging.Formatter(self.logFormat)
		return formatter.format(logobj)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(ColorLogFormatter())
logger.addHandler(stream_handler)
