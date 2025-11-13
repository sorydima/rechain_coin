Qt frontend notes:
- CMake target `rechain-qt` created in `frontend/qt/CMakeLists.txt`.
- To build with moved sources, pass `-DRECHAIN_USE_FRONTEND_QT_DIR=ON` to CMake.
- Keep UI resources under `frontend/qt/res` and translations under `frontend/qt/locale`.