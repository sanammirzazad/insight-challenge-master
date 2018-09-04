import sys
import collections
import os


# Define a function to return stock prices and line number for a given hour. line number represents that last line 
# in the  txt file associated to the given hour.
def getPricePerHour(hour, line_number, file):
    stock_price = {}
    while line_number < len(file):
        temp = file[line_number].strip()
        # Skip empty lines in the input file
        if not temp: 
            line_number += 1
            continue
	    
	    # Get the values in each line
        hr, name, price = temp.split('|')
        # Make sure that these values exits and are in the required format.
        if not hr or not name or not price:
        	line_number += 1 
        	continue
        # If hr is the same as hour, add it to the dictionary, otherwise stop.
        if int(hr) == hour:
            stock_price[name] = float(price)
            line_number += 1
            continue
        break 
    return stock_price, line_number

# Define a function to find matching stock in a specified hour and return their count and also their error
# This function also ensures that if no match is found, the error value of 0 is returned.
def getErrorPerHour(actual_prices, predicted_prices):
	error_sum = 0
	count = 0
	for name, price in predicted_prices.items():
		if actual_prices[name]:
			error_sum += abs(price - actual_prices[name])
			count += 1
	return error_sum, count

# Define a function to convert the ave_err to the correct format
def outputFormat(average_error,hour, window_size):
	output = '%d|%d|' % (hour - window_size, hour - 1)
	if average_error == -1:
		output += "NA"
	else:
		output += '{:0.2f}'.format(average_error)
	return output

# Define a function to chack the inputs are valid and return the values.
def checkInoutValidity(INPUT_PATH_WINDOW, INPUT_PATH_ACTUAL, INPUT_PATH_PREDICTED):
	if not os.path.exists(INPUT_PATH_WINDOW) or os.path.getsize(INPUT_PATH_WINDOW) == 0:
		print("The provided window.txt file doesn't exit or is empty.")
		window_size = -1
	else:		
		with open(INPUT_PATH_WINDOW, 'r') as window_file:
			window_size = int(window_file.read().strip())
			if window_size == 0:
				print("The provided window size should be a positive integer.")
				window_size = -1


	if not os.path.exists(INPUT_PATH_ACTUAL) or os.path.getsize(INPUT_PATH_ACTUAL) == 0:
		print("Actual prices file does not exist or is empty")
		actual_data = -1
	else:
		with open(INPUT_PATH_ACTUAL, 'r') as actual_file:
			actual_data = actual_file.readlines()
	if not os.path.exists(INPUT_PATH_PREDICTED) or os.path.getsize(INPUT_PATH_PREDICTED) == 0:
		print("Predicted prices file does not exist or is empty")
		predicted_data = -1
	else:
		with open(INPUT_PATH_PREDICTED, 'r') as preicted_file:
			predicted_data = preicted_file.readlines()
	return window_size, actual_data, predicted_data




def main():
	INPUT_PATH_WINDOW = sys.argv[1]
	INPUT_PATH_ACTUAL = sys.argv[2]
	INPUT_PATH_PREDICTED = sys.argv[3]
	OUTPUT_PATH_COMPARISON = sys.argv[4]


	# Reading the input files and making sure that they exist and nonempty
	window_size, actual_data, predicted_data = checkInoutValidity(INPUT_PATH_WINDOW, INPUT_PATH_ACTUAL, INPUT_PATH_PREDICTED)
	if window_size == -1 or actual_data == -1 or predicted_data == -1:
		print("Error in input data")
		exit()
	# Creating and openning the output file to write the results		
	output_file = open(OUTPUT_PATH_COMPARISON, "w")
	
	# Using a queue to store the errors per hour. The values in in the queue are total error and 
	# counts of the matched stocked prices for each hour
	window = collections.deque()
	actline_No = preline_No = 0
	hour = 1

	while actline_No < len(actual_data):
		actual_prices, actline_No = getPricePerHour(hour, actline_No, actual_data)
		predicted_prices, preline_No = getPricePerHour(hour, preline_No, predicted_data)
		# Consider the case where no prediction is made for an hour. In this case, there is no need to compute the error
		if predicted_prices:
			temp_error_sum, temp_count = getErrorPerHour(actual_prices, predicted_prices)
		else:
			temp_error_sum, temp_count = 0.0, 0
		if len(window) == window_size:
			total_sum = sum(i[0] for i in window)
			total_count = sum(i[1] for i in window)
			average_error = total_sum / float(total_count) if total_count != 0 else -1
			output = outputFormat(average_error,hour, window_size)
			output_file.write(output + "\n")
			window.popleft()

		window.append((temp_error_sum, temp_count))
		hour += 1

	# Write the average error for the last time interval in the output file
	total_sum = sum(i[0] for i in window)
	total_count = sum(i[1] for i in window)
	average_error = total_sum / float(total_count) if total_count != 0 else -1
	output = outputFormat(average_error,hour, window_size)
	output_file.write(output + "\n")


	output_file.close()

if __name__ == '__main__':
    main()




    
	

