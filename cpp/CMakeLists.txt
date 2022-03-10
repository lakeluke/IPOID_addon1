cmake_minimum_required(VERSION 3.5)

project(IPOID_addon1_cpp LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt5 COMPONENTS Core Gui Widgets REQUIRED)

set(DIR_INCLUDE include)
set(DIR_SRC src)
set(DIR_UI ui)
set(DIR_LIB lib)
set(CMAKE_AUTOUIC_SEARCH_PATHS ${DIR_UI})

file(GLOB HEADER_FILES "${DIR_INCLUDE}/*.h")
include_directories(BEFORE ${DIR_INCLUDE})
if(WIN32)
    include_directories(BEFORE ${DIR_INCLUDE}/win)
    link_directories(${DIR_LIB}/win)
elseif(APPLE)
    message(FATAL_ERROR "Apple MacOSX not supported")
elseif(UNIX)
    include_directories(BEFORE ${DIR_INCLUDE}/linux)
    link_directories(${DIR_LIB}/linux)
endif(WIN32)
aux_source_directory(${DIR_SRC} SRC_FILES)
set(PROJECT_SOURCES
    ${HEADER_FILES}
    ${SRC_FILES}
)
add_executable(${PROJECT_NAME} ${PROJECT_SOURCES})
target_link_libraries(${PROJECT_NAME} PRIVATE Qt5::Widgets Qt5::Core Qt5::Gui tobii_research)
