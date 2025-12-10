---
title: Increase Linux Boot Terminal Font Size
context: @Computer
priority: Medium
---
Next Action: Test increasing boot-time console font size. Steps:
1. Test `setfont` while in a virtual console.
2. If using `grub`, adjust `GRUB_GFXMODE`/`GRUB_GFXPAYLOAD_LINUX` or install a larger console font and update initramfs.
3. Persist changes and reboot to verify.

Notes: If you want, I can prepare the exact commands for your distro; tell me which Linux distribution/version you're using.
