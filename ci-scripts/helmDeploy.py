#/*
# * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The OpenAirInterface Software Alliance licenses this file to You under
# * the OAI Public License, Version 1.1  (the "License"); you may not use this file
# * except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.openairinterface.org/?page_id=698
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *-------------------------------------------------------------------------------
# * For more information about the OpenAirInterface (OAI) Software Alliance:
# *      contact@openairinterface.org
# */
#---------------------------------------------------------------------
#
#   Required Python Version
#     Python 3.x
#
#   Required Python Package
#     pexpect
#---------------------------------------------------------------------

#-----------------------------------------------------------
# Import
#-----------------------------------------------------------
import logging
import sshconnection as SSH
import html
import os
import re
import time
import sys

class ClusterDeploy:
	def __init__(self):
		self.eNBIPAddress = ""
		self.eNBUserName = ""
		self.eNBPassword = ""
		self.OCUserName = ""
		self.OCPassword = ""
		self.OCProjectName = ""
		self.sourceCodePath = "/tmp/CI-CN5G-FED-RHEL8"
        self.imageTags = ""
		self.mode = ""

#-----------------$
#PUBLIC Methods$
#-----------------$

	def Deploy_5gcn(self):
		lIpAddr = self.eNBIPAddress
		lUserName = self.eNBUserName
		lPassWord = self.eNBPassword
		lSourcePath = self.sourceCodePath
		ocUserName = self.OCUserName
		ocPassword = self.OCPassword
		ocProjectName = self.OCProjectName
        limageTags = self.imageTags
		if lIpAddr == '' or lUserName == '' or lPassWord == '' or lSourcePath == '' or ocUserName == '' or ocPassword == '' or ocProjectName == '' or limageTags == '':
			sys.exit('Insufficient Parameter')
		logging.debug('Running on server: ' + lIpAddr)
		mySSH = SSH.SSHConnection()
		mySSH.open(lIpAddr, lUserName, lPassWord)
		mySSH.command('cd ' + lSourcePath, '\$', 5)

        images = limageTags.split(',')
        for image in images:
            eachImage = image.split(':')
            imageName = eachImage(0)
            imageTag = eachImage(1)
            # Check if image is exist on the Red Hat server, before pushing it to OC cluster
            mySSH.command("sudo podman image inspect --format='Size = {{.Size}} bytes' " + imageName + ":" + imageTag, '\$', 60)
            if mySSH.getBefore().count('no such image') != 0:
                logging.error(f'\u001B[1m No such image {imageName}]\u001B[0m')
                mySSH.close()
                sys.exit(-1)
            else:
                result = re.search('Size *= *(?P<size>[0-9\-]+) *bytes', mySSH.getBefore())
                if result is not None:
                    imageSize = float(result.group('size'))
                    imageSize = imageSize / 1000
                    if imageSize < 1000:
                        logging.debug(f'\u001B[1m   {imageName} size is ' + ('%.0f' % imageSize) + ' kbytes\u001B[0m')
                    else:
                        imageSize = imageSize / 1000
                        if imageSize < 1000:
                            logging.debug(f'\u001B[1m   {imageName} size is ' + ('%.0f' % imageSize) + ' Mbytes\u001B[0m')
                        else:
                            imageSize = imageSize / 1000
                            logging.debug(f'\u001B[1m   {imageName} is ' + ('%.3f' % imageSize) + ' Gbytes\u001B[0m')
                else:
                    logging.debug(f'{imageName} size is unknown')

		# logging to OC Cluster and then switch to corresponding project
		mySSH.command(f'oc login -u {ocUserName} -p {ocPassword}', '\$', 6)
		if mySSH.getBefore().count('Login successful.') == 0:
			logging.error('\u001B[1m OC Cluster Login Failed\u001B[0m')
			mySSH.close()
			sys.exit(-1)
		else:
			logging.debug('\u001B[1m   Login to OC Cluster Successfully\u001B[0m')
		mySSH.command(f'oc project {ocProjectName}', '\$', 6)
		if mySSH.getBefore().count(f'Already on project "{ocProjectName}"') == 0 and mySSH.getBefore().count(f'Now using project "{self.OCProjectName}"') == 0:
			logging.error(f'\u001B[1m Unable to access OC project {ocProjectName}\u001B[0m')
			mySSH.close()
			sys.exit(-1)
		else:
			logging.debug(f'\u001B[1m   Now using project {ocProjectName}\u001B[0m')

		# Tag the image and push to the OC cluster
		mySSH.command('oc whoami -t | sudo podman login -u ' + ocUserName + ' --password-stdin https://default-route-openshift-image-registry.apps.5glab.nsa.eurecom.fr/ --tls-verify=false', '\$', 6)
		if mySSH.getBefore().count('Login Succeeded!') == 0:
			logging.error('\u001B[1m Podman Login to OC Cluster Registry Failed\u001B[0m')
			mySSH.close()
			sys.exit(-1)
		else:
			logging.debug('\u001B[1m Podman Login to OC Cluster Registry Successfully\u001B[0m')
        for image in images:
            imageName = image(0)
            imageTag = image(1)
            mySSH.command(f'oc create -f openshift/{imageName}-image-stream.yml', '\$', 6)
            if mySSH.getBefore().count('(AlreadyExists):') == 0 and mySSH.getBefore().count('created') == 0:
                logging.error(f'\u001B[1m Image Stream "{imageName}" Creation Failed on OC Cluster {ocProjectName}\u001B[0m')
                mySSH.close()
                sys.exit(-1)
            else:
                logging.debug(f'\u001B[1m   Image Stream "{imageName}" created on OC project {ocProjectName}\u001B[0m')
            mySSH.command(f'sudo podman tag {imageName}:{imageTag} default-route-openshift-image-registry.apps.5glab.nsa.eurecom.fr/{self.OCProjectName}/{imageName}:{imageTag}', '\$', 6)
            mySSH.command(f'sudo podman push default-route-openshift-image-registry.apps.5glab.nsa.eurecom.fr/{self.OCProjectName}/{imageName}:{imageTag} --tls-verify=false', '\$', 60)
            if mySSH.getBefore().count('Storing signatures') == 0:
                logging.error(f'\u001B[1m Image "{imageName}" push to OC Cluster Registry Failed\u001B[0m')
                mySSH.close()
                sys.exit(-1)
            else:
                logging.debug(f'\u001B[1m Image "{imageName}" push to OC Cluster Registry Successfully\u001B[0m')

		passPods = 0
		# Using helm charts deployment
		time.sleep(5)
        for image in images:
            eachImage = image.split(':')
            imageName = eachImage(0)
            imageTag = eachImage(1)		
			mySSH.command(f'sed -i -e "s#TAG#{imageTag}#g" ./charts/oai-5gcn/charts/{imageName}/values.yaml', '\$', 6)
			if imageName == 'oai-nrf':
				nameSufix = 'nrf'
			elif imageName == 'oai-amf':
				nameSufix = 'amf'
			elif imageName == 'oai-smf':
				nameSufix = 'smf'
			elif imageName == 'oai-spgwu-tiny':
				nameSufix = 'spgwu'
			mySSH.command(f'helm install {imageName} ./charts/{imageName}/ | tee -a archives/5gcn_helm_summary.txt 2>&1', '\$', 6)
			if mySSH.getBefore().count('STATUS: deployed') == 0:
				logging.error(f'\u001B[1m Deploying "{imageName}" Failed using helm chart on OC Cluster\u001B[0m')
			else:
				logging.debug(f'\u001B[1m   Deployed "{imageName}" Successfully using helm chart\u001B[0m')
			time.sleep(60)
			mySSH.command(f'oc get pods -o wide -l app.kubernetes.io/name={imageName} | tee -a archives/5gcn_pods_summary.txt', '\$', 6, resync=True)
			podName = re.findall(f'{imageName}[\S\d\w]+', mySSH.getBefore())
			isRunning = False
			count = 0
			while count < 2 and isRunning == False:
				time.sleep(60)
				mySSH.command(f'oc exec {podName} -c {nameSufix} -it -- ps aux', '\$', 6, resync=True)
				if mySSH.getBefore().count(f'oai_{nameSufix}') != 0:
					logging.debug(f'\u001B[1m POD "{imageName}" Service Running Sucessfully\u001B[0m')
					isRunning = True
					passPods += 1
				count +=1	
			if isRunning == False:
				logging.error(f'\u001B[1m POD "{imageName}" Service Running FAILED \u001B[0m')

		if passPods == 4:
			logging.debug(f'\u001B[1m   Deployment: OK \u001B[0m')
		else:
			logging.error(f'\u001B[1m 	Deployment: KO \u001B[0m')
			self.UnDeploy_5gcn()
			self.AnalyzeLogFile_5gcn()
			sys.exit(-1)
		self.AnalyzeLogFile_5gcn()
		
	def UnDeploy_5gcn(self):
		mySSH = SSH.SSHConnection()
		mySSH.open(lIpAddr, lUserName, lPassWord)
		mySSH.command('cd ' + lSourcePath, '\$', 5)
		logging.debug('\u001B[1m   UnDeploying the 5gcn\u001B[0m')
		# logging to OC Cluster and then switch to corresponding project
		mySSH.command(f'oc login -u {ocUserName} -p {ocPassword}', '\$', 6)
		if mySSH.getBefore().count('Login successful.') == 0:
			logging.error('\u001B[1m OC Cluster Login Failed\u001B[0m')
			mySSH.close()
			sys.exit(-1)
		else:
			logging.debug('\u001B[1m   Login to OC Cluster Successfully\u001B[0m')
		mySSH.command(f'oc project {ocProjectName}', '\$', 6)
		if mySSH.getBefore().count(f'Already on project "{ocProjectName}"') == 0 and mySSH.getBefore().count(f'Now using project "{self.OCProjectName}"') == 0:
			logging.error(f'\u001B[1m Unable to access OC project {ocProjectName}\u001B[0m')
			mySSH.close()
			sys.exit(-1)
		else:
			logging.debug(f'\u001B[1m   Now using project {ocProjectName}\u001B[0m')

		# UnDeploy the 5gcn pods
		images = self.imageTags.split(',')
        for image in images:
            eachImage = image.split(':')
            imageName = eachImage(0)
            imageTag = eachImage(1)
			mySSH.command(f'helm uninstall {imageName} | tee -a archives/5gcn_helm_summary.txt 2>&1', '\$', 6)
			if mySSH.getBefore().count(f'release "{imageName}" uninstalled') == 0 and mySSH.getBefore().count('release: not found') == 0:
				logging.error(f'\u001B[1m UnDeploying "{imageName}" Failed using helm chart on OC Cluster\u001B[0m')
			else:
				logging.debug(f'\u001B[1m   UnDeployed "{imageName}" Successfully on OC Cluster\u001B[0m')
			# Delete images and imagestream
			mySSH.command(f'sudo podman rmi default-route-openshift-image-registry.apps.5glab.nsa.eurecom.fr/{self.OCProjectName}/{imageName}:{imageTag}', '\$', 6)
			mySSH.command(f'oc delete is {imageName}', '\$', 6)
			logging.debug(f'\u001B[1m Deleted the "{imageName}" Image and ImageStream\u001B[0m')
		mySSH.command('oc logout', '\$', 6)
		mySSH.close()
		self.AnalyzeLogFile_5gcn()


	def AnalyzeLogFile_5gcn(self):
		pass



#--------------------------------------------------------------------------------------------------------
#
# Start of main
#
#--------------------------------------------------------------------------------------------------------

CN = ClusterDeploy()

argvs = sys.argv
argc = len(argvs)

while len(argvs) > 1:
    myArgv = argvs.pop(1)
    if re.match('^\-\-mode=(.+)$', myArgv, re.IGNORECASE):
        matchReg = re.match('^\-\-mode=(.+)$', myArgv, re.IGNORECASE)
        CN.mode = matchReg.group(1)	
    elif re.match('^\-\-eNBIPAddress=(.+)$', myArgv, re.IGNORECASE):
        matchReg = re.match('^\-\-eNBIPAddress=(.+)$', myArgv, re.IGNORECASE)
        CN.eNBIPAddress = matchReg.group(1)
    elif re.match('^\-\-eNBUserName=(.+)$', myArgv, re.IGNORECASE):
        matchReg = re.match('^\-\-eNBUserName=(.+)$', myArgv, re.IGNORECASE)
        CN.eNBUserName = matchReg.group(1)
    elif re.match('^\-\-eNBPassword=(.+)$', myArgv, re.IGNORECASE):
        matchReg = re.match('^\-\-eNBPassword=(.+)$', myArgv, re.IGNORECASE)
        CN.eNBPassword = matchReg.group(1)
    elif re.match('^\-\-OCUserName=(.+)$', myArgv, re.IGNORECASE):
        matchReg = re.match('^\-\-OCUserName=(.+)$', myArgv, re.IGNORECASE)
        CN.OCUserName = matchReg.group(1)
    elif re.match('^\-\-OCPassword=(.+)$', myArgv, re.IGNORECASE):
        matchReg = re.match('^\-\-OCPassword=(.+)$', myArgv, re.IGNORECASE)
        CN.OCPassword = matchReg.group(1)
    elif re.match('^\-\-OCProjectName=(.+)$', myArgv, re.IGNORECASE):
        matchReg = re.match('^\-\-OCProjectName=(.+)$', myArgv, re.IGNORECASE)
        CN.OCProjectName = matchReg.group(1)
    elif re.match('^\-\-imageTags=(.+)$', myArgv, re.IGNORECASE):
        matchReg = re.match('^\-\-imageTags=(.+)$', myArgv, re.IGNORECASE)
        CN.imageTags = matchReg.group(1)
	else:
		sys.exit('Invalid Parameter: ' + myArgv)

if CN.mode == 'Deploy':
	CN.Deploy_5gcn()
elif CN.mode == 'UnDeploy':
	CN.UnDeploy_5gcn()