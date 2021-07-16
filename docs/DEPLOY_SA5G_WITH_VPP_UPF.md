<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface 5G Core Network Deployment and Testing with gnbsim</font></b>
    </td>
  </tr>
</table>

![SA dsTest Demo](./images/5gcn_vpp_upf.jpg)

**TABLE OF CONTENTS**

1.  Pre-requisites
2.  Building Container Images
3.  Configuring Host Machines
4.  Configuring OAI 5G Core Network Functions
5.  [Deploying OAI 5G Core Network with VPP-UPF](#5-deploying-oai-5g-core-network)
6.  [Configuring gnbsim Scenario](#6-configuring-gnbsim-scenario)
7.  [Executing gnbsim Scenario](#7-executing-the-gnbsim-scenario)
8.  [Traffic Test](#8-traffic-test)
9.  [Analysing Scenario Results](#8-analysing-the-scenario-results)


* In this demo the image tags and commits which were used are listed below, follow the [Building images](./BUILD_IMAGES.md) to build images with below tags. 

| CNF Name    | Branch Name             | Commit at time of writing                  | Ubuntu 18.04 | RHEL8          |
| ----------- |:----------------------- | ------------------------------------------ | ------------ | ---------------|
| AMF         | `develop`               | `82ca64fe8d79dbadbb1a495124ee26352f81bd7a` | X            | X              |
| SMF         | `nwi`                   | `0dba68d6a01e1dad050f47437647f62d40acaec6` | X            | X              |
| VPP_UPF     | `develop`               | `0e877cb5b80a9c74fa6abca60b95e2d3d22f7a52` | X            | X              |

<br/>

In previous tutorial we have used oai-spgwu-tiny UPF. Moreover in this utorial we are going to integrate oai 5g core with opensource VPP-UPF by [Travelping](https://www.travelping.com/). VPP based UPF uses vector packet processing and it is has proven very good performance in the user plane. Motivation for this integration to test and validate high performance VPP-UPF in with oai 5G core.

##### About VPP-UPG -
UPG implements a GTP-U user plane based on 3GPP TS 23.214
and 3GPP TS 29.244 Release 15. It is implemented as an
out-of-tree plugin for [Fdio VPP](https://github.com/FDio/vpp). The possible uses for UPG are:
* User Plane Function (UPF) in 5G networks
* Packet Data Network Gateway User plane (PGW-U)
* Traffic Detection Function User plane (TDF-U)

Project is available on github as VPP-UPG which follows release 16 of 3GPP specification TS 29.244. More details about VPP-UPG can be found on [official page](https://github.com/travelping/upg-vpp). VPP-UPG currently doesn't support NRF feature hence and it also uses optional IE called network instance (nwi) to uniquely identify interfaces of UPF in the form of domain name. Hence we use branch nwi from smf to handle this optional element for the moment.

Let's begin !!
* Steps 1 to 4 are similar as previous tutorial on [DsTest](https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed/-/blob/146e5d5925acdc9633b91ac3198c8cdeec3ef34f/docs/DEPLOY_SA5G_WITH_DS_TESTER.md). Please follow these steps to deploy OAI 5G core network components.
* We depoloy gnbsim docker service on same host as of core network, so there is no need to create additional route as we did for dsTest-host.

## 5. Deploying OAI 5g Core Network ##
* We will use same wrapper script for docker-compose that used for previous tutorials to set up 5gcn with VPP-UPF. Use help option to check how to use this wrapper script.
* Note:- Here we have additional option to select UPF version between OAI-UPF (openair-spgwu-tiny) and 3rd party UPF (vpp-upf).

```bash
 oai-cn5g-fed/docker-compose$ ./core-network.sh -h

Only use the following options

start [option1] [option2]: start the 5gCN
stop [option1] [option2]: stops the 5gCN

--option1
nrf: nrf should be used
no-nrf: nrf should not be used

--option2
vpp-upf: vpp-upf should be used (only works without nrf, no-nrf option1)
spgwu : spgwu should be used as upf (works with or without nrf, nrf or no-nrf option1)

Example 1 : ./core-network.sh start nrf spgwu
Example 2: ./core-network.sh start no-nrf vpp-upf
Example 1 : ./core-network.sh stop nrf spgwu
Example 2: ./core-network.sh stop no-nrf vpp-upf

```

Please make a note that VPP-UPF doesnt support NRF feature, hence we deply 5gcn with no-nrf.
```bash
oai-cn5g-fed/docker-compose$ ./core-network.sh start no-nrf vpp-upf
Starting 5gcn components in the order mysql, amf, smf, vpp-upf...
Creating network "oai-public-core" with the default driver
Creating network "oai-public-access" with the default driver
Creating network "oai-public-sgi-lan" with the default driver
Creating mysql   ... done
Creating vpp-upf ... done
Creating oai-ext-dn ... done
Creating oai-amf    ... done
vpp-upf is up-to-date
mysql is up-to-date
oai-ext-dn is up-to-date
oai-amf is up-to-date
Creating oai-smf ... done
Core network started, checking the health status of the containers...
mysql : "starting", oai-amf : "healthy", oai-smf : "healthy", vpp-upf : "healthy"
All components are healthy...
Checking the if the containers are configured...
Checking if SMF is able to connect with UPF

UPF receiving heathbeats from SMF...

Core network is configured and healthy, total time taken 25094 milli seconds
 ```
We can verify status of all components by docker command also -
```bash
oai-cn5g-fed/docker-compose$ docker ps -a
CONTAINER ID   IMAGE             COMMAND                  CREATED              STATUS                         PORTS                          NAMES
a4aec90a58f9   oai-smf:nwi       "/bin/bash /openair-…"   About a minute ago   Up About a minute (healthy)    80/tcp, 9090/tcp, 8805/udp     oai-smf
64f0c500bac7   oai-amf:develop   "/bin/bash /openair-…"   About a minute ago   Up About a minute (healthy)    80/tcp, 9090/tcp, 38412/sctp   oai-amf
568189fd0b3d   ubuntu:bionic     "/bin/bash -c ' apt …"   About a minute ago   Up About a minute                                             oai-ext-dn
2ad05b6ca5ee   mysql:5.7         "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)    3306/tcp, 33060/tcp            mysql
8195ddfa3a63   vpp-upg:develop   "/openair-upf/bin/en…"   About a minute ago   Up About a minute (healthy)                                   vpp-upf

```
## 6. Configuring gnbsim Scenario ##
* Build gnbsim docker image
```bash
$ git clone https://gitlab.eurecom.fr/kharade/gnbsim.git
$ cd gnbsim
$ docker build --tag gnbsim:develop --target gnbsim --file docker/Dockerfile.ubuntu.18.04 .
```

## 7. Executing the gnbsim Scenario ##
* The configuration parameters, are preconfigured in [docker-compose.yaml](../docker-compose/docker-compose.yaml) and [docker-compose-gnbsim.yaml](../docker-compose/docker-compose-gnbsim.yaml) and one can modify it for test.
* Launch gnbsim docker service
```bash
oai-cn5g-fed/docker-compose$ docker-compose -f docker-compose-gnbsim.yaml up -d gnbsim-vpp

Creating gnbsim ... done
```
* After launching gnbsim-vpp, make sure all services status are healthy -
```bash
oai-cn5g-fed/docker-compose$ docker ps -a
CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS                         PORTS                          NAMES
749d00791989   gnbsim:develop    "/gnbsim/bin/entrypo…"   43 seconds ago   Up 41 seconds (healthy)                                       gnbsim-vpp
a4aec90a58f9   oai-smf:nwi       "/bin/bash /openair-…"   2 minutes ago    Up 2 minutes (healthy)         80/tcp, 9090/tcp, 8805/udp     oai-smf
64f0c500bac7   oai-amf:develop   "/bin/bash /openair-…"   3 minutes ago    Up 3 minutes (healthy)         80/tcp, 9090/tcp, 38412/sctp   oai-amf
568189fd0b3d   ubuntu:bionic     "/bin/bash -c ' apt …"   3 minutes ago    Up 3 minutes                                                  oai-ext-dn
2ad05b6ca5ee   mysql:5.7         "docker-entrypoint.s…"   3 minutes ago    Up 3 minutes (healthy)         3306/tcp, 33060/tcp            mysql
8195ddfa3a63   vpp-upg:develop   "/openair-upf/bin/en…"   3 minutes ago    Up 3 minutes (healthy)                                        vpp-upf

```
## 8. Traffic Test ##
* Ping test <br/>
Here we ping UE from external DN container.
```bash
$ docker exec -it oai-ext-dn ping -c 3 12.1.1.2
PING 12.1.1.2 (12.1.1.2) 56(84) bytes of data.
64 bytes from 12.1.1.2: icmp_seq=1 ttl=64 time=0.235 ms
64 bytes from 12.1.1.2: icmp_seq=2 ttl=64 time=0.145 ms
64 bytes from 12.1.1.2: icmp_seq=3 ttl=64 time=0.448 ms

--- 12.1.1.2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2036ms
rtt min/avg/max/mdev = 0.145/0.276/0.448/0.127 ms
rohan@rohan:~/gitrepo/oai-cn5g-fed/docker-compose$ 
```

* We can verify PFCP session at VPP-UPF as below -
```bash
oai-cn5g-fed/docker-compose$ docker exec vpp-upf ./bin/vppctl show upf session

CP F-SEID: 0x0000000000000001 (1) @ 192.168.71.133
UP F-SEID: 0x0000000000000001 (1) @ 192.168.71.202
  PFCP Association: 0
  TEID assignment per choose ID
PDR: 1 @ 0x7f9c7290c630
  Precedence: 0
  PDI:
    Fields: 0000000d
    Source Interface: Access
    Network Instance: access.oai.org
    Local F-TEID: 79982499 (0x04c46fa3)
            IPv4: 192.168.72.202
    UE IP address (source):
      IPv4 address: 12.1.1.2
    SDF Filter [1]:
      permit out ip from any to assigned 
  Outer Header Removal: GTP-U/UDP/IPv4
  FAR Id: 1
  URR Ids: [] @ 0x0
  QER Ids: [] @ 0x0
PDR: 2 @ 0x7f9c7290c6b0
  Precedence: 0
  PDI:
    Fields: 0000000c
    Source Interface: SGi-LAN
    Network Instance: sgi.oai.org
    UE IP address (destination):
      IPv4 address: 12.1.1.2
    SDF Filter [1]:
      permit out ip from any to assigned 
  Outer Header Removal: no
  FAR Id: 2
  URR Ids: [] @ 0x0
  QER Ids: [] @ 0x0
FAR: 1
  Apply Action: 00000002 == [FORWARD]
  Forward:
    Network Instance: sgi.oai.org
    Destination Interface: 2
FAR: 2
  Apply Action: 00000002 == [FORWARD]
  Forward:
    Network Instance: access.oai.org
    Destination Interface: 0
    Outer Header Creation: [GTP-U/UDP/IPv4],TEID:9acb0442,IP:192.168.72.141
```
* To see traffic flows at VPP-UPF
```bash
oai-cn5g-fed/docker-compose$ docker exec vpp-upf ./bin/vppctl show upf flows
proto 0x1, 12.1.1.2:0 <-> 192.168.73.135:0, seid 0x0000000000000001, UL pkt 4, DL pkt 3, Forward PDR 2, Reverse PDR 1, app None, lifetime 60, proxy 0, spliced 0

```
## 9. Analysing the Scenario Results ##

| Container     | Ip-address     |
| ------------- |:-------------- |
| mysql         | 192.168.71.131 |
| oai-smf       | 192.168.71.132 |
| oai-amf       | 192.168.71.133 |
| vpp-upf (N3)  | 192.168.72.134 |
| vpp-upf (N4)  | 192.168.71.134 |
| vpp-upf (N6)  | 192.168.73.134 |
| gnbsim (sctp) | 192.168.71.141 |
| gnbsim (gtp)  | 192.168.72.141 |
| oai-ext-dn    | 192.168.73.135 |

| Pcap                                                                                       |
|:------------------------------------------------------------------------------------------ |
| [5gcn-deployment-vpp.pcap](./results/gnbSIM/5gcn-deployment-vpp.pcap)                |


* For detailed analysis of messages, please refer previous tutorial of [testing with dsTester](./docs/DEPLOY_SA5G_WITH_DS_TESTER.md).


Last thing is to remove all services - <br/>

* Undeploy the gnbsim
```bash
/oai-cn5g-fed/docker-compose$ docker-compose -f docker-compose-gnbsim.yaml down
Stopping service gnbsim ...
Stopping gnbsim ... done
Removing gnbsim ... done
Network demo-oai-public-net is external, skipping
Service gnbsim is  stopped
```

* Undeploy the core network
```bash
/oai-cn5g-fed/docker-compose$ ./core-network.sh stop no-nrf vpp-upf
Stopping service no-nrf ...
Stopping oai-smf    ... done
Stopping oai-amf    ... done
Stopping oai-ext-dn ... done
Stopping mysql      ... done
Stopping vpp-upf    ... done
Removing oai-smf    ... done
Removing oai-amf    ... done
Removing oai-ext-dn ... done
Removing mysql      ... done
Removing vpp-upf    ... done
Removing network oai-public-core
Removing network oai-public-access
Removing network oai-public-sgi-lan
Service no-nrf is stopped
```


