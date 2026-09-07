## Current Infrastructure

- **Hypervisor:** Proxmox VE on a Dell Optiplex 3060 (8GB RAM, 500GB HDD)
- **Networking:** Netgear GS108Tv3 managed switch, GL.iNet GL-MT300N-V2 travel router (repeater mode) providing WAN
- **Domain Controller:** Windows Server 2022 (Desktop Experience), VirtIO drivers, 60GB disk
- **SIEM:** Ubuntu Server running Wazuh manager, indexer, and dashboard
- **Additional VMs:** Kali Linux (offensive tooling)

## Completed Work

### Active Directory Domain Controller
Stood up a Windows Server 2022 VM on Proxmox, installed the Active Directory Domain Services role, promoted it to a domain controller, and configured the domain from scratch, including DHCP and basic network connectivity for client VMs to join.

*(write-up and configs still to be published, see Repo Structure below)*

### Wazuh SIEM Deployment
Deployed a full Wazuh stack (manager, indexer, dashboard) on a dedicated Ubuntu Server VM and enrolled the domain controller as a monitored agent, including resolving a chain of real install/config failures along the way. See `/Wazuh/wazuh-siem-deployment.md` for the full write-up.

## In Progress

- **Attack simulation:** Atomic Red Team and password spraying against the domain, hunting specific Windows Security Event IDs (e.g. 4625 failed logons) and validating detection in Wazuh
- **Additional agent coverage:** enrolling the Windows 11 client VM
- **VLAN segmentation** on the GS108Tv3
- **Vulnerability scanning** via OpenVAS or Nessus