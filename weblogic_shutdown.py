#!/usr/weblogic/bea/oracle/wlserver/common/bin/wlst.sh
import sys
print "shutdown   testappsrv  server....."
connect('weblogic','weblogic','t3://localhost:7001')
shutdown('testappsrv','Server','false',1000,'true', 'false')
print "shutdown  testappsrv server Success........................"
