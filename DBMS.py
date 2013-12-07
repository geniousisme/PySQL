#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import glob

def findTableConfPath(tableAbsPath):
    return [tableConfPath for tableConfPath in glob.glob(os.path.dirname(tableAbsPath) + "/*.conf")][0]

def findTableAndRecordPath(databasePath, argList):
  recordPath = tablePath = None
  for root, dirs, files in os.walk(databasePath, topdown=False):
    for tableName in dirs: 
      if tableName == argList[0]:
        tablePath = os.path.join(root, tableName)
        if os.path.exists(tablePath + '/' + argList[1]):  
          recordPath = os.path.join(tablePath, argList[1])
  return [tablePath, recordPath]

def findAllTables2PathDict(relationPath):
  tableName2PathDict = {}
  for root, dirs, files in os.walk(relationPath, topdown=False):
    # for fileName in files:
    #   tableName2PathDict[fileName] = os.path.join(root, fileName)
    for dirName in dirs:
      tableName2PathDict[dirName] = os.path.join(root, dirName)
  return tableName2PathDict

def findAllDBs():
  return os.listdir('./DB')

def MatchTableSetting(tableAbsPath, argList):
  tableConfPath = findTableConfPath(tableAbsPath)
  print 'tableConfPath', tableConfPath
  tableConf = open(tableConfPath, 'r')
  
  if os.path.exists(tableAbsPath + '/' + argList[0]):
    print '[Insert Error] Table with same primary key already exists.'
    return False
    
  argIter = argList.__iter__()
  for line in tableConf.readlines():
    lineList = line.split()
    arg = argIter.next()
    print "lineList:", lineList
    print "arg:", arg

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

def insertTable(tableAbsPath, argList):
  # print 'insert'
  newTable = open(tableAbsPath + '/' + argList.pop(0), 'a+')
  for arg in argList:
    newTable.write(arg+'\n')
  newTable.close()

def deleteRecord(recordAbsPath):
  os.remove(recordAbsPath)
  


  # print tableConf.read()
  #先判斷有沒有* => 有則arg不能為null or nil => 再判斷是char or int => arg是否輸入符合char or int => 再判斷範圍 => arg是否宣告在其範圍內
