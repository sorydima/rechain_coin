# Architecture Proposal — System Refactor

Goals:
- Preserve backward compatibility of public ABI and CLI/RPC.
- Separate concerns: core (consensus, storage, crypto), backend (daemons, RPC), frontend (UI), infra (build/CI), ai, mesh, docs.
- Make cross-platform targets first-class and prepare for mesh overlay and userver backend.

High-level recommendations:
1. Core/module boundaries
   - Create `core/include` for stable public headers and `core/src` for implementation.
   - Provide C API shims for any public symbols that may be used by plugins or external tooling.

2. Backend
   - Move long-running daemons and CLI tools to `backend/` with a clear `backend/bin` layout.
   - Add `backend/api` for userver-based services (HTTP/gRPC) for metadata, telemetry, and management.

3. Frontend
   - Isolate Qt UI in `frontend/qt`. Keep resources and translations local to the UI project.
   - Add platform-specific frontends under `frontend/{android,ios,web}` as required.

4. Infra
   - Centralize CMake toolchains and cross-compile scripts in `infra/`.
   - Add CI templates for building Qt/UI and core libraries across platforms.

5. Mesh and AI
   - Provide `mesh/` as an overlay implementation that interacts with `core/network` via a defined interface.
   - Keep `ai/` optional and out of core build; provide Python modules and Dockerized training environments.

Compatibility strategies:
- Maintain public header layout and provide deprecation headers when refactoring internals.
- Use compatibility wrappers for any exported functions whose signatures change.
- Add integration tests in `infra/tests` that exercise the public CLI and RPC surface.

Migration plan (small incremental steps):
1. Create top-level directories and move UI sources to `frontend/qt` (or create symlinks) — do not change include paths yet.
2. Add `core/include` and re-export public headers via `core/public.h`.
3. Introduce CMake targets for `core` and `frontend` and make old build scripts depend on them.
4. Migrate backend binaries to `backend/` and add userver integration in a new `backend/api` module.
5. Add mesh overlay and AI module as optional packages.

Next actions (automatable):
- Generate scaffold directories and helper scripts (move steps, CI templates).
- Add skeleton `ai_quantum_core` Python package for experimentation.
- Create top-level `CMakeLists.txt` referencing `core/`, `frontend/` and `backend/` targets.

Implemented changes in this refactor:
- Added `core/include/rechain_core.h` and `core/src/core_stub.c` to expose a stable C API shim.
- Added `core/CMakeLists.txt` to build `rechain_core` library and install headers.
- Added `frontend/qt/CMakeLists.txt` which can use sources from `src/qt` or `frontend/qt` via option.
- Migrated `src/qt` to `frontend/qt` with backup script and added migration helpers in `infra/scripts/`.
- Added `mesh/` prototypes: discovery, BLE packer, Wi-Fi Direct stubs, voting prototype, and sync protocol.
- Added `ai/ai_quantum_core` scaffold with model and training harness.
- CI workflow (GitHub Actions) skeleton added under `infra/ci/github-workflows/ci.yml`.
- Backend userver stub added at `backend/api/userver_stub.py`.

Platform Builder plan (next):
- Generate platform folders under `frontend/{android,ios,macos,windows,linux,web}` with starter projects and build scripts.
- Add Flutter templates if mobile/web frontends chosen.

Cross-compile plan (next):
- Provide toolchain files for CMake under `infra/toolchains/` for cross-compiling to Android/iOS/Windows.
- Add example `CMakePresets.json` and Docker-based cross-build environments.

Quantum Core plan (next):
- Provide a pip-installable `ai/ai_quantum_core` package and examples for graph-based training.