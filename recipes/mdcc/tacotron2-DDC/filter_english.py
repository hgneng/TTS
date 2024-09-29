#!/usr/bin/env python3
import csv
import subprocess

def filter(sourceFile, targetFile):
    file = open(targetFile, mode='w', newline='')
    # Create a writer object
    writer = csv.writer(file)

    # Open the CSV file
    with open(sourceFile, mode='r') as file:
        # Create a CSV reader object
        # ./audio/447_1709011939_16988_371.88_376.92.wav,./transcription/447_1709011939_16988_371.88_376.92.txt,male,5.0400000000000205
        csv_reader = csv.reader(file)

        # Read the file line by line
        for row in csv_reader:
            result = subprocess.run(['grep', '-P', '[\\x{4E00}-\\x{9FFF}]', 'mdcc-dataset/' + row[1]], capture_output=True, text=True)
            #result = subprocess.run(['echo', '"[\\x{4E00}-\\x{9FFF}]"'], capture_output=True, text=True)
            if (result.stdout):
                #print("Chinese:" + result.stdout)
                writer.writerow(row)
            else:
                result = subprocess.run(['cat', 'mdcc-dataset/' + row[1]], capture_output=True, text=True)
                print("English:" + result.stdout)


filter('mdcc-dataset/cnt_asr_train_metadata.csv', 'train.csv')
#filter('mdcc-dataset/cnt_asr_valid_metadata.csv', 'valid.csv')

