cmake_minimum_required(VERSION 3.16)
project(rechain_coin)

# Root CMake that delegates to infra which contains the high-level orchestration
add_subdirectory(infra)

# Optionally allow selecting frontend source directory via cache variable
# To build with sources moved to frontend/qt, pass -DRECHAIN_USE_FRONTEND_QT_DIR=ON to cmake
