import os

#use file IO to operate the DBMS, the fuction work as their name.

def appendNewRecord(fileObj, filePath, newLine):
  fileObj = open(filePath, 'a+')
  fileObj.write(newLine)
  fileObj.close()

def readLinesFromFile(filePath):
  fileObj = open(filePath, 'r')
  fileLineList = fileObj.readlines()
  fileObj.close()
  return fileLineList

def findContentAndPrimaryKeyIndex(fileObj, filePath, primaryColumnName):
  fileObj = open(filePath, 'r') if os.path.exists(filePath) else open(filePath, 'a+')
  fileContent = fileObj.read()
  fileObj.close()
  primaryKeyIndex = fileContent.find(primaryColumnName) if fileContent.find('*') < 0 else -999
  return [fileContent, primaryKeyIndex]

def setPrimaryKeyColumn(fileObj, filePath, fileContent, PrimaryKeyIndex):
  fileObj = open(filePath, 'w')
  fileContent = fileContent[:PrimaryKeyIndex] + '*' + fileContent[PrimaryKeyIndex:]
  fileObj.write(fileContent)
  fileObj.close()
