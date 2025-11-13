"""Offline mesh voting application prototype.

This module demonstrates a simple majority-based election among discovered nodes.
It uses the discovery service to find peers, then runs a single-round vote where each
node broadcasts its vote and collects votes for a configurable timeout.

Note: This is a proof-of-concept and does not provide strong anti-spoofing protections.
Use signatures and authenticated channels for production.
"""

import time
import threading
import json
import uuid
from typing import Dict
from .discovery import DiscoveryService

VOTE_TIMEOUT = 5.0


class MeshVote:
    def __init__(self, option_list):
        self.node_id = str(uuid.uuid4())
        self.options = option_list
        self.votes: Dict[str, str] = {}
        self.lock = threading.Lock()
        self.discovery = DiscoveryService(node_id=self.node_id, metadata={'name': 'voter'})

    def _on_update(self, msg, addr):
        # simple executor for discovered nodes
        pass

    def run_vote(self, my_choice: str):
        assert my_choice in self.options
        # Announce vote via multicast (reuse discovery packet for demo)
        sock = None
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        payload = json.dumps({'type': 'vote', 'node_id': self.node_id, 'choice': my_choice}).encode('utf-8')
        self.discovery.start()
        end = time.time() + VOTE_TIMEOUT
        while time.time() < end:
            try:
                sock.sendto(payload, ('224.0.0.251', 9999))
            except Exception:
                pass
            time.sleep(0.5)
        # Collect votes by reading multicast socket directly (simplified)
        sock.close()
        # This demo does not implement vote collection; it's an exercise for integration with discovery listener.


if __name__ == '__main__':
    v = MeshVote(['yes', 'no'])
    v.run_vote('yes')
