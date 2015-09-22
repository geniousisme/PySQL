#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys
import glob
import File
#column string to array
def columnStr2List(columnStr):
  return columnStr.replace(" ","").split(',')
#get the selected column name
def getColumnName(tableConfLine):
  return tableConfLine.split()[0].replace(':','')
#sort the dict(hash) by value
def sortedByValueDictFormatter(Dict):
  tupleList = sorted(Dict.items(), key=lambda x: x[1])
  return [ tuple[0] for tuple in tupleList ]
#find the table conf path
def findTableConfPath(tableAbsPath):
    return [tableConfPath for tableConfPath in glob.glob(os.path.dirname(tableAbsPath) + "/*.conf")][0]
#find primary key column from table conf file
def findPrimaryKeyColumnIndex(tableConfPath):
  primaryKeyIndex = None
  tableConf = open(tableConfPath, 'r')
  for index, line in enumerate(tableConf.readlines()):
    if line.find('*') >= 0: primaryKeyIndex = index 
  tableConf.close()
  return primaryKeyIndex
#check the permission is useradmin or not
def isUser(password):
  userAdminFile = open('./dbConfig/useradmin', 'r')
  userPasswordList = userAdminFile.read().splitlines()
  userAdminFile.close()
  if password in userPasswordList:
    return True
  else:
    return False
#check the permission is sysadmin or not
def isAdmin(password):
  sysAdminFile = open('./dbConfig/sysadmin', 'r')
  sysPasswordList = sysAdminFile.read().splitlines()
  sysAdminFile.close()
  if password in sysPasswordList:
    return True
  else:
    return False

#get all column name and their index line from table conf file
def getAllColumn2IndexDict(tableAbsPath):
  tableConf = open(findTableConfPath(tableAbsPath), 'r')
  column2IndexDict = {}
  lineIndex = 0
  for line in tableConf.readlines():
    if line.find('*') >= 0: continue
    else: 
      column2IndexDict[getColumnName(line)] = lineIndex  
      lineIndex += 1
  tableConf.close()
  return column2IndexDict
#find selected table and record path
def findTableAndRecordPath(databasePath, argList):
  recordPath = tablePath = None
  tableIndex = 0 if 'from' not in argList else argList.index('from') + 1 
  for root, dirs, files in os.walk(databasePath, topdown=False):
    for tableName in dirs: 
      if tableName == argList[tableIndex]:
        tablePath = os.path.join(root, tableName)
        tableConfPath = findTableConfPath(tablePath)
        primaryKeyIndex = findPrimaryKeyColumnIndex(tableConfPath)
        if len(argList) > 2:
          if os.path.exists(tablePath + '/' + argList[primaryKeyIndex+1]):   
            recordPath = os.path.join(tablePath, argList[primaryKeyIndex+1])
  argList.pop(tableIndex)
  if 'from' in argList: argList.remove('from')
  return [tablePath, recordPath]


def findAllDBs():
  return os.listdir('./DB')
#judge the input command line matches the rule we define or not
def MatchTableSetting(tableAbsPath, argList, sqlType):
  argList.pop
  tableConfPath = findTableConfPath(tableAbsPath)
  # print 'tableConfPath', tableConfPath
  tableConf = open(tableConfPath, 'r')
  
  if os.path.exists(tableAbsPath + '/' + argList[0]) and sqlType == 'insert':
    print '[Insert Error] Table with same primary key already exists.'
    return False
    
  argIter = argList.__iter__()
  for line in tableConf.readlines():
    lineList = line.split()
    arg = argIter.next()
    # print "lineList:", lineList
    # print "arg:", arg

    if lineList[0].find('*') >= 0:
      if arg == 'null' or arg == 'nil':  
        print '[Insert Error] Primary Key Column must not be null or nil.'
        return False

    if lineList[1]=='character':
      if not type(arg).__name__=='str':
        print '[Insert Error] Column must fit char type.'
        return False
      else: #type(arg).__name__=='str':
        if not ( len(arg) <= int(lineList[-1]) ):
          print '[Insert Error] Column must fit in the char lenght range.'
          return False
    
    if lineList[1]=='integer':
      if not arg.isdigit():
        print '[Insert Error] Column must fit int type.'
        return False
      else: #if arg.isdigit()
        if not ( int(lineList[-2]) <= int(arg) <= int(lineList[-1]) ):
          print '[Insert Error] Column must fit in the int range.'  
          return False        

  tableConf.close()
  return True
#setup relation file
def setRelation(matchObj, argList, tableConfPath, tableConfContent):
  dataType = matchObj.group().split()[1]
  if dataType != 'integer' and dataType != 'character':
    print '[Syntax Error] try "set --help" or "set -h" to get help.'
    return None
  elif dataType == 'integer':
    columnName = argList.pop(2)
    range = ' '.join(argList[-3:]) if len(argList) > 2 else 'range '+ str(-sys.maxint-1) + ' ' + str(sys.maxint)
  elif dataType == 'character':
    columnName = argList.pop()
    range =  argList.pop() if len(argList) > 2 else '128'
  if tableConfContent.find(columnName) < 0: 
    File.appendNewRecord(None, tableConfPath, columnName + ': ' + dataType + ' ' + range + '\n') 
  else:
    print '[Setting Error] The column name already exist. Plz try "set --help" or "set -h" to get help.'

#insert record into table 
def insertTable(tableAbsPath, argList):
  tableConfPath = findTableConfPath(tableAbsPath)
  primaryKeyIndex = findPrimaryKeyColumnIndex(tableConfPath)
  newTable = open(tableAbsPath + '/' + argList.pop(primaryKeyIndex), 'a+')
  for arg in argList:
    newTable.write(arg+'\n')
  newTable.close()

def deleteRecord(recordAbsPath):
  os.remove(recordAbsPath)

def updateRecord(tableAbsPath, recordAbsPath, argList): 
  tableConfPath = findTableConfPath(tableAbsPath)
  primaryKeyIndex = findPrimaryKeyColumnIndex(tableConfPath)
  argList.pop(primaryKeyIndex)
  newRecord = open(recordAbsPath, 'w')
  for arg in argList:
    newRecord.write(arg+'\n')
  newRecord.close()
#judge the condition for select-where part
def whereConditionsCheck(recordAbsPath, argList, Column2IndexDict):
  whereIndex = argList.index('where')
  columnName, whereCondition, whereLimit = argList[whereIndex+1:]
  if columnName not in Column2IndexDict.keys(): 
    print '[Select Error] Column does not exist. Plz try select --help or select -h for help'
    return False
  recordFileObj = open(recordAbsPath, 'r')
  recordLineList = recordFileObj.readlines()
  recordFileObj.close()
  if whereCondition == '>':
    if int(recordLineList[Column2IndexDict[columnName]]) >  int(whereLimit): return True
    else: return False
  elif whereCondition == '=':
    if int(recordLineList[Column2IndexDict[columnName]]) == int(whereLimit): return True
    else: return False
  elif whereCondition == '<':
    if int(recordLineList[Column2IndexDict[columnName]]) <  int(whereLimit): return True
    else: return False
  elif whereCondition == '<=':
    if int(recordLineList[Column2IndexDict[columnName]]) <= int(whereLimit): return True
    else: return False
  elif whereCondition == '>=':
    if int(recordLineList[Column2IndexDict[columnName]]) >= int(whereLimit): return True
    else: return False 
  else: 
    print '[Select Error] Condition can not be recognized. Plz try select --help or select -h for help'
    return False

#先找table => 找tableConf => 讀出每一個column(除了primaryKeyColumn)所在row的index(primarykey之後的column記得原來的index數-1) => 進入所有record中判斷條件 => 符合條件就print出
def selectRecords(tableAbsPath, argList):
  Column2IndexDict = getAllColumn2IndexDict(tableAbsPath)
  selectedColumnList = columnStr2List( argList[0] ) if argList[0]!='*' else sortedByValueDictFormatter(Column2IndexDict)
  print '--------------------------------'
  for root, dirs, files in os.walk(tableAbsPath, topdown=False):
    for recordFile in files:
      recordAbsPath = os.path.join(root, recordFile)
      if whereConditionsCheck(recordAbsPath, argList, Column2IndexDict):
        print os.path.basename(recordAbsPath)
        record = open(recordAbsPath, 'r')
        recordLineList = record.readlines()
        record.close()
        for columnName in selectedColumnList:
          print columnName, recordLineList[Column2IndexDict[columnName]]
        print '--------------------------------'
  



  # print tableConf.read()
  #先判斷有沒有* => 有則arg不能為null or nil => 再判斷是char or int => arg是否輸入符合char or int => 再判斷範圍 => arg是否宣告在其範圍內
