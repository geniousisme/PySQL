def appendNewRecord(fileObj, fileName, newLine):
  fileObj = open(fileName, 'a')
  fileObj.write(newLine)
  fileObj.close()

def findContentAndPrimaryKeyIndex(fileObj, fileName, primaryColumnName):
  fileObj = open(fileName, 'r')
  fileContent = fileObj.read()
  fileObj.close()
  primaryKeyIndex = fileContent.find(primaryColumnName)
  return [fileContent, primaryKeyIndex]

def setPrimaryKeyColumn(fileObj, fileName, fileContent, PrimaryKeyIndex):
  fileObj = open(fileName, 'w')
  fileContent = fileContent[:PrimaryKeyIndex] + '*' + fileContent[PrimaryKeyIndex:]
  fileObj.write(fileContent)
  fileObj.close()