#!/bin/bash

# Functioning of the script
# 1. Start
# 1.1 Start the core network components (Mysql ---> NRF ---> AMF ---> SMF --> SPGWU)
# 1.2 Check if the components started properly (skip)
# 1.3 Check if the components are healthy, calculate individual time
# 1.4 Check if the components are connected and core network is configured properly
# 1.5 Green light
# 2. Stop

RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'

if [[ $1 == 'start' ]]; then
	start_time=$(date +%s%N | cut -b1-13)
	echo -e "${BLUE}Starting 5gcn components in the order mysql, nrf, amf, smf, spgwu${NC}..."
	docker-compose -f docker-compose.yaml -p 5gcn up -d
	echo -e "${GREEN}Checking the health status of the containers${NC}..."
	while true; do
		mysql_health=$(docker inspect --format='{{json .State.Health.Status}}' mysql)
		nrf_health=$(docker inspect --format='{{json .State.Health.Status}}' oai-nrf)
		amf_health=$(docker inspect --format='{{json .State.Health.Status}}' oai-amf)
		smf_health=$(docker inspect --format='{{json .State.Health.Status}}' oai-smf)
		spgwu_health=$(docker inspect --format='{{json .State.Health.Status}}' oai-spgwu)
		if [[ ${mysql_health} == '"healthy"' && ${nrf_health} == '"healthy"' && ${amf_health} == '"healthy"' && ${smf_health} == '"healthy"' && ${spgwu_health} == '"healthy"' ]]; then
			echo -e "${GREEN}All components are healthy${NC}..."
			break
		else
			echo -e "${RED}Component Status\nmysql : $mysql_health\noai_nrf : $nrf_health\noai_amf : $amf_health\noai_smf : $smf_health\noai_spgwu : $spgwu_health${NC}"
			sleep 2
		fi
	done
	echo "Checking if core network is configured properly.."
	smf_registration_nrf=$(curl -s -X GET http://192.168.66.44/nnrf-nfm/v1/nf-instances?nf-type="SMF" | grep -o '192.168.66.43')
	upf_registration_nrf=$(curl -s -X GET http://192.168.66.44/nnrf-nfm/v1/nf-instances?nf-type="UPF" | grep -o '192.168.66.45')
	sample_registration=$(curl -s -X GET http://192.168.66.44/nnrf-nfm/v1/nf-instances?nf-type="SMF")
	echo -e "${BLUE}For example: oai-smf Registration with oai-nrf can be checked on this url /nnrf-nfm/v1/nf-instances?nf-type='SMF' $sample_registration${NC}"
	if [[ -z $smf_registration_nrf && -z $upf_registration_nrf ]]; then
		echo -e "${RED}Registration problem with NRF, check the reason manually${NC}..."
	else
		echo -e "${GREEN}SMF and UPF are registered to NRF${NC}..."
	fi
	upf_logs=$(docker logs oai-spgwu | grep  'Received SX HEARTBEAT RESPONSE')
	if [[ -z $upf_logs ]]; then
	 	echo -e "${RED}UPF not receiving heartbeats from SMF${NC}..."
	else
	 	echo -e "${GREEN}UPF receiving heathbeats from SMF${NC}..."
	fi
	end_time=$(date +%s%N | cut -b1-13)
	final_time=$(expr $(expr $end_time - $start_time))
	echo -e "${GREEN}Core network is running properly, total time taken $final_time milli seconds${NC}"

elif [[ $1 == 'stop' ]]; then
	echo -e "${BLUE}Stopping the core network${NC}..."
	docker-compose -f docker-compose.yaml -p 5gcn down
	echo -e "${GREEN}Core network stopped${NC}"
else
	echo -e "Please define either to ${RED}start${NC} or ${RED}stop${NC} the core network"
fi

