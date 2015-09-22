#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# primary key shouldnt set twice times
# default(DB) -> Dir(Relation, ex.STUDENT is a relation, STUDENT.conf is the relation attribute setting config file)
# And STUDENT_DB is the table we set for demo from STUDENT relation, the column attribute follow the conf file
# if user dont use create database, then the DB default setting is in default Dir

import cmd
import getpass
import os
import re
import sys

# the module defined by myself
import DBMS
import File

#change the command line to array
def str2List(str):
  fromIndex = str.find('from')
  if fromIndex >= 0:  str = str[:fromIndex].replace(' ','') + ' ' + str[fromIndex:]
  return str.split()

#main function of PySQL
class PySQL(cmd.Cmd):
  
  def __init__(self):
    cmd.Cmd.__init__(self)
    self.prompt = 'pysql>>> '
    self.intro  = "****** Chris Hsu own SQL DB for DBMS project by Python ******"
    self.authority = 'user'

#see the command line u have typed in
  def do_hist(self, args):
    """Print a list of commands that have been entered"""
    print self._hist
#shortcut to enter admin
  def do_root(self, args):
    self.prompt = 'chrisql>>> '
    self.authority = 'admin'
#sign up for PySQL
  def do_register(self, args):
    password   = getpass.getpass(prompt='type in your password:')
    repassword = getpass.getpass(prompt='confirm your password:')
    if password == repassword:
      File.appendNewRecord(None, './dbConfig/useradmin', password+'\n')
      print 'Register to PySQL suceessfully!!'
    else:
      print '[Error] the password you tyoe in are not the same :( Plz try again.'

  def do_login(self, args):
    password = getpass.getpass()
    if DBMS.isAdmin(password):
      self.prompt = 'chrisql>>> '
      self.authority = 'admin'
      print 'you are boss in PySQL!!'    
    elif DBMS.isUser(password):
      self.authority = 'user_admin'
      print 'hello, visiter, wellcome to PySQL :)'
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
        else: print '[Setting Error] The Relation already exists. Plz new another relation.'
        self.tableConfPath = './DB/default/'+newTableName+'/'+newTableName+'.conf'
    elif self.authority == 'user_admin':  print '[Error] authority not enough.'
    else: 
      print '[Error] authority not enough.'
  
  def do_DEFINE(self, args):
    self.do_define( args )
#primary key & column name judge
  def do_set(self, args):
    if self.authority == 'admin':
      match = re.search('attribute\s*\w*', args)
      if match is None:
        if re.search('primary\s*key\s*\w*', args):
          argList = str2List(args)
          columnName = argList.pop()
          tableConfContent, tablePrimaryKeyIndex = File.findContentAndPrimaryKeyIndex(self.tableConf, self.tableConfPath, columnName)
          if tablePrimaryKeyIndex >= 0:
            File.setPrimaryKeyColumn(self.tableConf, self.tableConfPath, tableConfContent, tablePrimaryKeyIndex)
            self.primaryKeyExist = True
          elif tablePrimaryKeyIndex == -999:
            print '[Setting Error] Primary key already set.'
          else:
            print '[Setting Error] No such column for primary key setting, try "set --help" or "set -h" to get help.'
        else: print '[Syntax Error] try "set --help" or "set -h" to get help.'
      else:
        tableConfContent = File.findContentAndPrimaryKeyIndex(None, self.tableConfPath, '')[0]
        DBMS.setRelation(match, str2List(args), self.tableConfPath, tableConfContent)
    else: 
      print '[Error] authority not enough.'

  def do_SET(self, args):
    self.do_set( args )
#create the table folder to save record
  def do_create(self, args):
    argList = args.split()
    if argList[0] == 'table' or argList[0] == 'TABLE':
      if self.authority == 'admin': 
        tmpDBName = './DB/default/'
        tmpTableConfName = tmpDBName + argList[1] + '/' + argList[1] + '.conf'
        if os.path.exists(tmpTableConfName): 
          self.selectDB = tmpDBName
          tmpTableConf = open(tmpTableConfName, 'r')
          if tmpTableConf.read().find('*') >= 0 or self.primaryKeyExist: 
            tmpTableConf.close()
            os.mkdir('./DB/default/' + argList[1] + '/' + argList[2] + '/')
          else: '[Setting Error] No column was set as primary key, try "set --help" or "set -h" to get help.'
        else: print '[Relation Error] There is no such relation. Plz try "set --help" or "set -h" to get help.'
      else: print '[Error] authority not enough.'
    else: print '[Syntax Error] try "create table --help" or "create table -h" to get help.' 

  def do_CREATE(self, args):
    self.do_create( args )   
#insert record for table  
  def do_insert(self, args):
    argList = args.split()
    if self.authority == 'admin':
      if self.selectDB is not None:
        selectTablePath, selectRecordPath = DBMS.findTableAndRecordPath(self.selectDB ,argList)
        if selectTablePath is not None:
          if 'values' in argList: argList.remove('values')
          if DBMS.MatchTableSetting(selectTablePath, argList, 'insert'):
            DBMS.insertTable(selectTablePath, argList)
      else: print '[Insert Error] Choose the DB first. Plz try "use --help" or "use -h" to get help.'
    else: print '[Error] authority not enough.'

  def do_INSERT(self, args):
    self.do_insert( args )
#can show columns/DBs/tables
  def do_show(self, args): #show all DB/tables
    argList = str2List(args)
    if args == 'databases' or args == 'DATABASES':
      print "###################"
      for DB in os.listdir('./DB'):
        print DB 
      print "###################"
    elif args == 'tables' or args == 'TABLES':
      print "###################"
      for table in os.listdir('./DB/default'):
        print table 
      print "###################"
    elif argList[1] == 'columns' or argList[1] == 'COLUMNS':
      print "###################"
      if self.selectDB is not None:
        selectTablePath = DBMS.findTableAndRecordPath(self.selectDB, argList)[0]
        Column2IndexDict = DBMS.getAllColumn2IndexDict(selectTablePath)
        for column in Column2IndexDict.keys():
          print column
      print "###################"
  
  def do_SHOW(self, args):
    self.do_show( args )
#choose which databases u want
  def do_use(self, args): #assign which DB to use 
    
    if args in DBMS.findAllDBs(): self.selectDB = './DB/' + args + '/'
    else: print '[Use Error] There is no such DB, check again!!'

  def do_USE(self, args):
    self.do_use( args )
#following detail, plz see the DBMS.py file
  def do_select(self, args):
    argList = str2List(args)
    if self.selectDB is not None:
      selectTablePath = DBMS.findTableAndRecordPath(self.selectDB ,argList)[0]
      if selectTablePath is not None:
        DBMS.selectRecords(selectTablePath, argList)
      else: print '[Select Error] The table does not exist. Plz try "use --help" or "use -h" to get help.'
    else: print '[Select Error] Choose the DB first. Plz try "use --help" or "use -h" to get help.'
  
  def do_SELECT(self, args):
    self.do_select( args )
  
  def do_update(self, args):
    argList = str2List(args)
    if self.authority == 'admin':
      if self.selectDB is not None:
        selectTablePath, selectRecordPath = DBMS.findTableAndRecordPath(self.selectDB ,argList)
        if selectTablePath is not None:
          if selectRecordPath is not None:
            if DBMS.MatchTableSetting(selectTablePath, argList, 'update'):
              DBMS.updateRecord(selectTablePath, selectRecordPath, argList)
          else: print '[Update Error] The record does not exist. Plz try "use --help" or "use -h" to get help.'
        else: print '[Update Error] The table does not exist. Plz try "use --help" or "use -h" to get help.'
      else: print '[Update Error] Choose the DB first. Plz try "use --help" or "use -h" to get help.'
    else: print '[Error] authority not enough.'

  def do_UPDATE(self, args):
    self.do_update( args )

  
  def do_delete(self, args):
    argList = str2List(args)
    if self.authority == 'admin':
      if self.selectDB is not None:
        selectTablePath, selectRecordPath = DBMS.findTableAndRecordPath(self.selectDB ,argList)
        if selectTablePath is not None:
          if selectRecordPath is not None:
            DBMS.deleteRecord(selectRecordPath)
          else: print '[Delete Error] The record does not exist. Plz try "use --help" or "use -h" to get help.'
        else: print '[Delete Error] The table does not exist. Plz try "use --help" or "use -h" to get help.'
      else: print '[Delete Error] Choose the DB first. Plz try "use --help" or "use -h" to get help.'
    else: print '[Error] authority not enough.'

  def do_DELETE(self, args):
    self.do_delete( args )
#deal with the empty input
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
#excute before the cmd execution
  def precmd(self, line):
    """ This method is called after the line has been input but before
        it has been interpreted. If you want to modifdy the input line
        before execution (for example, variable substitution) do it here.
    """

    if line.strip() != '':  self.cmd = line.strip().split()[0]
    self._hist += [ line.strip() ]
    if self.cmd == 'exit':
      self.do_exit(line)
    elif self.cmd == 'hist':
      self._hist.pop()
    elif len(self._hist) >= 2: 
      if (self._hist[len(self._hist)-2].find('define') >= 0) and (self.cmd != 'set'):
        if self.authority == 'admin':
          print "[Error] Plz finish relation setting first."
          self._hist.pop()
          line = ''
    return line
#execute after cmd execution
  def postcmd(self, stop, line):
    """If you want to stop the console, return something that evaluates to true.
       If you want to do some post command processing, do it here.
    """
    return stop
  
  
  def do_exit(self, args):
    return True   

if __name__ == '__main__':
    PySQL().cmdloop()