"""This programme will take the path of the directory where all the required file is present or should be present and the second argument is the target file name i.e Combined.csv
If there is no file(s) present in the directory, then it will create the file - Combined.csv with header('Source IP' and 'Environment' first and as the files get dropped it will pickup those and
make the entries in the Combined.csv. This programme will keep on running unless it is killed or stopped."""

import os, time, csv, datetime

class Risk_Analytics:

    def __init__(self, path, file_name):
        self.path = path
        os.chdir(path)
        print(os.getcwd())
        self.file_name = file_name

    def file_Check(self):

        self.newFileCnt = 0
        self.originalFileCount = 0
        while True:
            if (self.file_name in os.listdir(self.path)):
                self.newFileCnt = len(os.listdir(self.path))
                print(f"Number of Original File Present is : {self.newFileCnt}")
                originalListFile = os.listdir(self.path)
                print(f"originalListFile : {originalListFile}")
                time.sleep(10)
                print(f"After sleep of 10 seconds")
                self.newFileCnt = len(os.listdir(self.path))
                print(f"New File Count : {self.newFileCnt}")
                if self.newFileCnt > self.originalFileCount:
                    newFileList = os.listdir(self.path)
                    fileToBeProcessed = list(set(newFileList) - set(originalListFile))
                    if not fileToBeProcessed:
                        continue
                    else:
                        print(f"fileToBeProcessed : {fileToBeProcessed}")
                        fileToBeProcessedWithoutExt = fileToBeProcessed[0].split('.')[0]
                        print(f"fileToBeProcessedWithoutExt :{fileToBeProcessedWithoutExt}")

                        for f in fileToBeProcessed:
                            with open(f,'r') as rf:
                                csv_reader = csv.reader(rf)
                                next(csv_reader)
                                for line in csv_reader:
                                    with open(self.file_name, 'a',newline='') as wf:
                                        csv_writer = csv.writer(wf,)
                                        print(f"Printing the value of the csv entries : [{line[0]},{fileToBeProcessedWithoutExt}]")
                                        csv_writer.writerow([line[0],fileToBeProcessedWithoutExt])

                        #Remove duplicate entries from the Combined.csv
                        with open(self.file_name, 'r', newline='') as in_file, open('new_'+self.file_name, 'w', newline='') as out_file:
                            reader = csv.reader(in_file)
                            writer = csv.writer(out_file)
                            seen = set()  # set for fast O(1) amortized lookup
                            for row in reader:
                                if row:
                                    row = tuple(row)
                                    if row in seen: continue  # skip duplicate
                                    seen.add(row)
                                    writer.writerow(row)

                else:
                    print(f"There is no new files to be processed...")
            else:
                print(f"There is no files present in the Given Path and hence Generating the Empty File with the name :{self.file_name}")
                with open(self.file_name,'w') as tf:
                    writer = csv.writer(tf)
                    header = ['Source IP','Environment']
                    writer.writerow(header)
                    print(f"File {self.file_name} with header only created Successfully")
                    self.originalFileCount = len(os.listdir(self.path))
                    print(f"Number of File present in the else part is :{self.originalFileCount}")

if __name__ == '__main__':
    #The path value can be changed in the below line.
    path = r"C:\Users\91998\Documents\Pramod\Official\TCS\Engineering Test Risk Analytics\Testing_Engineering"
    target_file = 'Combined.csv'
    risk = Risk_Analytics(path, target_file)
    risk.file_Check()