#!/bin/bash
set -eo pipefail

sleep 2
IS_VPP_UPF=$(docker ps -a | grep vpp-upg | awk {'print $2'})
if [$IS_VPP_UPF=="vpp-upg:develop"];then
    x=1, VPP_STATUS=0
    while [ $x -le 10 ]
	do
		VPP_UPF_PFCP_ENDPOINT=$(docker exec -it vpp-upf ./bin/vppctl show upf pfcp endpoint | awk -v RS='([0-9]+\\.){3}[0-9]+' 'RT{print RT}')
		PING_STATE=$(ping -c 3 $VPP_UPF_PFCP_ENDPOINT | grep "icmp_seq")
		if [ -z "$var" ];then
			echo "PFCP endpoint could not be reached"
		else
			echo "PFCP endpoint is ready, restarting SMF"
			docker restart oai-smf
		fi
		x=$(( $x + 1 ))
	done
fi

STATUS=0
SMF_IP_SBI_INTERFACE=$(ifconfig $SMF_INTERFACE_NAME_FOR_SBI | grep inet | awk {'print $2'})
#Check if entrypoint properly configured the conf file and no parameter is unset(optional)
SMF_SBI_PORT_STATUS=$(netstat -tnpl | grep -o "$SMF_IP_SBI_INTERFACE:$SMF_INTERFACE_PORT_FOR_SBI")
NB_UNREPLACED_AT=`cat /openair-smf/etc/*.conf | grep -v contact@openairinterface.org | grep -c @ || true`

if [ $NB_UNREPLACED_AT -ne 0 ]; then
	STATUS=-1
	echo "Healthcheck error: UNHEALTHY configuration file is not configured properly"
fi

if [[ -z $SMF_SBI_PORT_STATUS ]]; then
	STATUS=-1
	echo "Healthcheck error: UNHEALTHY SBI TCP/HTTP port $SMF_INTERFACE_PORT_FOR_SBI is not listening."
fi

exit $STATUS