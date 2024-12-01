
# rechain_coin - Cryptocurrency Project

The **rechain_coin** project is a cryptocurrency implementation using **C**, **C++**, **Qt**, and **Python**. It implements core blockchain functionality including decentralized transactions, wallet management, secure peer-to-peer communication, and more.

## Features
- Decentralized ledger and transaction validation.
- Wallet management and private key encryption.
- Cross-platform Qt-based GUI.
- Python APIs for scripting and automation.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sorydima/rechain_coin.git
   cd rechain_coin
   ```
2. Install dependencies:
   - On Debian/Ubuntu:
     ```bash
     sudo apt-get install build-essential qt5-default libssl-dev cmake python3
     ```
   - On macOS:
     ```bash
     brew install qt openssl cmake python
     ```
   - On Windows:
     Use **vcpkg** or manually download Qt and OpenSSL.

3. Build the project:
   ```bash
   mkdir build && cd build
   cmake ..
   make
   ```

4. Run the application:
   ```bash
   ./rechain_coin
   ```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License
This project is licensed under the [MIT License](LICENSE.md).
