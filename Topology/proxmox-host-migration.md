# Proxmox Host Migration: Splitting the Homelab Across Two Hosts

## Executive Objective

The original homelab ran entirely on a Dell OptiPlex 3060 with only 7.6GB of usable RAM. This forced a workaround: the Windows Server 2022 domain controller and the Wazuh SIEM stack couldn't run at full allocation simultaneously, so the DC had to be shut down whenever the Wazuh dashboard needed full host resources for review. This writeup documents migrating the DC and a Windows 11 client VM off the OptiPlex and onto a second host (a G6 machine with 16GB RAM), freeing the OptiPlex to run Wazuh full-time and enabling both environments to run concurrently for realistic attack/defense and monitoring work.

## Architecture Topology

- **Host 1 (OptiPlex 3060):** Proxmox VE, 7.6GB usable RAM, 6 CPU threads. Runs the Wazuh manager/indexer/dashboard stack on a dedicated Ubuntu Server VM.
- **Host 2 (pve-g6):** Proxmox VE, 16GB RAM. Fresh install. Now hosts the Windows Server 2022 DC (VMID 200) and a Windows 11 client (VMID 400).
- Both hosts sit on the same LAN segment (192.168.4.x), connected through the existing Netgear GS108Tv3 switch and served by the GL.iNet Mango travel router in repeater mode.
- The two hosts are **not clustered**. A two-node Proxmox cluster carries split-brain risk since neither node can independently confirm quorum if the other drops. Running them as independent hosts on a shared LAN avoids that risk entirely, since no live migration or shared storage was needed for this migration.

## Operational Execution

1. **Backup on source host:** Used `vzdump` in snapshot mode with zstd compression to back up both VMs without downtime:
   ```
   vzdump 200 --storage local --mode snapshot --compress zstd
   vzdump 400 --storage local --mode snapshot --compress zstd
   ```
2. **Transfer:** Copied the resulting `.vma.zst` archives to pve-g6 over the LAN via `scp`, targeting `/var/lib/vz/dump/` on the destination.
3. **Restore on destination host:** Used `qmrestore` to rebuild both VMs on pve-g6, reusing the original VMIDs (200, 400) since the new host had no conflicting IDs:
   ```
   qmrestore /var/lib/vz/dump/vzdump-qemu-200-*.vma.zst 200
   qmrestore /var/lib/vz/dump/vzdump-qemu-400-*.vma.zst 400
   ```
   The restore mapped cleanly to the G6's default `local-lvm` storage pool with no manual intervention needed, and correctly recreated all three virtual devices for the Windows 11 VM (EFI disk, main disk, TPM state), preserving Secure Boot and TPM 2.0 requirements without reconfiguration.
4. **VirtIO drivers:** No manual driver reinstallation was needed. VirtIO drivers are installed inside the guest OS and are tied to the virtual hardware Proxmox presents (disk controller, NIC type), not the physical host. Since `vzdump`/`qmrestore` preserve the full VM hardware config alongside the disk image, both VMs booted with their existing drivers intact.

## Troubleshooting and Lessons Learned

| Issue | Cause | Resolution |
|---|---|---|
| `-bash: zvdump: command not found` | Typo (`zvdump` instead of `vzdump`) | Corrected command spelling |
| `qm start 400` failed: `volume 'local:iso/Win11_25H2_English_x64_v2.iso' does not exist` | The Windows 11 VM still had its original install ISO attached in the virtual CD-ROM drive; `vzdump` recorded the config reference but did not (and should not) copy the ISO itself | Detached the phantom CD-ROM: `qm set 400 --ide2 none,media=cdrom` |
| `swtpm_setup: Not overwriting existing state file` on `qm start 400` | Informational, not an error. TPM state from the backup was reused rather than regenerated | No action needed |

## Status / Next Steps

- Both VMs confirmed running on pve-g6.
- **Pending:** Update the Wazuh agent config (`ossec.conf`) on the DC to point to the OptiPlex's Wazuh manager IP, restart the agent service, and confirm the DC re-registers as an active agent in the dashboard.
- **Pending:** Set a DHCP reservation for the DC's new IP on the GL.iNet Mango to prevent future address drift.
- Once verified, the OptiPlex can be dedicated entirely to Wazuh, and the DC/client environment on the G6 can run continuously for live attack/defense testing without resource contention.
