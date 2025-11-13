# Frontend

UI code, desktop Qt application, and platform-specific frontends.

Mapping notes:
- `src/qt` contains existing Qt UI — move it to `frontend/qt`.
- Keep forms and resources under `frontend/qt/res` and use `frontend/qt/CMakeLists.txt` to build the UI.