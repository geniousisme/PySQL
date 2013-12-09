import os

def appendNewRecord(fileObj, fileName, newLine):
  fileObj = open(fileName, 'a+')
  fileObj.write(newLine)
  fileObj.close()

def findContentAndPrimaryKeyIndex(fileObj, fileName, primaryColumnName):
  fileObj = open(fileName, 'r')
  fileContent = fileObj.read()
  fileObj.close()
  primaryKeyIndex = fileContent.find(primaryColumnName) if fileContent.find('*') < 0 else -999
  return [fileContent, primaryKeyIndex]

def setPrimaryKeyColumn(fileObj, fileName, fileContent, PrimaryKeyIndex):
  fileObj = open(fileName, 'w')
  fileContent = fileContent[:PrimaryKeyIndex] + '*' + fileContent[PrimaryKeyIndex:]
  fileObj.write(fileContent)
  fileObj.close()






# for path, subdirs, files in os.walk('./DB/dafault'):
#   print path
#   print subdirs
#   print files
#   # for filename in files:
#   #   f = os.path.join(path, filename)
#   #   print str(f) + os.linesep

# from os.path import join, getsize
# for root, dirs, files in os.walk('./DB/dafault/STUDENT'):
#     print root, "consumes",
#     print sum(getsize(join(root, name)) for name in files),
#     print "bytes in", len(files), "non-directory files"

# import os
# for root, dirs, files in os.walk("./DB", topdown=False):
#     print [name for name in files]
      
#     # for name in dirs:
#     #     print name