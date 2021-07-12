<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface 5G Core Network Deployment : Building Container Images</font></b>
    </td>
  </tr>
</table>

# 1.  Retrieve the correct network function branches #

| CNF Name    | Branch Name | Commit at time of writing                  | Ubuntu 18.04 | RHEL8 (UBI8)    |
| ----------- |:----------- | ------------------------------------------ | ------------ | ----------------|
| AMF         | `develop`   | `f31dc5a5a013882f4c5f6132d1b2af7f6c98ece2` | X            | X               |
| SMF         | `develop`   | `7e3ffb6b444269b7667501ee82da9c7b3f7bf9eb` | X            | X               |
| NRF         | `develop`   | `f722502f92333747503b13491962ade7c5e6dbca` | X            | X               |
| SPGW-U-TINY | `develop`   | `7f687f853eaa7617ba56da186d0d55afb6219558` | X            | X               |

**UPDATE (2021/07/12): all branches have been tagged with `2021.w28`.**

**PLEASE USE newer commits than these tags.**

```bash
$ git clone https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed.git
$ cd oai-cn5g-fed

# You can specify a tag on the parent GIT repository such as `2021.w28`
$ git checkout 2021.w28
# Or you can sync to the latest version
$ git checkout master

# Then you need to resync the sub-modules (ie AMF, SPGW-U-TINY, SMF, NRF).
# You can specify:
#   ---  a valid tag (such as seen)
#   ---  a newer tag
#   ---  a branch to get the latest (`develop` being the latest stable)
#        Usually the better option is to specify `develop`


$ ./scripts/syncComponents.sh -h
Openair-CN components synchronization
   Original Author: Raphael Defosseux

   Requirement: git shall be installed

   By default (no options) all components will be synchronized to
     the 'develop' branch.
   Each component can be synchronized a dedicated branch.

Usage:
------
    syncComponents.sh [OPTIONS]

Options:
--------
    --nrf-branch ####
    Specify the source branch for the OAI-NRF component

    --amf-branch ####
    Specify the source branch for the OAI-AMF component

    --smf-branch ####
    Specify the source branch for the OAI-SMF component

    --spgwu-tiny-branch ####
    Specify the source branch for the OAI-SPGW-U-TINY component

    --help OR -h
    Print this help message.

$ ./scripts/syncComponents.sh --spgwu-tiny-branch 2021.w28
---------------------------------------------------------
OAI-AMF    component branch : develop
OAI-SMF    component branch : develop
OAI-NRF    component branch : develop
OAI-SPGW-U component branch : 2021.w28
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
$ docker build --target oai-amf --tag oai-amf:develop \
               --file component/oai-amf/docker/Dockerfile.amf.ubuntu18 \
               --build-arg NEEDED_GIT_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-amf
$ docker image prune --force
$ docker image ls
oai-amf                 develop             f478bafd7a06        1 minute ago          258MB
...
```

## 3.2 On a RHEL8 Host ##

RHEL base images generally needs a subscription to access the package repository. For that the base image needs ca and entitlement .pem files. Copy the ca and entitlement .pem files in the oai-amf repository in a new folder name tmp before building the image. 

```bash
$ sudo podman build --target oai-amf --tag oai-amf:develop \
               --file component/oai-amf/docker/Dockerfile.amf.rhel8 \
               --build-arg NEEDED_GIT_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-amf
...
```

The above command is with podman, in case of docker it can be changed with its docker equivalent.


# 4. Build SMF Image #

## 4.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-smf --tag oai-smf:develop \
               --file component/oai-smf/docker/Dockerfile.smf.ubuntu18 \
               --build-arg NEEDED_GIT_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-smf
$ docker image prune --force
$ docker image ls
oai-smf                 develop             f478bafd7a06        1 minute ago          274MB
...
```

## 4.2 On a RHEL8 Host ##

RHEL base images generally needs a subscription to access the package repository. For that the base image needs ca and entitlement .pem files. Copy the ca and entitlement .pem files in the oai-smf repository in a new folder name tmp before building the image. 

```bash
$ sudo podman build --target oai-smf --tag oai-smf:develop \
               --file component/oai-smf/docker/Dockerfile.smf.rhel8 \
               --build-arg NEEDED_GIT_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-smf
...
```

The above command is with podman, in case of docker it can be changed with its docker equivalent.

# 5. Build NRF Image #

## 5.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-nrf --tag oai-nrf:develop \
               --file component/oai-nrf/docker/Dockerfile.nrf.ubuntu18 \
               --build-arg NEEDED_GIT_PROXY="http://proxy.eurecom.fr:8080" component/oai-nrf
$ docker image prune --force
$ docker image ls
oai-nrf                 develop             04334b29e103        1 minute ago          280MB
...
```

## 5.2 On a RHEL8 Host ##

RHEL base images generally needs a subscription to access the package repository. For that the base image needs ca and entitlement .pem files. Copy the ca and entitlement .pem files in the oai-nrf repository in a new folder name tmp before building the image. 

```bash
$ sudo podman build --target oai-nrf --tag oai-nrf:develop \
               --file component/oai-nrf/docker/Dockerfile.nrf.rhel8 \
               --build-arg NEEDED_GIT_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-nrf
...
```

The above command is with podman, in case of docker it can be changed with its docker equivalent.

# 6. Build SPGW-U Image #

## 6.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-spgwu-tiny --tag oai-spgwu-tiny:gtp-ext-header \
               --file component/oai-upf-equivalent/docker/Dockerfile.ubuntu18.04 \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" component/oai-upf-equivalent
$ docker image prune --force
$ docker image ls
oai-spgwu-tiny          gtp-ext-header             dec6311cef3b        1 minute ago          255MB
...
```

## 6.2 On a RHEL8 Host ##

RHEL base images generally needs a subscription to access the package repository. For that the base image needs ca and entitlement .pem files. Copy the ca and entitlement .pem files in the oai-spgwu repository in a new folder name tmp before building the image. 

```bash
$ sudo podman build --target oai-spgwu-tiny --tag oai-spgwu-tiny:develop \
               --file component/oai-spgwu-tiny/docker/Dockerfile.centos8 \
               --build-arg NEEDED_GIT_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-upf-equivalent
...
```

The above command is with podman, in case of docker it can be changed with its docker equivalent.

You are ready to [Configure the Containers](./CONFIGURE_CONTAINERS.md) or deploying the images using [helm-charts] (./DEPLOY_SA5G_HC.md)
