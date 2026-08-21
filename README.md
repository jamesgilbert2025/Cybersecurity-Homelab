# Cybersecurity Homelab

A self-built lab environment for practicing identity and access management (IAM) and SOC-style security operations, built while pursuing a B.S. in Cybersecurity at Johnson & Wales University.

## Why This Exists

I'm targeting SOC and IAM analyst roles in financial services. This repo documents the infrastructure I've built and the security work I run on top of it, treated the way a real environment would be: configured, attacked, monitored, and hardened.

## Current Infrastructure

- **Hypervisor:** Proxmox VE on a Dell Optiplex 3060 (8GB RAM, 500GB HDD)
- **Networking:** Netgear GS108Tv3 managed switch, GL.iNet GL-MT300N-V2 travel router (repeater mode) providing WAN
- **Domain Controller:** Windows Server 2022 (Desktop Experience), VirtIO drivers, 60GB disk
- **Additional VMs:** Ubuntu Server (networking practice), Kali Linux (offensive tooling)

## Completed Work

### Active Directory Domain Controller
Stood up a Windows Server 2022 VM on Proxmox, installed the Active Directory Domain Services role, promoted it to a domain controller, and configured the domain from scratch, including DHCP and basic network connectivity for client VMs to join.

*(write-up and configs still to be published, see Repo Structure below)*

## Future Ideas

- **ASUS Eee PC (AntiX Linux):** separate legacy hardware project, not yet integrated into the main lab. Considering repurposing it as a rogue device on the network, simulating an attacker box that connects and attempts lateral movement, rather than just a standalone build.

## In Progress

- **SIEM deployment:** Wazuh on the domain controller for centralized log telemetry
- **Attack simulation:** Atomic Red Team and password spraying against the domain, hunting specific Windows Security Event IDs (e.g. 4625 failed logons)
- **VLAN segmentation** on the GS108Tv3
- **Vulnerability scanning** via OpenVAS or Nessus

## Repo Structure

Each project gets its own folder and write-up following the same format:

1. **Objective** — what problem this addresses and why it matters
2. **Architecture** — topology, tools, versions
3. **Execution** — commands, scripts, configs
4. **Analysis** — logs, screenshots, findings
5. **Hardening / Remediation** — what I'd fix or recommend

## Tools Used

Nmap, Wireshark, Metasploit, Cisco Packet Tracer, TryHackMe, SQLite/SQL, PowerShell, Python
