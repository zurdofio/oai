<h1 align="center">
    <a href="https://openairinterface.org/"><img src="https://openairinterface.org/wp-content/uploads/2015/06/cropped-oai_final_logo.png" alt="OAI" width="550"></a>
</h1>

<p align="center">
    <a href="https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed/-/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-OAI--Public--V1.1-blue" alt="License"></a>
    <a href="https://jenkins-oai.eurecom.fr/job/OAI-CN5G-AMF/"><img src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins-oai.eurecom.fr%2Fjob%2FOAI-CN5G-AMF%2F&label=build%20AMF"></a>
    <a href="https://jenkins-oai.eurecom.fr/job/OAI-CN5G-NRF/"><img src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins-oai.eurecom.fr%2Fjob%2FOAI-CN5G-NRF%2F&label=build%20NRF"></a>
    <a href="https://jenkins-oai.eurecom.fr/job/OAI-CN5G-SMF/"><img src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins-oai.eurecom.fr%2Fjob%2FOAI-CN5G-SMF%2F&label=build%20SMF"></a>
</p>

<h2 align="center">
 OPENAIR-CN-5G: An implementation of the 5G Core network by the OpenAirInterface community.
</h2>

`OPENAIR-CN-5G` is an implementation of the 3GPP specifications for the 5G Core Network.
At the moment, it contains the following network elements:

* Access and Mobility Management Function (**[AMF](https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-amf)**)
* Authentication Server Management Function (**AUSF**)
* Network Repository Function (**[NRF](https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-nrf)**)
* Session Management Function (**[SMF](https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-smf)**)
* Unified Data Management (**UDM**)
* Unified Data Repository (**UDR**)
* User Plane Function (**UPF**) with 2 variants:
  * Simple Implementation based on our 4G CUPS component (**[SPGWU-TINY](https://github.com/OPENAIRINTERFACE/openair-spgwu-tiny)**)
  * VPP-Based Implementation (**UPF-VPP**)

Each has its own repository. Some of these repositories are still private, soon to be released.

This repository is a **Federation of the OpenAir CN 5G repositories**.

Its main purpose is for Continuous Integration scripting.

It also hosts some tutorials.

* [How to do a container-based simple deployment](docs/DEPLOY_HOME.md).

# Licence info

It is distributed under `OAI Public License V1.1`.
See [OAI Website for more details](https://www.openairinterface.org/?page_id=698).

The text for `OAI Public License V1.1` is also available under [LICENSE](LICENSE)
file at the root of this repository.

# Collaborative work

This source code is managed through a GITLAB server, a collaborative development platform.

Process is explained in [CONTRIBUTING](CONTRIBUTING.md) file.

# Contribution requests

In a general way, anybody who is willing can contribute on any part of the
code in any network component.

Contributions can be simple bugfixes, advices and remarks on the design,
architecture, coding/implementation.

# Release Notes

They are available on the [CHANGELOG](CHANGELOG.md) file.

