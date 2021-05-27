#/*
# * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The OpenAirInterface Software Alliance licenses this file to You under
# * the OAI Public License, Version 1.1  (the "License"); you may not use this file
# * except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *   http://www.openairinterface.org/?page_id=698
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *-------------------------------------------------------------------------------
# * For more information about the OpenAirInterface (OAI) Software Alliance:
# *   contact@openairinterface.org
# */
#---------------------------------------------------------------------

import re
import sys
import subprocess
import yaml

locexist = False
try:
    with open('DS-TEST-RESULTS/dsTester_Summary.txt') as f:
        for line in f:
            if re.search('Result file is available here', str(line)):
                result = re.search('(?:\/.+?\/)(.+?)(?:\/.+)', str(line))
                if result:
                    result1 = re.search('^(.*/)([^/]*)$', str(result.group(0)))
                    print(result1.group(1))
                    subprocess.Popen(f'cp {result1.group(1)}* DS-TEST-RESULTS/',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                locexist = True
except IOError:
    print("File not accessible to check DSTester Summary: DS-TEST-RESULTS/dsTester_Summary.txt")

if locexist:
    try:
        with open('DS-TEST-RESULTS/5gcn.yaml') as f:
            data = yaml.full_load(f)
            if data["final-result"] == 'fail':
                sys.exit(-1)
    except IOError:
        print("File not accessible to check DSTester result: DS-TEST-RESULTS/5gcn.yaml")
