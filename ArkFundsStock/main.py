
''' 
Initialization
CMD: pip3 install selenium

Exececution
CMD: python3 main.py
'''

# Importing Important Imports
from selenium import webdriver
import csv

def remove(text, item):
	''' Helper Function for Cleaning Data '''
	return text.replace(item, '')

def getStock(link):

	''' 
	Main Function to Retrieve Data 
	Link (str): 'arkk', 'arkq' or 'arkw'
	Returns: Data for TESLA INC from latest update
	'''

	# Initializing Driver for Web Calls
	driverPath = r'C:\\Users\\taaha\\Desktop\\chromedriver'
	chromeOptions = webdriver.chrome.options.Options()
	chromeOptions.add_argument('--headless')

	# Attempting to establish a connection (Max Tries: 5)
	for attempt in range(5):
		try:
			driver = webdriver.Chrome(
				executable_path = driverPath,
				options = chromeOptions
			)
			break
		except: 
			print('\nERROR GENERATING DRIVER. RETRYING...')
		
	# Running GET request for page
	driver.get(f'https://ark-funds.com/{link}#holdings')

	# Waiting for Top Ten Table to load
	table = driver.find_element_by_id('topten')
	while table.text == '':	# Not Loaded Yet
		table = driver.find_element_by_id('topten')

	# Getting Table
	text = str(table.text)
	text = remove(text, 'View All Holdings')
	text = remove(text, 'As of ')
	text = remove(text, ',')

	# CLEANING DATA --------

	# Separating
	data = text.split()
	data = data[:17]

	# Slicing for TSLA
	date = data[0]
	labels = data[1:9]
	values = data[10:]

	# Cleaning False Splits
	labels.remove('Held')
	labels[5] = 'Shares Held'

	labels.remove('Price')
	labels[3] = 'Market Price'

	labels[-1] = 'Market Value'

	values.remove('INC')
	values[1] = 'TESLA INC'

	# Returning Data
	return [link] + [date] + values

def writeToFile(data):

	''' Appending Given Data to TSLA_DATA.csv file '''

	file = open('TSLA_DATA.csv', 'a')
	file.write('\n')
	for line in data:
		value = ','.join(line)
		
		# Writing Data
		file.write('\n' + value)
	file.close()

def getValues(date):

	''' Searching Database for given data '''

	with open('TSLA_DATA.csv') as file:
		reader = csv.DictReader(file)

		data = []
		for row in reader:
			
			# Checking for Date
			if row['Date'] == date:
				data.append(row + '\n')

			# Exiting
			if len(data) == 3:
				break

		print(data)

		# No Data
		if len(data) == 0:		
			print('No Data for Specified Date Found')

def main():

	# Getting Table Values
	arkk = getStock('arkk')
	arkw = getStock('arkw')
	arkq = getStock('arkq')

	# Compiling and Writing to File
	data = [arkk, arkw, arkq]
	writeToFile(data)

# Executing Program
if __name__ == '__main__':
	main()
