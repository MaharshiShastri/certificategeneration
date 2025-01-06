#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <windows.h>
#include <commdlg.h>
#include <thread>
#include <mutex>

int point1x = 100, point1y = 100, point2x = 200, point2y = 200;
bool startGeneration = false;
std::mutex imageMutex; // Mutex for thread-safe image access

void onMouse(int event, int x, int y, int, void* userdata) {
    if (event == cv::EVENT_LBUTTONDOWN) {
        startGeneration = true;
    }
}

std::string openFileDialog(const std::string& message) {
    // Display the message in dialog box
    MessageBox(NULL, message.c_str(), "File Selection", MB_OK);
    // Buffer to store the file path
    char filename[MAX_PATH] = "";

    // Initialize the OPENFILENAME structure
    OPENFILENAME ofn;
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = NULL;
    ofn.lpstrFilter = "All Files\0*.*\0Text Files\0*.TXT\0";
    ofn.lpstrFile = filename;
    ofn.nMaxFile = MAX_PATH;
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;

    if (GetOpenFileName(&ofn)) {
        return std::string(filename);
    } else {
        std::cerr << "No file selected." << std::endl;
        return "";
    }
}

void draw_rectangle(cv::Mat& resizeImage) {
    cv::Mat tempImage = resizeImage.clone();
    cv::rectangle(tempImage, cv::Point(point1x, point1y), cv::Point(point2x, point2y), cv::Scalar(255, 0, 0), 2);
    cv::imshow("Editor", tempImage);
}

// Function to process a single row (multithreading function)
void processRow(const std::vector<std::string>& row, cv::Mat resizeImage, const std::string& outputPath) {
    for (const auto& col : row) {
        if (col == "Name") continue;

        // Lock the mutex to safely access the shared image
        std::lock_guard<std::mutex> lock(imageMutex);

        // Save image with text inside rectangle
        cv::Mat tempImage = resizeImage.clone();
        int centrex = (point1x + point2x) / 2;
        cv::putText(tempImage, col, cv::Point(centrex - 10, point2y), cv::FONT_HERSHEY_COMPLEX, 1.0, cv::Scalar(0, 0, 0), 2);

        std::stringstream ss;
        ss << outputPath << "\\" << col << ".jpg";
        std::string outputImage = ss.str();
        cv::imwrite(outputImage, tempImage);
        std::cout << "Saved: " << outputImage << std::endl;
    }
}

int main() {
    // Load and resize the base image
    std::string image_file = openFileDialog("Select the base certificate");
    cv::Mat image = cv::imread(image_file);
    if (image.empty()) {
        std::cerr << "Error loading image!" << std::endl;
        return -1;
    }
    double height = 0.5, width = 0.5;
    cv::Mat resizeImage;
    cv::Size newSize(image.cols * height, image.rows * width);
    cv::resize(image, resizeImage, newSize);

    // Open the CSV file
    std::string selectedFile = openFileDialog("Select the CSV");
    std::ifstream file(selectedFile);
    if (!file.is_open()) {
        std::cerr << "Error opening file!" << std::endl;
        return -1;
    }

    // Set rectangle location using trackbars
    cv::namedWindow("Editor", cv::WINDOW_AUTOSIZE);
    cv::createTrackbar("x1", "Editor", &point1x, resizeImage.cols);
    cv::createTrackbar("y1", "Editor", &point1y, resizeImage.rows);
    cv::createTrackbar("x2", "Editor", &point2x, resizeImage.cols);
    cv::createTrackbar("y2", "Editor", &point2y, resizeImage.rows);
    cv::setMouseCallback("Editor", onMouse);

    // Wait until left mouse click to start certificate generation
    while (!startGeneration) {
        draw_rectangle(resizeImage);
        char key = cv::waitKey(1);
        if (key == 27) { // Escape button
            std::cout << "Cancelled by user!" << std::endl;
            return 0;
        }
    }

    // Process CSV file
    std::string line;
    std::vector<std::thread> threads;
    std::string outputPath = openFileDialog("Select output directory"); // Output directory
    while (std::getline(file, line)) {
        std::istringstream ss(line);
        std::string token;
        std::vector<std::string> row;

        while (std::getline(ss, token, ',')) {
            row.push_back(token);
        }

        // Launch a new thread for each row
        threads.emplace_back(processRow, row, resizeImage, outputPath);
    }

    // Join all threads
    for (auto& thread : threads) {
        if (thread.joinable()) {
            thread.join();
        }
    }

    file.close();
    cv::destroyAllWindows();
    std::cout << "All certificates have been generated!" << std::endl;
    return 0;
}

