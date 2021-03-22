<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface 5G Core Network Docker Deployment : Configure Containers</font></b>
    </td>
  </tr>
</table>


**TABLE OF CONTENTS**

1.  [Networking](#1-create-a-docker-bridged-network)
2.  [Deploy](#2-deploy-the-containers)
3.  [Configure](#3-configure-the-containers)

# 1. Create a Docker Bridge Network #

```bash
$ docker network create --attachable --subnet 192.168.61.0/26 --ip-range 192.168.61.0/26 prod-oai-public-net
```

Once again we chose an **IDLE** IP range in our network. **Please change to proper value in your environment.**

# 2. Deploy the containers #

Container deployment has to follow a strict order if the `NRF` is used for `SMF` and `UPF` registration
mysql --> oai-nrf --> oai-amf --> oai-smf --> oai-upf

# 3. Configure the containers #

**TODO**

