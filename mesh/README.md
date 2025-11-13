# Mesh

Code and specifications for mesh networking, device discovery, and P2P overlay.

Mapping notes:
- Provide clear interfaces between `core/network` and `mesh` overlay.
- Add documentation and simulation scripts.

Mesh networking tools and protocols.

Files:
- `discovery.py` — UDP multicast discovery service (announcer + listener).
- `multicast_topology.json` — simple local storage of discovered nodes for quick testing.

Next steps:
- Add Bluetooth LE advertising relay with encryption.
- Add Wi-Fi Direct exchange helpers and a sync protocol implementation.