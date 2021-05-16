<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface 5G Core Network Deployment and Testing with dsTest</font></b>
    </td>
  </tr>
</table>

![SA dsTest Demo](./images/5gCN_gnbsim.jpg)

**TABLE OF CONTENTS**

1.  Pre-requisites
2.  Building Container Images
3.  Configuring Host Machines
4.  Configuring OAI 5G Core Network Functions
5.  Deploying OAI 5G Core Network
6.  [Configuring gnbsim Scenario](#6-configuring-gnbsim-scenario)
7.  [Executing gnbsim Scenario](#7-executing-the-gnbsim-scenario)


This tutorial is a extension of previous tutorial. In previous tutorial we have seen the advanced testing tool dsTester, which is useful for validating even more complex scenarios. Moreover, there are various other opensource gnb/ue simulator tools are available for SA5G test. In this tutorial we use opensource simulator tool called gnbsim. With the help of gnbsim tool, we can perform very basic SA5G test by simulating one gnb and one ue. 

* Steps 1 to 5 are similar as previous tutorial. Please follow these steps to deploy OAI 5G core network components.

## 6. Configuring gnbsim Scenario ##
* Build gnbsim docker image
```bash
$ git clone https://gitlab.eurecom.fr/kharade/gnbsim.git
$ cd gnbsim
$ docker build --tag gnbsim:develop --target gnbsim --file docker/Dockerfile.ubuntu.18.04 .
```

## 7. Executing the gnbsim Scenario ##
* Launch gnbsim docker service
```bash
oai-cn5g-fed/docker-compose$ ./core-network.sh start gnbsim

Creating gnbsim ... done
```
* Ping test
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
* Iperf test
Here we do iperf traffic test between gnbsim UE and external DN node. We can make any node as iperf server/client.<br/>
Running iperf server on external DN container
```bash
$ docker exec -it oai-ext-dn iperf3 -s 
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
Accepted connection from 12.1.1.2, port 43339
[  5] local 192.168.70.135 port 5201 connected to 12.1.1.2 port 55553
[ ID] Interval           Transfer     Bandwidth
[  5]   0.00-1.00   sec  73.8 MBytes   619 Mbits/sec                  
[  5]   1.00-2.00   sec  76.3 MBytes   640 Mbits/sec                  
[  5]   2.00-3.00   sec  77.8 MBytes   653 Mbits/sec                  
[  5]   3.00-4.00   sec  66.7 MBytes   560 Mbits/sec                  
[  5]   4.00-5.00   sec  71.9 MBytes   603 Mbits/sec                  
[  5]   5.00-6.00   sec  80.2 MBytes   673 Mbits/sec                  
[  5]   6.00-7.00   sec  76.5 MBytes   642 Mbits/sec                  
[  5]   7.00-8.00   sec  78.6 MBytes   659 Mbits/sec                  
[  5]   8.00-9.00   sec  74.5 MBytes   625 Mbits/sec                  
[  5]   9.00-10.00  sec  75.5 MBytes   634 Mbits/sec                  
[  5]  10.00-10.01  sec   740 KBytes   719 Mbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth
[  5]   0.00-10.01  sec  0.00 Bytes  0.00 bits/sec                  sender
[  5]   0.00-10.01  sec   753 MBytes   631 Mbits/sec                  receiver
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
```
Running iperf client on gnbsim
```bash
$ docker exec -it gnbsim iperf3 -c 192.168.70.135 -B 12.1.1.2
Connecting to host 192.168.70.135, port 5201
[  5] local 12.1.1.2 port 55553 connected to 192.168.70.135 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  77.6 MBytes   651 Mbits/sec   29    600 KBytes       
[  5]   1.00-2.00   sec  76.2 MBytes   640 Mbits/sec    0    690 KBytes       
[  5]   2.00-3.00   sec  77.5 MBytes   650 Mbits/sec    4    585 KBytes       
[  5]   3.00-4.00   sec  66.2 MBytes   556 Mbits/sec  390    354 KBytes       
[  5]   4.00-5.00   sec  72.5 MBytes   608 Mbits/sec    0    481 KBytes       
[  5]   5.00-6.00   sec  80.0 MBytes   671 Mbits/sec    0    598 KBytes       
[  5]   6.00-7.00   sec  76.2 MBytes   640 Mbits/sec    7    684 KBytes       
[  5]   7.00-8.00   sec  78.8 MBytes   661 Mbits/sec    3    578 KBytes       
[  5]   8.00-9.00   sec  75.0 MBytes   629 Mbits/sec    1    670 KBytes       
[  5]   9.00-10.00  sec  75.0 MBytes   629 Mbits/sec    5    554 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec   755 MBytes   633 Mbits/sec  439             sender
[  5]   0.00-10.00  sec   753 MBytes   631 Mbits/sec                  receiver

iperf Done.
```


