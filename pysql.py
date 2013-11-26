import cmd
import getpass
import os
import re

class PySQL(cmd.Cmd):

  def __init__(self):
    cmd.Cmd.__init__(self)
    self.prompt = 'pysql>>> '
    self.intro  = "Chris Hsu own SQL DB for DBMS project by Python"
    self.authority = 'user'
  def do_hist(self, argss):
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
      if self.authority == 'admin':
        print 'you are boss in PySQL!!'    
    elif password == 'user123':
      self.authority = 'user_admin'
      if self.authority == 'user_admin':
        print 'hello, visiter, wellcome to PySQL :)'
    else:
      print '[Error] Wrong Password :( Plz try again.'
    # args.split("")
  def do_logout(self, args):
    print "logout"
    if self.authority == 'admin' or self.authority == 'user_admin':
      self.prompt = 'pysql>>> '
      self.authority = 'user'
    # return True
  def do_define(self, args):
    # print "define"
    # print 'args:', args
    if self.authority == 'admin':
      args = args.split()[0].lower() + ' ' + args.split()[1]
      match = re.search('relation\s*\w*', args)
      if match is None:
        print '[Syntax Error] try "define --help" or "deifne -h" to get help.'
      else: 
        new_table_name = match.group().split()[1]
        os.mkdir('./DB/default/'+new_table_name)
    elif self.authority == 'user_admin':
      print '[Error] authority not enough.'
  
  def do_DEFINE(self, args):
    self.do_define(args)

  def do_set(self, args):
    # if self._hist.pop()
    print "set"

  def do_create_tabble(self, args):
    print args
  
  def do_insert(self, args):
    print "insert"
  
  def do_select(self, args):
    print "select"
  
  def do_update(self, args):
    print "update"
  
  def do_set(self, args):
    print "set"
  
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

  def postloop(self):
    """Take care of any unfinished business.
       Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
    """
    cmd.Cmd.postloop(self)   ## Clean up command completion
    print "Exiting..."

  def precmd(self, line):
    """ This method is called after the line has been input but before
        it has been interpreted. If you want to modifdy the input line
        before execution (for example, variable substitution) do it here.
    """
    print "pre command, line:", line.strip()

    self.cmd = line.strip()
    self._hist += [ line.strip() ]
    # print self._hist
    # print self._hist[len(self._hist)-2]
    if self.cmd == 'exit':
      self.do_exit(line)
    elif len(self._hist) >= 2: 
      if (self._hist[len(self._hist)-2].find('define') >= 0) and (self.cmd != 'set'):
        print "[Error] Plz finish relation setting first."
        self._hist.pop()
        line = ''
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