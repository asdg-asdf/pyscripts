#!/home/mw/weblogic/wls1036/wlserver_10.3/common/bin/wlst.sh
import sys
print "start  updateDeploy samplev01....."
connect('weblogic','weblogic1','t3://localhost:7001')
undeploy("samplev01")
#redeploy("samplev01")
deploy("samplev01","/tmp/war/v3/samplev01.war",targets="mSrv1",securityModel="Advanced",timeout=600000,block="true")
startApplication("samplev01")
print "updateDeploy  samplev01 Success........................"
