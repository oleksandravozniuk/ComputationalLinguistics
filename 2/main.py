
import collections
import csv
import re
import math 
import matplotlib.pyplot as plt


def getFromFile(filename):
    resultArray = []
    rows = [] 
    with open(filename, encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile) 
        for row in csvreader: 
            rows.append(row)     
    for row in rows:  
        result =  ''.join(row) 
        x = result.split(";")
        resultArray.append(x)
    return resultArray

def clearStr(str, isMinWord):
    newStr = re.sub(r'[^\w\s]','', str).lower();
    if isMinWord:
        newStr = re.sub(r'\b\w{1,3}\b', '', newStr)
    return newStr

def clearArray(array, isMinWord):
    resultArray = []
    for words in array:
        str = clearStr(words[1], isMinWord);
        row = [words[0], str, words[2]]
        resultArray.append(row)
    return resultArray


def getFrequencyByClassName(array, className):
    count = 0
    for words in array:
        index = words[2].find(className)
        if(index != -1):
            count = count + 1
    return count

def getArrayByClassName(array, className):
    resultArray = []
    for words in array:
        index = words[2].find(className)
        if(index != -1):
            resultArray.append(words)
    return resultArray

def getTotalWords(array):
    total = 0
    for words in array:
        total = total + len(words[1].split())
    return total

def getCountFromArrays(array, array2):

    dict = {}

    for words in array:
        for key in words[1].split():
            if key in dict:
                dict[key] = dict[key] + 1
            else:
                dict[key] = 1

    for words in array2:
        for key in words[1].split():
            if key in dict:
                dict[key] = dict[key] + 1
            else:
                dict[key] = 1

    return len(dict)

def getDictWords(array):
    dict = {}
    for words in array:
        for key in words[1].split():
            if key in dict:
                dict[key] = dict[key] + 1
            else:
                dict[key] = 1
    return dict


def getCoff(ddc, row, dict, k, total):
    splitedWords = row[1].split()
    value = 0
    for word in splitedWords:
        if word in dict:
            value = value + math.log( (dict[word] + 1) / (k + total) )
        else:
            value = value + math.log( (0 + 1) / (k + total) )
    return ddc + value

def printDebug(isDebug, message):
    if isDebug:
        print(message)

def modeling(filename, isDebug, testFileName):

    isMinLength = False

    print(filename)

    firstClass = '0'
    secondClass = '1'
    
    array = getFromFile(filename)
    print(array)

    firstFreq = getFrequencyByClassName(array, firstClass)
    secondFreq = getFrequencyByClassName(array, secondClass)

    firstArray = getArrayByClassName(array, firstClass)
    secondArray = getArrayByClassName(array, secondClass)

    firstArrayClear = clearArray(firstArray, isMinLength)
    secondArrayClear = clearArray(secondArray, isMinLength)
    
    k = getCountFromArrays(firstArrayClear, secondArrayClear)

    firstTotal = getTotalWords(firstArrayClear)
    secondTotal = getTotalWords(secondArrayClear)

    firstDict = getDictWords(firstArrayClear)
    secondDict = getDictWords(secondArrayClear)


    if(isDebug):
        print('filename: ' + filename)

        print('class ' + firstClass)
        print('frequency: ' + str(firstFreq))
        print('words count: ' + str(firstTotal))

        print('class ' + secondClass)
        print('frequency: ' + str(secondFreq))
        print('words count: ' + str(secondTotal))
        print('\n')


    FFirstLog = math.log(firstFreq / (firstFreq + secondFreq))
    SFirstLog = math.log(secondFreq / (firstFreq + secondFreq))

    testArray = getFromFile(testFileName)
    testArrayClear = clearArray(testArray, isMinLength)
    
    goodResult = 0;
    allResult = len(testArrayClear)
    for row in testArrayClear:
        printDebug(isDebug, row)
        coffFirst = getCoff(FFirstLog, row, firstDict, k, firstTotal)
        coffSecond = getCoff(SFirstLog, row, secondDict, k, secondTotal)
        message = firstClass + ': ' + str(coffFirst) + '  ' + secondClass + ': ' + str(coffSecond)
        printDebug(isDebug, message)
        if(coffFirst > coffSecond):
            printDebug(isDebug, firstClass)
            if('клас = 0' == row[2]):
                goodResult += 1
                printDebug(isDebug, 'correct')
            else:
                printDebug(isDebug, 'uncorrect')
        else:
            printDebug(isDebug, secondClass)
            if('клас = 1' == row[2]):
                goodResult += 1
                printDebug(isDebug, 'correct')
            else:
                printDebug(isDebug, 'uncorrect')
                
    print('test jokes count: ' + str(allResult))
    print('correct results: ' + str(goodResult))
    print('uncorrect results: ' + str(allResult - goodResult))

def defaultHist(res: dict):
      plt.bar(res.keys(), res.values(), color='g', label = "Real distribution")
      plt.show()

def buildHistograms(filename, isMinLength):

    print(filename)

    firstClass = '0'
    secondClass = '1'
    
    array = getFromFile(filename)

    firstArray = getArrayByClassName(array, firstClass)
    secondArray = getArrayByClassName(array, secondClass)

    firstArrayClear = clearArray(firstArray, isMinLength)
    secondArrayClear = clearArray(secondArray, isMinLength)

    firstDict = getDictWords(firstArrayClear)
    secondDict = getDictWords(secondArrayClear)

    od = collections.OrderedDict(sorted(firstDict.items(), key=lambda x: x[1], reverse=True)[:10])
    defaultHist(od)

    od = collections.OrderedDict(sorted(secondDict.items(), key=lambda x: x[1], reverse=True)[:10])
    defaultHist(od)

def firstPart(debug):

    fileNameTest = 'test.csv'
    modeling('test_10.csv', debug, fileNameTest)
    modeling('test_20.csv', debug, fileNameTest)
    modeling('test_30.csv', debug, fileNameTest)


def main():

    debug = False
    firstPart(debug)

    #buildHistograms('dataset.csv', False)
    #buildHistograms('dataset.csv', True)

    
main()