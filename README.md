# REChain ®️ 🪐

Implementation of a <https://matrix.katya.wtf> node in Python based on the Katya ® 👽 Kit framework.

> **NOTE:** In 2019, we split our implementation of "REChain ®️ 🪐 Coin" from its development framework
> "Katya ® 👽 Kit".

This repo contains runtimes for the REChain ®️ 🪐 Coin network based on C++ & QT Technology. The README file provides
information about installing the `REChain ®️ 🪐 Coin` binary and developing on the codebase.

---

Repository reorganized:

To improve modularity and prepare for cross-platform builds, mesh networking and AI integration, a set of top-level
directories was added. These are scaffolds and do not yet replace existing build scripts; migration is incremental.

New top-level directories:
- `core/` — core libraries and public headers
- `frontend/` — UI code (Qt) and platform frontends
- `backend/` — daemons, CLI and server components
- `infra/` — build scripts, CMake toolchains and CI templates
- `ai/` — optional machine-learning modules (includes `ai_quantum_core` scaffold)
- `mesh/` — mesh networking overlay and related tools
- `docs/` — documentation and architecture guides
- `platforms/` — platform-specific scaffolds for Android, iOS, Web, etc.

See `docs/ARCHITECTURE.md` for the high-level refactor plan and guidelines.


Intro
-----
RecCoin is a free open source peer-to-peer electronic token system that is
completely decentralized, without the need for a central server or trusted
parties.  Users hold the crypto keys to their own money and transact directly
with each other, with the help of a P2P network to check for double-spending.


Setup
-----
You need the Qt4 run-time libraries to run reccoin-qt. On Debian or Ubuntu:
  sudo apt-get install libqtgui4

Unpack the files into a directory and run:
 bin/32/reccoin-qt (GUI, 32-bit)
 bin/32/reccoin (headless, 32-bit)
 bin/64/reccoin-qt (GUI, 64-bit)
 bin/64/reccoin (headless, 64-bit)
 .

Copyright © 2019-2024 Need help? 🤔 Donate US! ⌛️ For tea, coffee! For the future of decentralized and distributed internet. We do cool and, in my opinion, useful things for the safety and security of users' personal data. And on a completely non-commercial basis! 😎 Email us! 👇 A Dmitry Sorokin production. All rights reserved. Powered by REChain ®️. 🪐 Copyright © 2019-2024 REChain, Inc REChain ® is a registered trademark hr@adminmarina.ru p2p@adminmarina.ru pr@adminmarina.ru sorydima@adminmarina.ru support@adminmarina.ru sip@adminmarina.ru music@adminmarina.ru cfa@adminmarina.ru anti@adminmarina.ru mot_cfa@adminmarina.ru rechainstore@adminmarina.ru models@adminmarina.ru dex@adminmarina.ru email@adminmarina.ru musicdapp@adminmarina.ru pitomec@adminmarina.ru delus@adminmarina.ru gateway@adminmarina.ru husco@adminmarina.ru info@adminmarina.ru maring@adminmarina.ru modus@adminmarina.ru rechainnetworkhost@adminmarina.ru tanyacity@adminmarina.ru support@xn--90ao4a.tech Please allow anywhere from 1 to 5 business days for E-mail responses! 💌 Our Stats! 👀 At the end of 2023, the number of downloads from the Open-Source Places, Apple AppStore, Google Play Market, and the REChain.Store, namely the Domestic application store from the REChain ®️ brand 🪐, а именно Отечественный магазин приложений от бренда REChain ®️ 🪐 ✨ exceeded 29 million downloads. 😈 👀

