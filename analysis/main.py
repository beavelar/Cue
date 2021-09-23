import logging
import pandas as pd
from data.report import report
from watchdog.observers import Observer
from util.rate.rate_util import rate_excel
from filewatcher.filewatcher import filewatcher
from environment.environment import environment
from util.input.input_util import prompt_for_input
from util.directory.directory_util import create_directories

#########################################################################################################

logging.basicConfig(format='%(levelname)s: %(asctime)s - %(name)s.%(funcName)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#########################################################################################################

def main(historical_dir, parsed_file, recap_file):
	parsed_directory = 'Parsed'
	processed_directory = 'Processed'
	unprocessed_directory = 'Unprocessed'
	directories = [f'{historical_dir}\\{parsed_directory}', f'{historical_dir}\\{processed_directory}', f'{historical_dir}\\{unprocessed_directory}']
	create_directories(directories)

	output_historical_df = None
	valid_choices = ['p', 'parse', 'a', 'analyze', 'r', 'rate']
	choice_prompt = 'Parse, analyze or rate historical data? (P/A/R): '
	row_choice_prompt = 'Which row to start on?: '

	graph_parse_prompt = prompt_for_input(choice_prompt, valid_choices)
	output_historical_xlsx = pd.ExcelFile(parsed_file)
	output_historical_df = pd.read_excel(output_historical_xlsx, 'Historical Alerts')

	# Parsing Unusual Whales historical data
	if graph_parse_prompt.lower() == valid_choices[0] or graph_parse_prompt.lower() == valid_choices[1]:
		try:
			logger.info(f'Creating filewatcher for {historical_dir}\\{unprocessed_directory}')
			event_handler = filewatcher(f'{historical_dir}\\{parsed_directory}', f'{historical_dir}\\{processed_directory}')
			observer = Observer()

			logger.info(f'Starting up filewatcher for {historical_dir}\\{unprocessed_directory}')
			observer.schedule(event_handler, path=f'{historical_dir}\\{unprocessed_directory}', recursive=False)
			observer.start()

			while True:
				try:
					pass
				except KeyboardInterrupt:
					observer.stop()
		except Exception as ex:
			logger.critical(f'Failed to create filewatcher for {historical_dir}\\{unprocessed_directory}')
			logger.critical(str(ex))
	# Analyzing historical report and creating call and put report containing the results
	elif graph_parse_prompt.lower() == valid_choices[4] or graph_parse_prompt.lower() == valid_choices[5]:
		logger.info('User selected to analyze parsed data')
		# output_dir = os.path.dirname(os.path.normpath(parsed_file))
		# ouput_call_report = f'{output_dir}\\Call Report.xlsx'
		# ouput_put_report = f'{output_dir}\\Put Report.xlsx'
		call_report = None
		put_report = None
		call_df = output_historical_df.loc[output_historical_df['Option Type'] == 'call']
		put_df = output_historical_df.loc[output_historical_df['Option Type'] == 'put']

		try:
			call_report = report(call_df)
		except TypeError as ex:
			logger.warning('TypeError exception caught creating call report')
			logger.warning(ex)
		try:
			put_report = report(put_df)
		except TypeError as ex:
			logger.warning('TypeError exception caught creating put report')
			logger.warning(ex)
	# Rates Unusual Whales alerts and color codes the cells indicating if BAD, OKAY, GOOD, or BEST
	elif graph_parse_prompt.lower() == valid_choices[6] or graph_parse_prompt.lower() == valid_choices[7]:
		logger.info('User selected to rate parsed data')
		#########################################################################################################
		call_report = None
		put_report = None
		call_df = output_historical_df.loc[output_historical_df['Option Type'] == 'call']
		put_df = output_historical_df.loc[output_historical_df['Option Type'] == 'put']

		try:
			call_report = report(call_df)
		except TypeError as ex:
			logger.warning('TypeError exception caught creating call report')
			logger.warning(ex)
		try:
			put_report = report(put_df)
		except TypeError as ex:
			logger.warning('TypeError exception caught creating put report')
			logger.warning(ex)
		#########################################################################################################
		if call_report != None and put_report != None:
			row_prompt = int(prompt_for_input(row_choice_prompt))
			rate_excel(recap_file, call_report, put_report, row_prompt)
		else:
			report_failed = 'call' if call_report == None else 'put'
			logger.warning(f'Unable to rate data, {report_failed} came back as None')

if __name__ == "__main__":
	env = environment()
	if env.historical_dir != '' and env.parsed_file != '' and env.options_file != '':
		main(env.historical_dir, env.parsed_file, env.options_file)
	else:
		logger.critical(f'Environment variables are not properly defined')
		logger.critical(f'Exiting..')