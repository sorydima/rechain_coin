cmake_minimum_required(VERSION 3.16)
project(rechain_coin)

option(RECHAIN_USE_FRONTEND_QT_DIR "If ON, CMake will prefer sources under frontend/qt over src/qt" OFF)

# Configure known subprojects
add_subdirectory(core)
add_subdirectory(frontend)
add_subdirectory(backend)

# Provide a top-level target for convenience
add_custom_target(build_all DEPENDS rechain-qt)
