cmake_minimum_required(VERSION 3.16)
project(rechain_qt)

find_package(Qt5 COMPONENTS Widgets REQUIRED)

option(RECHAIN_USE_FRONTEND_QT_DIR "Use sources in frontend/qt instead of src/qt" OFF)

if(RECHAIN_USE_FRONTEND_QT_DIR AND EXISTS "${CMAKE_SOURCE_DIR}/frontend/qt")
    set(QT_SRC_DIR "${CMAKE_SOURCE_DIR}/frontend/qt")
else()
    set(QT_SRC_DIR "${CMAKE_SOURCE_DIR}/src/qt")
endif()

message(STATUS "Using Qt sources from: ${QT_SRC_DIR}")

# Collect UI sources from the chosen directory
file(GLOB QT_SOURCES "${QT_SRC_DIR}/*.cpp")
file(GLOB QT_HEADERS "${QT_SRC_DIR}/*.h")
file(GLOB QT_FORMS "${QT_SRC_DIR}/forms/*.ui")
file(GLOB QT_RES "${QT_SRC_DIR}/res/*")

add_executable(rechain-qt ${QT_SOURCES} ${QT_HEADERS})

target_include_directories(rechain-qt PRIVATE ${QT_SRC_DIR})

target_link_libraries(rechain-qt PRIVATE Qt5::Widgets)
