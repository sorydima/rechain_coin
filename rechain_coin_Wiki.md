
# rechain_coin Wiki

## Home
### Welcome to the rechain_coin Wiki!
The **rechain_coin** repository is a cryptocurrency project developed using **C**, **C++**, **Qt**, and **Python**. It implements core blockchain functionality, including decentralized transactions, wallet management, and secure peer-to-peer communication. This Wiki provides guidance for setting up, using, and contributing to the project.

---

## Getting Started
### Prerequisites
To set up and build the project, ensure you have the following installed:
1. **C++ Compiler**: GCC (Linux), Clang (macOS), or MSVC (Windows).
2. **Qt Framework**: Latest version for GUI development.
3. **Python**: Version 3.8 or above for scripting and API utilities.
4. **CMake**: For building the project.
5. **OpenSSL**: For secure communication.

### Installation
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

---

## Features
1. **Core Blockchain Functionality**
   - Decentralized ledger.
   - Peer-to-peer transaction validation.

2. **Wallet Management**
   - Generate, import, and manage cryptocurrency wallets.
   - Encryption of private keys.

3. **Qt-Based GUI**
   - Cross-platform user interface for interacting with the blockchain.

4. **Python APIs**
   - Python bindings for scripting blockchain operations.

---

## Architecture
### System Overview
The project follows a modular architecture:

1. **Core Blockchain Logic**:
   Written in **C/C++**, responsible for ledger management, transaction validation, and consensus.

2. **Qt GUI**:
   User interface for wallet operations and blockchain interactions.

3. **Python Scripts**:
   Used for automation and API integration.

4. **Networking Module**:
   Handles peer discovery, message routing, and encryption via OpenSSL.

---

## Usage Guide
### Running the GUI Application
1. Launch the compiled executable:
   ```bash
   ./rechain_coin
   ```

2. Features available in the GUI:
   - **Create Wallet**: Generate a new wallet.
   - **Send Coins**: Initiate transactions.
   - **Transaction History**: View past transactions.

### Using the Python API
1. Import the Python bindings:
   ```python
   from rechain_coin import BlockchainAPI
   api = BlockchainAPI()
   ```
2. Example: Create a new wallet:
   ```python
   wallet = api.create_wallet("password123")
   print(f"Wallet Address: {wallet['address']}")
   ```

3. Example: Send coins:
   ```python
   tx = api.send_coins(sender="wallet_address", recipient="recipient_address", amount=10.0)
   print(f"Transaction ID: {tx['id']}")
   ```

---

## Contributing
### How to Contribute
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Make your changes and build the project:
   ```bash
   cmake ..
   make
   ```
4. Test your changes:
   - Unit tests are located in the `tests` directory.
   ```bash
   ./run_tests
   ```
5. Submit a pull request.

### Code Style Guidelines
- **C++**: Follow the [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html).
- **Python**: Adhere to [PEP 8](https://pep8.org/).
- **Qt**: Use best practices for Qt GUI development.

---

## FAQ
1. **What is rechain_coin?**
   A cryptocurrency implementation using REChain Basis technology.

2. **Which platforms are supported?**
   Linux, macOS, and Windows.

3. **How do I report bugs?**
   Use the GitHub Issues tab.

4. **Can I integrate rechain_coin with other systems?**
   Yes, use the Python APIs for integration.

---

## Additional Resources
1. **Protocol Documentation**: [Protocol.md](#).
2. **Qt Documentation**: [Qt Framework](https://doc.qt.io/).
3. **Python APIs**: See the `python_api` directory in the repository.

