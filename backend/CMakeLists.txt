cmake_minimum_required(VERSION 3.16)
project(rechain_backend)

# Placeholder backend CMake. Move server/daemon source files here.
add_library(rechain_backend STATIC)

target_include_directories(rechain_backend PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
