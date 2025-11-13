# Core

This directory is intended for core libraries and non-UI logic of the project (consensus, networking, storage, cryptography).

Mapping notes:
- Current `src/` contains C++ core implementation. During reorganization, copy or move stable core files here and update build scripts.
- Keep ABI and public headers stable to preserve backward compatibility.

Guidelines:
- Expose a small, well-documented public API in `core/include` and keep implementation in `core/src`.
- Add compatibility shims when refactoring internal APIs.