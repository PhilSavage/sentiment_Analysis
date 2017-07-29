import csv


def readcsv(csvname):
    with open(csvname,'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)
