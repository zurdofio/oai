## Author: Sagar Arora
## Revised by: Rohan 

#!/bin/bash

# Functioning of the script
# 1. Start
# 1.1 Start the core network components (Mysql ---> NRF ---> AMF ---> SMF --> SPGWU)
# 1.1.1 Start the core network components (Mysql ---> NRF ---> AMF ---> SMF --> VPP-UPF)
# 1.2 Check if the components are healthy, calculate individual time
# 1.3 Check if the components are connected and core network is configured properly
# 1.4 Green light
# 2. Stop

RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
WHITE='\033[0;97m'
STATUS=0 #STATUS 0 exit safe STATUS 1 exit with an error

if [[ $1 == 'start' ]]; then
    start_time=$(date +%s%N | cut -b1-13)
    if [[ $2 == 'nrf' ]]; then
        echo -e "${BLUE}Starting 5gcn components in the order nrf, mysql, amf, smf, spgwu${NC}..."
        docker-compose -f docker-compose.yaml -p 5gcn up -d
    elif [[ $2 == 'no-nrf' ]]; then
        if [[ $3 == 'vpp-upf' ]]; then
            echo -e "${BLUE}Starting 5gcn components in the order mysql, amf, smf, vpp-upf${NC}..."
            docker-compose -f docker-compose-vpp-upf.yaml -p 5gcn up -d oai-amf
                sleep 5
            docker-compose -f docker-compose-vpp-upf.yaml -p 5gcn up -d oai-smf
        elif [[ $3 == 'spgwu' ]]; then
            echo -e "${BLUE}Starting 5gcn components in the order mysql, amf, smf, spgwu${NC}..."
            docker-compose -f docker-compose-no-nrf.yaml -p 5gcn up -d
        fi
    fi
    echo -e "${GREEN}Core network started, checking the health status of the containers${NC}..."
    # 25 is a interval it can be increased or decreased
    for loop in $(seq 1 25); do
        mysql_health=$(docker inspect --format='{{json .State.Health.Status}}' mysql)
        if [[ $2 == 'nrf' ]]; then
            nrf_health=$(docker inspect --format='{{json .State.Health.Status}}' oai-nrf)
        fi
        amf_health=$(docker inspect --format='{{json .State.Health.Status}}' oai-amf)
        smf_health=$(docker inspect --format='{{json .State.Health.Status}}' oai-smf)
        if [[ $3 == 'vpp-upf' ]];then
            vpp_upf_health=$(docker inspect --format='{{json .State.Health.Status}}' vpp-upf)
        else
            spgwu_health=$(docker inspect --format='{{json .State.Health.Status}}' oai-spgwu)
        fi
        if [[ ${mysql_health} == '"healthy"' && ${amf_health} == '"healthy"' && ${smf_health} == '"healthy"' && ${spgwu_health} == '"healthy"' && $2 != 'nrf' && $3 != 'vpp-upf' ]]; then
            echo -e "\n${GREEN}All components are healthy${NC}..."
            STATUS=0
            break
        elif [[ ${mysql_health} == '"healthy"' && ${amf_health} == '"healthy"' && ${smf_health} == '"healthy"' && ${spgwu_health} == '"healthy"' && ${nrf_health} == '"healthy"' && $2 == 'nrf' &&  $3 != 'vpp-upf' ]]; then
            echo -e "\n${GREEN}All components are healthy${NC}..."
            STATUS=0
            break
        elif [[ ${mysql_health} == '"healthy"' && ${amf_health} == '"healthy"' && ${smf_health} == '"healthy"' && ${vpp_upf_health} == '"healthy"' && $2 != 'nrf' && $3 == 'vpp-upf' ]]; then
            echo -e "\n${GREEN}All components are healthy${NC}..."
            STATUS=0
            break
        elif [[ $2 != 'nrf' && $3 == 'spgwu' ]]; then
            echo -ne "mysql : $mysql_health, oai-amf : $amf_health, oai-smf : $smf_health, oai-spgwu : $spgwu_health\033[0K\r"
            STATUS=1
            sleep 2
        elif [[ $2 != 'nrf' && $3 == 'vpp-upf' ]]; then
            echo -ne "mysql : $mysql_health, oai-amf : $amf_health, oai-smf : $smf_health, vpp-upf : $vpp_upf_health\033[0K\r"
            STATUS=1
            sleep 2
        elif [[ $2 == 'nrf' && $3 == 'spgwu' ]]; then
            echo -ne "oai-nrf : $nrf_health, mysql : $mysql_health, oai-amf : $amf_health, oai-smf : $smf_health, oai-spgwu : $spgwu_health\033[0K\r"
            STATUS=1
            sleep 2
        fi
    done
    echo -e "${BLUE}Checking the if the containers are configured${NC}..."
    if [[ $2 == 'nrf' && $3 != 'vpp-upf' && $STATUS == 0 ]]; then
        echo -e "\nChecking if SMF and UPF registered with nrf core network"
        smf_registration_nrf=$(curl -s -X GET http://192.168.70.130/nnrf-nfm/v1/nf-instances?nf-type="SMF" | grep -o '192.168.70.133')
        upf_registration_nrf=$(curl -s -X GET http://192.168.70.130/nnrf-nfm/v1/nf-instances?nf-type="UPF" | grep -o '192.168.70.134')
        sample_registration=$(curl -s -X GET http://192.168.70.130/nnrf-nfm/v1/nf-instances?nf-type="SMF")
        echo -e "\n${BLUE}For example: oai-smf Registration with oai-nrf can be checked on this url /nnrf-nfm/v1/nf-instances?nf-type='SMF' $sample_registration${NC}"
        if [[ -z $smf_registration_nrf && -z $upf_registration_nrf ]]; then
            echo -e "${RED}Registration problem with NRF, check the reason manually${NC}..."
            STATUS=1
        else
            echo -e "${GREEN}SMF and UPF are registered to NRF${NC}..."
        fi
    else
        echo -e "${BLUE}Checking if SMF is able to connect with UPF${NC}"
        if [[ $3 == 'vpp-upf' ]];then
            upf_logs=$(docker logs oai-smf | grep  'handle_receive(16 bytes)')
        else
            upf_logs=$(docker logs oai-spgwu | grep  'Received SX HEARTBEAT RESPONSE')
        fi
        if [[ -z $upf_logs && $STATUS == 0 ]]; then
            echo -e "\n${RED}UPF not receiving heartbeats from SMF${NC}..."
            STATUS=1
        else
            echo -e "\n${GREEN}UPF receiving heathbeats from SMF${NC}..."
        fi
    fi
    end_time=$(date +%s%N | cut -b1-13)
    final_time=$(expr $(expr $end_time - $start_time))
    if [[ $STATUS == 0 ]]; then
        echo -e "\n${GREEN}Core network is configured and healthy, total time taken $final_time milli seconds${NC}"
        exit $STATUS
    else
        echo -e "\n${RED}Core network is un-healthy, total time taken $final_time milli seconds\ndebug using docker inspect command...${NC}"
        exit $STATUS
    fi

elif [[ $1 == 'stop' ]]; then
    echo -e "${RED}Stopping service $2 ${NC}..."
    if [[ $2 == 'nrf' && $3 == 'spgwu' ]]; then
        docker-compose -f docker-compose.yaml -p 5gcn down
    elif [[ $2 != 'nrf' && $3 == 'vpp-upf' ]]; then
        docker-compose -f docker-compose-vpp-upf.yaml -p 5gcn down
    elif [[ $2 = 'no-nrf' && $3 == 'spgwu' ]]; then
        docker-compose -f docker-compose-no-nrf.yaml -p 5gcn down
    fi
    echo -e "${GREEN}Service $2 is stopped${NC}"
else
    echo -e "\nOnly use the following options\n
${RED}start ${WHITE}[option1]${NC} ${WHITE}[option2]${NC}: start the 5gCN\n\
${RED}stop ${WHITE}[option1]${NC} ${WHITE}[option2]${NC}: stops the 5gCN\n\
\n--option1\n\
${RED}nrf${NC}: nrf should be used\n\
${RED}no-nrf${NC}: nrf should not be used\n\
\n--option2\n\
${RED}vpp-upf${NC}: vpp-upf should be used (only works without nrf, no-nrf option1)\n\
${RED}spgwu${NC} : spgwu should be used as upf (works with or without nrf, nrf or no-nrf option1)\n\n\
Example 1 : ./core-network.sh start nrf spgwu\n\
Example 2: ./core-network.sh start no-nrf vpp-upf\n\
Example 1 : ./core-network.sh stop nrf spgwu\n\
Example 2: ./core-network.sh stop no-nrf vpp-upf"
fi

