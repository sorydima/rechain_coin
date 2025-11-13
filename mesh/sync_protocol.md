Mesh Sync Protocol — draft

Goals:
- Efficiently synchronize data between nodes that were offline and rejoin the network.
- Minimize bandwidth and avoid conflicts via vector clocks and per-resource causal histories.

Key concepts:
1. Node identity and vector clocks
   - Every node maintains a stable node_id and a local counter.
   - Each shared object has a version vector (map node_id -> counter).

2. Gossip exchange
   - On reconnect, nodes perform a handshake exchanging digests: list of (object_id, version_vector)
   - Missing/older objects are requested. Conflicts are resolved via application-specific merge or CRDTs.

3. Chunked transfer and resumability
   - Large objects are transferred as chunked blobs with checksums; incomplete transfers can be resumed.

4. Security
   - All sync messages are authenticated (HMAC) and optionally encrypted.
   - Use session keys negotiated via ECDH between nodes.

5. Recovery and tombstones
   - Deletions are tombstoned with version vectors to prevent resurrection of deleted objects.

6. Offline consensus
   - For critical shared state, use majority-agreement within the discovered mesh or delegated leaders.

Message types:
- HELLO { node_id, capabilities, summary_hash }
- DIGEST { object_id, version_vector }
- REQUEST { object_id, chunk_index }
- CHUNK { object_id, chunk_index, data, checksum }
- ACK

Conflict handling:
- Prefer CRDTs for high-availability mutable state (sets, maps, counters).
- For non-CRDT state, require application-level merge or present conflict to user.

Next steps:
- Implement a prototype in Python using asyncio with optional uTP/UDP transport and ECDH session keys.
