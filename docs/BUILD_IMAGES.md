<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface 5G Core Network Docker Deployment : Building the Images</font></b>
    </td>
  </tr>
</table>

# 1.  Retrieve the proper code version #

At the time of writing (2020 / 09 / 23), this is the current state:

 * Limited attach
 * We are using our 4G SPGW-U as UPF

**cNF Name** | **Branch Name** | **Commit at time of writing**              | Ubuntu18 | CentOS7 | CentOS8
------------ | --------------- | ------------------------------------------ | -------- | ------- | -------
AMF          | `develop`       | `8341c82073923601091f59803fe6c066cd8a68d8` | X        |         |  
SMF          | `develop`       | `e43b4429ce0eb8e754dd2bfbaa2c620cfa36ac49` | X        |         |  
SPGW-U-TINY  | `develop`       | `e812920bc48dcedb0e8f3811f3dbbe2ebebeb899` | X        |         |  

```bash
$ git clone https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed.git
$ cd oai-cn5g-fed
$ git checkout master
$ git pull origin master
$ ./scripts/syncComponents.sh
---------------------------------------------------------
OAI-AMF    component branch : develop
OAI-SMF    component branch : develop
OAI-SPGW-U component branch : develop
---------------------------------------------------------
....
```

# 2. Generic Parameters #

Here in our network configuration, we need to pass the "GIT PROXY" configuration.

*   If you do not need, remove the `--build-arg NEEDED_GIT_PROXY=".."` option.
*   If you do need it, change with your proxy value.

# 3. Build AMF Image #

## 3.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-amf --tag oai-amf:production \
               --file component/oai-amf/docker/Dockerfile.ubuntu.18.04 \
               --build-arg NEEDED_GIT_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-amf
$ docker image prune --force
$ docker image ls
oai-amf                 production             f478bafd7a06        1 minute ago          258MB
...
```

# 4. Build SMF Image #

## 4.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-smf --tag oai-smf:production \
               --file component/oai-smf/docker/Dockerfile.ubuntu.18.04 \
               --build-arg NEEDED_GIT_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-smf
$ docker image prune --force
$ docker image ls
oai-smf                 production             f478bafd7a06        1 minute ago          274MB
...
```

# 5. Build SPGW-U Image #

## 5.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-spgwu-tiny --tag oai-spgwu-tiny:production \
               --file component/oai-upf-equivalent/ci-scripts/Dockerfile.ubuntu18.04 \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" component/oai-upf-equivalent
$ docker image prune --force
$ docker image ls
oai-spgwu-tiny          production             588e14481f2b        1 minute ago          220MB
...
```

You are ready to [Configure the Containers](./CONFIGURE_CONTAINERS.md).
