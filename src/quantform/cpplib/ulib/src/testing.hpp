#ifndef TESTING_HPP
#define TESTING_HPP


#include <vector>
#include <string>
#include <functional>
#include <chrono>
#include <exception>
#include <filesystem>

#include "../ulib.hpp"


namespace ulib {

  class TestSuite {

    protected:

      using testFunction = std::function<bool()>;

      // Struct for holding individual test info
      typedef struct {
        testFunction test;
        std::string submodule;
        std::string testname;
      } testStruct;

      // The list of function references
      std::vector<testStruct> testStructs;

      // The name of the test suite
      std::string testSuiteName = "undefined";


    public:

      // Default constructor. Leaves the name of the test suite undefined
      TestSuite(void) { }


      // Constructor that allows specifying the name of the test suite
      TestSuite(const std::string& name) {
        testSuiteName = name;
      }


      // Method for adding a function pointer to the test suite.
      bool addTest(testFunction function, std::string submodule = "undefined", std::string testname = "undefined") {

        testStruct newTest;

        newTest.test = function;
        newTest.submodule = submodule;
        newTest.testname = testname;

        testStructs.push_back(newTest);
        return true;
      }


      // Method that gives the number of tests currently in the suite
      int numTests() {
        return testStructs.size();
      }


      // Method for cleaning up tmp directory. Returns the number of files deleted
      int cleanTmpDir() {
        std::string protectedFile = std::filesystem::current_path().string() + "/tmp/README.md";
        std::string tmpPath = std::filesystem::current_path().string() + "/tmp";
        int nDeletedFiles = 0;

        for (const std::filesystem::directory_entry &fileEntry : std::filesystem::directory_iterator(tmpPath)) {
          std::string filePath = fileEntry.path().string();

          if ( filePath == protectedFile ) {
            continue;
          }

          if ( !std::filesystem::remove(filePath) ) {
            ERROR(formString("Could not delete file: ", filePath, "!"));
          }

          nDeletedFiles++;
        }

        return nDeletedFiles;
      }


      /* 
       * Method for running the tests in the test suite. 
       * Returns true if all tests pass, false otherwise
       */
      bool runTests(bool showTestInfo = false) {
        INFO(formString("Running tests for: ", testSuiteName));

        if ( this->numTests() == 0 ) {
          INFO("No tests defined");
          return true;
        }

        int countPassed = 0;
      
        for (int i = 0; i < this->numTests(); i++) {
          testStruct test_i = testStructs[i];
          bool passed;
          int milliseconds;

          std::string infoString = "";
          if ( showTestInfo ) {
            infoString = ulib::formString(" ", test_i.submodule, "|", test_i.testname);
          }

          try {
            const auto start = std::chrono::high_resolution_clock::now();
            passed = test_i.test();
            const auto end = std::chrono::high_resolution_clock::now();

            const auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
            milliseconds = (int)duration.count();
          }
          catch (std::exception& e) {  // Note, doesn't catch hardware exceptions like segmentation fault
            INFO(formString("Test ", i + 1, infoString, " - ERROR (", e.what(), ")\n"));
            continue;
          }

          if ( passed ) {
            countPassed++;
            INFO(formString("Test ", i + 1, infoString, " - PASSED (time taken ", milliseconds, " ms)"));
          }
          else {
            INFO(formString("Test ", i + 1, infoString, " - FAILED (time taken ", milliseconds, " ms)"));
          }
        }

        int nDeletedFiles = this->cleanTmpDir();
        LOWPRIORITY(ulib::formString("Deleted ", nDeletedFiles, " files from tmp directory"));

        return ( countPassed == this->numTests() );
      }


  };

}


#endif