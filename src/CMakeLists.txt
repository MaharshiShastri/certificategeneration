#CMakeLists for C++
# Set the minimum required version of CMake
cmake_minimum_required(VERSION 3.10)

# Define the project name
project(CertificateGeneration)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set the path to OpenCV (ensure these are static libraries, .a or .lib files)
set(OpenCV_DIR "D:\\opencv\\x64\\mingw\\lib")

# Prioritize static libraries
set(CMAKE_FIND_LIBRARY_SUFFIXES ".a" ".lib")

# Set OpenCV to use static libraries
set(OPENCV_STATIC ON)

# Find the OpenCV package
find_package(OpenCV REQUIRED COMPONENTS core imgproc highgui)

if (NOT OpenCV_FOUND)
    message(FATAL_ERROR "OpenCV not found. Please check the OpenCV_DIR path.")
endif()

# Set flags to statically link the runtime (if using MinGW or GCC)
if(MINGW)
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -static-libgcc -static-libstdc++ -static")
elseif(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /MT")  # Static CRT linking
endif()

# Add the executable for the example project
add_executable(example example.cpp)

# Link the OpenCV libraries and other dependencies
target_link_libraries(example ${OpenCV_LIBS} comdlg32 kernel32 msvcrt user32)

# Specify the DLLs to copy (replace these with actual paths if needed)
set(OPEN_CV_DLLS
    "D:/opencv/x64/mingw/bin/libopencv_core4100.dll"
    "D:/opencv/x64/mingw/bin/libopencv_highgui4100.dll"
    "D:/opencv/x64/mingw/bin/libopencv_imgcodecs4100.dll"
    "D:/opencv/x64/mingw/bin/libopencv_imgproc4100.dll"
)

# Additional system DLLs that need to be copied
set(SYSTEM_DLLS
    "C:/Windows/System32/comdlg32.dll"
    "C:/Windows/System32/kernel32.dll"
    "C:/Windows/System32/msvcrt.dll"
    "C:/Windows/System32/user32.dll"
)

# Copy the required DLLs to the build output directory
foreach(DLL ${OPEN_CV_DLLS} ${SYSTEM_DLLS})
    get_filename_component(DLL_NAME ${DLL} NAME)
    add_custom_command(TARGET example POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${DLL} $<TARGET_FILE_DIR:example>/${DLL_NAME}
    )
endforeach()
