import logging
from os import environ
from datetime import datetime
from itertools import groupby


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)

FILE_PATH = environ.get('SCRIPT_FILE_PATH', 'mbox.txt')
OUTPUT_FORMAT = environ.get('SCRIPT_OUTPUT_FORMAT', '%(from)s (%(date)s): %(subject)s')
DATE_FORMAT = environ.get('SCRIPT_DATE_FORMAT', 'Date: %a, %d %b %Y %H:%M:%S %z')


def parse(file_path):
	res = []
	with open(file_path, 'r') as f:
		mail = {}
		for line in f:
			if line.startswith('Date:'):
				try:
					# Date: Sat, 5 Jan 2008 09:12:18 -0500
					date = datetime.strptime(line.strip(), DATE_FORMAT)
				except ValueError:
					continue  # for skipping next logic
				# 5 Jan 2008 09:12:18 -0500
				mail = {}
				mail['date'] = date
			elif line.startswith('From:'):
				# From: stephen.marquard@uct.ac.za
				mail['from'] = line.split(' ')[1].strip()
			elif line.startswith('Subject:'):
				# Subject: [sakai] svn commit: r39772 - conten...
				mail['subject'] = ' '.join(line.split(' ')[1:]).strip()
				res.append(mail)
		_logger.info('File parsed...')
		_logger.debug(mail)
	return res


def process_data(data):
	res = []
	data = list(sorted(data, key=lambda r: r['from']))
	for key, row in groupby(data, lambda r: r['from']):
		res.append((key, len(list(row))))
	return res

def main():
	_logger.info('Script started...')
	data = parse(FILE_PATH)

	_logger.info('Result:')
	for item in data:
		_logger.info('\t' + OUTPUT_FORMAT % item)

	_logger.info('Statistics:')
	for key, count in process_data(data):
		_logger.info('\t' + '%s: %s' % (key, count))

	_logger.info('Script end.')


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		_logger.critical('Force down...')
