---
title: HP Pavilion - CachyOS Linux Configuration (saved)
created: 2025-12-06
---

# HP Pavilion — CachyOS Linux Configuration (Saved 2025-12-06)

**Host:** cachyhp
**Machine:** HP Pavilion (user-provided)
**Distro:** CachyOS (Arch-based)
**OS Release:**
```
NAME="CachyOS Linux"
PRETTY_NAME="CachyOS"
ID=cachyos
BUILD_ID=rolling
ANSI_COLOR="38;2;23;147;209"
HOME_URL="https://cachyos.org/"
DOCUMENTATION_URL="https://wiki.cachyos.org/"
SUPPORT_URL="https://discuss.cachyos.org/"
BUG_REPORT_URL="https://github.com/cachyos"
PRIVACY_POLICY_URL="https://terms.archlinux.org/docs/privacy-policy/"
LOGO=cachyos
LSB Version:    n/a
Distributor ID: cachyos
Description:    CachyOS
Release:        rolling
Codename:       n/a
```

**Kernel:**
```
Linux cachyhp 6.18.0-1-cachyos-bore-lto #1 SMP PREEMPT_DYNAMIC Sat, 06 Dec 2025 00:49:25 +0000 x86_64 GNU/Linux
```

**Bootloader:** Limine (user noted "I have limine installed (not Grub)")

## Context & Notes
- User asked for console/boot font adjustments and mentioned Limine; instructions for testing and persisting console font changes were prepared separately.
- This file captures the minimal OS/kernel/bootloader context for quick reference when troubleshooting or scripting for this machine.

## Saved actions & pointers
- See `GTD-Tasks/1-Next-Actions/increase-boot-terminal-font-size.md` for the Next Action entry created earlier.
- Limine config path (typical): `/boot/limine/limine.cfg` (if present on this system).
- Persistent console font (Arch/CachyOS): `/etc/vconsole.conf` and `mkinitcpio -P` were recommended to regenerate initramfs after changes.

## Useful commands to collect more hardware details (run locally and paste results into this file when available)
```fish
# Distro / kernel
cat /etc/os-release
uname -a

# Hardware summary (install inxi if needed)
sudo lspci -vnn
lsusb
sudo lsblk -f
# Optional: install and run inxi for a concise hardware summary
sudo pacman -S inxi
inxi -Fxxz
```

## Revert / recovery notes
- If console font changes cause problems, revert `/etc/vconsole.conf` from a backup and re-run `sudo mkinitcpio -P`.
- If Limine config was changed manually, keep `/boot/limine/limine.cfg.bak` as a backup and restore it if needed.

---

Saved by LifeOS assistant on 2025-12-06 for HP Pavilion `cachyhp` (CachyOS).
