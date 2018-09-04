@Author Sanam Mirzazad

## Run:
The following command can be used to run the code: ./run.sh

## Test:
The code is tested for different use cases. For instance, different window sizes, 0 empty sizes, error with input files, such as empty or non-existence. 

## Approach:
1) The code read the input files.
2) For each hour, the actual and predicted prices are stored, and the error values are found for matching stock prices. 
3) For faster processing, a sliding window is defined as a deque. The values are stored in the deque, and once the values for a new hour is computed, the first value in the queue is popped, and the new one is being appended.
4) The average error is computed by averaging over the values in the window and written to the output once each average error is computed.

# prediction-validation-Sanam
