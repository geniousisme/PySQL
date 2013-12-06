#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# primary key shouldnt set twice times
# default(DB) -> Dir(Relation, ex.STUDENT is a relation, STUDENT.conf is the relation attribute setting config file)
# And STUDENT_DB is the table we set for demo from STUDENT relation, the column attribute follow the conf file
# if user dont use create database, then the DB default setting is in default Dir
# 先求有，再求好，先把現在這版寫完，再來考慮有create database情況的事情
# create 那邊的select DB 一定要再改好一點！！！

import cmd
import getpass
import os
import re
import sys

# the module defined by myself
import DBMS
import File

class PySQL(cmd.Cmd):

  def __init__(self):
    cmd.Cmd.__init__(self)
    self.prompt = 'pysql>>> '
    self.intro  = "****** Chris Hsu own SQL DB for DBMS project by Python ******"
    self.authority = 'user'
  def do_hist(self, args):
    """Print a list of commands that have been entered"""
    print self._hist

  def do_root(self, args):
    self.prompt = 'chrisql>>> '
    self.authority = 'admin'

  def do_login(self, args):
    password = getpass.getpass()
    if  password == '5477cc0411':
      self.prompt = 'chrisql>>> '
      self.authority = 'admin'
      if self.authority == 'admin': print 'you are boss in PySQL!!'    
    elif password == 'user123':
      self.authority = 'user_admin'
      if self.authority == 'user_admin':  print 'hello, visiter, wellcome to PySQL :)'
    else: print '[Error] Wrong Password :( Plz try again.'

  def do_logout(self, args):
    print "logout"
    if self.authority == 'admin' or self.authority == 'user_admin':
      self.prompt = 'pysql>>> '
      self.authority = 'user'

  def do_define(self, args):
    if self.authority == 'admin':
      args = args.split()[0].lower() + ' ' + args.split()[1]
      match = re.search('relation\s*\w*', args)
      if match is None: print '[Syntax Error] try "define --help" or "deifne -h" to get help.'
      else: 
        newTableName = match.group().split()[1]
        if not os.path.exists('./DB/default/' + newTableName): os.mkdir( './DB/default/' + newTableName )
        else: '[Setting Error] The Relation already exists. Plz new another relation.'
        self.tableConfName = './DB/default/'+newTableName+'/'+newTableName+'.conf'
    elif self.authority == 'user_admin':  print '[Error] authority not enough.'
    else: print '[Error] authority not enough.'
  
  def do_DEFINE(self, args):
    self.do_define( args )

  def do_set(self, args):
    # print 'set command!!!'
    if self.authority == 'admin':
      # args = args.split()[0].lower() + ' ' + args.split()[1]
      # print 'args:', args
      match = re.search('attribute\s*\w*', args)
      if match is None:
        if re.search('primary\s*key\s*\w*', args):
          argList = args.split()
          columnName = argList.pop()
          tableConfContent, tablePrimaryKeyIndex = File.findContentAndPrimaryKeyIndex(self.tableConf, self.tableConfName, columnName)
          if tablePrimaryKeyIndex >= 0:
            File.setPrimaryKeyColumn(self.tableConf, self.tableConfName, tableConfContent, tablePrimaryKeyIndex)
            self.primaryKeyExist = True
          else: print '[Setting Error] No such column for primary key setting, try "set --help" or "set -h" to get help.'
        else: print '[Syntax Error] try "set --help" or "set -h" to get help.'
      else:
        dataType = match.group().split()[1]
        if dataType == 'integer':
          argList = args.split()
          columnName = argList.pop(2)
          intRange = ' '.join(argList[-3:]) if len(argList) > 2 else 'range '+ str(-sys.maxint-1) + ' ' + str(sys.maxint)
          File.appendNewRecord(self.tableConf, self.tableConfName, columnName + ': ' + dataType + ' ' + intRange + '\n')  
        elif dataType == 'character':
          argList = args.split()
          columnName = argList.pop()
          charLength = argList.pop() if len(argList) > 2 else '128'
          File.appendNewRecord(self.tableConf, self.tableConfName, columnName + ': ' + dataType + ' ' + charLength + '\n')
        else: print '[Syntax Error] try "set --help" or "set -h" to get help.'

  def do_SET(self, args):
    self.do_set( args )

  def do_create(self, args):
    argList = args.split()
    if argList[0] == 'table' or argList[0] == 'TABLE':
      if self.authority == 'admin': 
        # tmpRelationName = './DB/default/' + argList[1] + '/'
        tmpDBName = './DB/default/'
        tmpTableConfName = tmpDBName + argList[1] + '/' + argList[1] + '.conf'
        if os.path.exists(tmpTableConfName): 
          # self.selectRelation = tmpRelationName
          self.selectDB = tmpDBName
          tmpTableConf = open(tmpTableConfName, 'r')
          if tmpTableConf.read().find('*') >= 0 or self.primaryKeyExist: 
            tmpTableConf.close()
            os.mkdir('./DB/default/' + argList[1] + '/' + argList[2] + '/')
            # newTable = open('./DB/default/' + argList[1] + '/' + argList[2] + '/' + argList[2], 'a')
            # newTable.close()
          else: '[Setting Error] No column was set as primary key, try "set --help" or "set -h" to get help.'
        else: print '[Relation Error] There is no such relation. Plz try "set --help" or "set -h" to get help.'
      else: print '[Error] authority not enough.'
    else: print '[Syntax Error] try "create table --help" or "create table -h" to get help.' 

  def do_CREATE(self, args):
    self.do_create( args )   
  
  def do_insert(self, args):
    argList = args.split()
    if self.authority == 'admin':
      if self.selectDB is not None:
        selectTables2PathDict = DBMS.findAllTables2PathDict(self.selectDB)
        if argList[0] in selectTables2PathDict.keys():
          tableName = argList.pop(0) 
          if 'values' in argList: argList.remove('values')
          if DBMS.MatchTableSetting(selectTables2PathDict[ tableName ], argList):
            print 'yes!!!!!!!!!!!!! Fit all condition!!'
            # DBMS.insertTable(selectTables2PathDict[ tableName ], argList)
          else:
            print 'Nooooooooooooooooooo!!!!!!!!!!!!!'

      else: print '[Insert Error] Choose the DB first. Plz try "use --help" or "use -h" to get help.'
    else: print '[Error] authority not enough.'

  def do_show(self, args): #show all DB/tables
    if args == 'databases' or args == 'DATABASES':
      print "show all databases:"
      for DB in os.listdir('./DB'):
        print DB 

  def do_use(self, args): #assign which DB to use 
    if args in DBMS.findAllDBs(): self.selectDB = './DB/' + args
    else: print '[Use Error] There is no such DB, check again!!'
  
  def do_select(self, args):
    print "select!!"
  
  def do_update(self, args):
    print "update"
  
  def do_delete(self, args):
    print "delete"

  def emptyline(self):    
    """Do nothing on empty input line"""
    pass

  ## Override methods in Cmd object ##
  def preloop(self):
    """Initialization before prompting user for commands.
       Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
    """
    cmd.Cmd.preloop(self)   ## sets up command completion
    self._hist    = []      ## No history yet
    self._locals  = {}      ## Initialize execution namespace for user
    self._globals = {}
    self.cmd   = None
    self.tableConf = None
    # self.selectRelation = None
    self.selectDB = None
    self.primaryKeyExist = False

  def postloop(self):
    """Take care of any unfinished business.
       Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
    """
    cmd.Cmd.postloop(self)   ## Clean up command completion
    print "Exiting PySQL..."

  def precmd(self, line):
    """ This method is called after the line has been input but before
        it has been interpreted. If you want to modifdy the input line
        before execution (for example, variable substitution) do it here.
    """
    print "pre command, line:", line.strip()

    if line.strip() != '':  self.cmd = line.strip().split()[0]
    self._hist += [ line.strip() ]
    # print self._hist
    # print self._hist[len(self._hist)-2]
    if self.cmd == 'exit':
      self.do_exit(line)
    elif self.cmd == 'hist':
      self._hist.pop()
      self.do_hist(line)
    elif len(self._hist) >= 2: 
      if (self._hist[len(self._hist)-2].find('define') >= 0) and (self.cmd != 'set'):
        print "[Error] Plz finish relation setting first."
        self._hist.pop()
        line = ''
    print 'line:', line
    return line

  def postcmd(self, stop, line):
    """If you want to stop the console, return something that evaluates to true.
       If you want to do some post command processing, do it here.
    """
    if stop == 'skip': return stop
    print "post command, line:", line.strip()  
    print "there is stop:", stop
    return stop
  
  
  def do_exit(self, args):
    return True   

if __name__ == '__main__':
    PySQL().cmdloop()