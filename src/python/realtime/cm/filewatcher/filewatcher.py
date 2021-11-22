import os
import shutil
import logging
from util.parse.parse_util import parse_alerts
from watchdog.events import DirCreatedEvent, FileCreatedEvent, FileSystemEventHandler

#########################################################################################################

logging.basicConfig(format='%(levelname)s: %(asctime)s - %(name)s.%(funcName)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#########################################################################################################

class filewatcher(FileSystemEventHandler):
	'''
	filewatcher
	----------

	This class will handle the file events occuring on the desired directory
	
	Available class variables:

	- parsed_path - Will contain the string path of where the parsed files will be saved to

	- processed_path - Will contain the string path of where the processed files will be moved to
	'''
	def __init__(self, parsed_path: str, processed_path: str) -> None:
		'''
		__init__
		----------

		Creates a filewatcher object which will utilize the FileSystemEventHandler __init__ function
		
		Sets the parsed_path and processed_path variables

		- parsed_path - Will contain the string path of where the parsed files will be saved to

		- processed_path - Will contain the string path of where the processed files will be moved to
		'''
		FileSystemEventHandler.__init__(self)
		self.parsed_path = parsed_path
		self.processed_path = processed_path

	def on_created(self, event: DirCreatedEvent or FileCreatedEvent) -> None:
		'''
		on_created
		----------

		This function will handle DirCreatedEvents or FileCreatedEvents
		
		We don't expect DirCreatedEvents so we will assume all events are FileCreatedEvents
		
		The file from the event will be parsed and copied over to the processed directory
		
		The parsed result will be placed in the parsed directory
		'''
		logger.info(f'New file detected in: {event.src_path}')
		file_name = os.path.basename(event.src_path)
		parse_alerts(event.src_path, f'{self.parsed_path}\\{file_name}')
		shutil.move(event.src_path, f'{self.processed_path}\\{file_name}')
		logger.info(f'Moved {event.src_path} to {self.processed_path}\\{file_name}')