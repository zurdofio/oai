<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface 5G Core Network Docker Deployment : Building Container Images</font></b>
    </td>
  </tr>
</table>

# 1.  Retrieve the correct network function branches #

| CNF Name    | Branch Name             | Commit at time of writing                  | Ubuntu 18.04 | RHEL8          |
| ----------- |:----------------------- | ------------------------------------------ | ------------ | ---------------|
| AMF         | `develop`               | `82ca64fe8d79dbadbb1a495124ee26352f81bd7a` | X            | Releasing soon |
| SMF         | `develop`               | `0dba68d6a01e1dad050f47437647f62d40acaec6` | X            | Releasing soon |
| NRF         | `develop`               | `0e877cb5b80a9c74fa6abca60b95e2d3d22f7a52` | X            | Releasing soon |
| SPGW-U-TINY | `gtp_extension_header`  | `b628036d2e6060da8ba77c5e4cdde35bf18a62a5` | X            | Releasing soon |

```bash
$ git clone https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed.git
$ cd oai-cn5g-fed
$ git checkout master
$ git pull origin master
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

$ ./scripts/syncComponents.sh --spgwu-tiny-branch gtp_extension_header
---------------------------------------------------------
OAI-AMF    component branch : develop
OAI-SMF    component branch : develop
OAI-NRF    component branch : develop
OAI-SPGW-U component branch : gtp_extension_header
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
               --file component/oai-amf/docker/Dockerfile.ubuntu.18.04 \
               --build-arg NEEDED_GIT_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-amf
$ docker image prune --force
$ docker image ls
oai-amf                 develop             f478bafd7a06        1 minute ago          258MB
...
```

# 4. Build SMF Image #

## 4.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-smf --tag oai-smf:develop \
               --file component/oai-smf/docker/Dockerfile.ubuntu18.04 \
               --build-arg NEEDED_GIT_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-smf
$ docker image prune --force
$ docker image ls
oai-smf                 develop             f478bafd7a06        1 minute ago          274MB
...
```

# 5. Build NRF Image #

## 5.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-nrf --tag oai-nrf:develop \
               --file component/oai-nrf/docker/Dockerfile.ubuntu.18.04 \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" component/oai-nrf
$ docker image prune --force
$ docker image ls
oai-nrf                 develop             04334b29e103        1 minute ago          280MB
...
```


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

You are ready to [Configure the Containers](./CONFIGURE_CONTAINERS.md).
