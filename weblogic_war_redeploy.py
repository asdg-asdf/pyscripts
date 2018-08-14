#!/usr/weblogic/bea/oracle/wlserver/common/bin/wlst.sh
import sys
print "start  updateDeploy testwar....."
connect('weblogic','weblogic','t3://localhost:7001')
stopApplication("testwar")
redeploy("testwar")
startApplication("testwar")
print "updateDeploy  Success........................"
