#!/usr/weblogic/bea/oracle/wlserver/common/bin/wlst.sh
import sys
print "start  updateDeploy perbank....."
connect('weblogic','weblogic','t3://localhost:7001')
stopApplication("perbank")
redeploy("perbank")
startApplication("perbank")
print "updateDeploy  Success........................"
