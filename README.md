# REChain 🪐

Implementation of a <https://matrix.katya.wtf> node in Python based on the Katya ® 👽 Kit framework.

> **NOTE:** In 2019, we split our implementation of "REChain 🪐 Coin" from its development framework
> "Katya ® 👽 Kit".

This repo contains runtimes for the REChain 🪐 Coin network based on C++ & QT Technology. The README file provides
information about installing the `REChain 🪐 Coin` binary and developing on the codebase.

## Installation

### Building REChain 🪐 Coin (RecCoin)

See doc/readme-qt.rst for instructions on building reccoin-qt,
the intended-for-end-users, nice-graphical-interface, reference
implementation of RecCoin.

**NOTE:** /* See doc/build-*.txt for instructions on building REChain 🪐 Coin,
the intended-for-services, no-graphical-interface, reference
implementation of RecCoin. */

#### Building reccoin-qt

RecCoin 1.0

Copyright (c) 2009-2012 Bitcoin Developers
Copyright (c) 2011-2012 Litecoin Developers
Copyright (c) 2020 REChain
Copyright (c) 2019-2020 Dmitry Sorokin

Distributed under the MIT/X11 software license, see the accompanying
file COPYING or http://www.opensource.org/licenses/mit-license.php.
This product includes software developed by the OpenSSL Project for use in
the OpenSSL Toolkit (http://www.openssl.org/).  This product includes
cryptographic software written by Eric Young (eay@cryptsoft.com).


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
