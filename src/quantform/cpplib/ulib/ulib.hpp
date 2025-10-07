#ifndef ULIB_HPP
#define ULIB_HPP


#include <filesystem>
#include <vector>
#include <string>


/*
 * This is the file one should include when using ulib functions
 */


// Include the SIMD specific utility functions
#include "src/simd.hpp" 


// Include the logging specific utility functions
#include "src/logging.hpp" 


 // Include the basic utility functions
#include "src/utility.hpp" 


// Include the testing specific utility functions
#include "src/testing.hpp" 



namespace ulib {

  /*
   * Function that defines and returns the path to the log file. If no path for a logfile is passed it will 
   * not change the stdout. In such cases the the function just returns the string "stdout".
   */
  inline std::string logfile(const std::string& _logfilePath = "") {
    static bool firstCall = true;
    std::string logfilePath = "undefined";

    if ( firstCall ) {
      firstCall = false;

      if ( logfilePath == "" ) {
        logfilePath = "stdout";
        return logfilePath;
      }

      // Check if the directory in which the log is to be stored exists. If not create it
      std::vector<std::string> path_vector = split(_logfilePath, '/');
      std::string dir_path = join(std::vector<std::string>(path_vector.begin(), path_vector.end() - 1), '/');
      DEBUG(dir_path);
      
      //if ( !std::filesystem::exists(dir_path) ) {
      //  std::filesystem::create_directories(dir_path);
      //}

      // Write output into a log file
      freopen(_logfilePath.c_str(), "w", stdout);

      logfilePath = _logfilePath;
    }

    return logfilePath;
  }


  // Define the test suite here for ease of access
  TestSuite tests = TestSuite("ulib");

}

#endif