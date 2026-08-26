# Active Directory Domain Join: Windows 11 Client

## Executive Objective
Extend the existing Active Directory environment (`khoo.local`) by deploying a Windows 11 Pro client VM in Proxmox and joining it to the domain. The goal was to validate end-to-end domain functionality, DNS-based service location, authentication, and initial credential lifecycle policy, laying the foundation for future Group Policy and SIEM log correlation labs.

## Architecture / Topology
- **Hypervisor:** Proxmox VE, running on a Dell Optiplex 3060 (8GB RAM)
- **Domain Controller:** Windows Server 2022, hosting AD DS for the domain `khoo.local`
- **Client:** Windows 11 Pro VM, provisioned via Proxmox (UEFI/OVMF, TPM 2.0 virtual device, VirtIO drivers)
- **Network:** Both VMs on the same bridged network (vmbr0), client configured to use the DC's IP as its DNS server

## Operational Execution

### VM Provisioning
- Created the Windows 11 VM in Proxmox using the Q35 machine type and OVMF (UEFI) BIOS, required for Windows 11's TPM and Secure Boot checks
- Added a virtual TPM 2.0 device
- Bypassed the Windows 11 4GB RAM installer minimum by temporarily allocating 4096MB during setup, then scaling back post-install to conserve host resources
- Skipped Microsoft account provisioning in favor of a local account, to keep the client in a clean state for domain join (avoiding any Azure AD/Entra enrollment conflicts)

### Domain Join
- Located the domain name via **Active Directory Users and Computers** on the DC (`khoo.local`)
- Initial join attempt failed with: *"An Active Directory domain controller for the domain could not be contacted."*
- **Root cause:** the client's DNS was not pointed at the domain controller, so it could not resolve the SRV records for `khoo.local` needed to locate the DC
- **Diagnosis:** used `nslookup khoo.local` from the client to confirm DNS resolution was failing, and ran `Get-ADDomain` on the DC to verify the domain configuration
- **Fix:** manually set the client's DNS server to the DC's IP address, then re-ran the domain join, which succeeded
- Verified success two ways: the computer object appeared in Active Directory Users and Computers, and a domain user account was used to log in directly on the client

### Credential Lifecycle Policy
- Configured a temporary default password for all initial user accounts (`Khoo2026!`), with **"User must change password at next logon"** enforced
- Post-first-login, users transition to individualized passwords following a `Khoo[FirstName]` convention (e.g. `KhooChelsea`)
- This models a basic real-world onboarding pattern: shared temp credentials for provisioning, forced rotation to reduce the window where a known default password is valid

## Troubleshooting Notes
| Issue | Cause | Resolution |
|---|---|---|
| Domain join failure | Client DNS not pointed at DC | Manually set DNS to DC IP address |
| Windows 11 install blocked | Installer enforces 4GB RAM minimum | Temporarily raised VM memory during install, reduced after |

## Next Steps
- Deploy a first Group Policy Object and validate application on the client
- Begin SIEM log correlation (Wazuh) using authentication events from this domain join and subsequent logons

