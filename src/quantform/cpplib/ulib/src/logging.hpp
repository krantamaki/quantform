#ifndef LOGGING_HPP
#define LOGGING_HPP


#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <filesystem>

#include "../ulib.hpp"


#ifndef BASE_VERBOSITY
  #define BASE_VERBOSITY 3
#endif


// Define macros for easier usage of the logging functions

// For error messages
#ifndef ERROR
  #define ERROR(msg) { ulib::_errorMsg(msg, __FILE__, __PRETTY_FUNCTION__, __LINE__); }  // Note that __PRETTY_FUNCTION__ macro is GCC specific
#endif

// For warning messages
#ifndef WARNING
  #define WARNING(msg) { ulib::_warningMsg(msg, __func__); }
#endif

// For info messages
#ifndef INFO
  #define INFO(msg) { ulib::_infoMsg(msg, __func__); }
#endif

// For low priority information
#ifndef LOWPRIORITY
  #define LOWPRIORITY(msg) { ulib::_lowPriorityMsg(msg, __func__); }
#endif

// For debugging information
#ifndef DEBUG
  #define DEBUG(msg) { ulib::_debugMsg(msg, __func__); }
#endif


namespace ulib {

  /*
   * Function that defines and returns the verbosity level
   * Note that verbosity will have 5 levels:
   *   1: Error messages
   *   2: 1 and warning messages
   *   3: 2 and base info messages
   *   4: 3 and low priority info messages
   *   5: Everything (i.e. 4 and debug messages)
   * If an improper level is passed will default to level 5
   */
  inline int verbosity(int _verbosity = BASE_VERBOSITY) {
    static bool firstCall = true;
    static int set_verbosity = BASE_VERBOSITY;

    if ( firstCall ) {
      firstCall = false;

      if ( _verbosity < 0 || _verbosity > 5 ) {
        set_verbosity = 5;
        return set_verbosity;
      }
      set_verbosity = _verbosity;
    }

    return set_verbosity;
  }


  // Function that generates and throws a more descriptive error message
  inline void _errorMsg(const std::string& msg, const char* file, const char* func, int line) {
    std::ostringstream msgStream;

    msgStream << "\n" << "ERROR: In file " << file << " at function " << func << " on line " << line << " : " << msg;
    std::string msgString = msgStream.str();
    std::cout << msgString << "\n\n" << std::endl;

    throw std::runtime_error(msgString);
  }


  // Function that forms and prints a warning message
  inline void _warningMsg(const std::string& msg, const char* func, bool always_print=false) {
    if (always_print) {
      std::cout << func << ": " << "WARNING! " << msg << std::endl;
    }

    if (verbosity() > 1) {
      std::cout << func << ": " << "WARNING! " << msg << std::endl;
    }
  }


  // Function that forms and prints an information message
  inline void _infoMsg(const std::string& msg, const char* func, bool always_print=false) {
    if (always_print) {
      std::cout << func << ": " << msg << std::endl;
      return;
    }
    if (verbosity() > 2) {
      std::cout << func << ": " << msg << std::endl;
    }
  }


  // Function that forms and prints a low priority info message
  inline void _lowPriorityMsg(const std::string& msg, const char* func) {
    if (verbosity() > 3) {
      std::cout << func << ": " << msg << std::endl;
    }
  }


  // Function that forms and prints a debug info message
  inline void _debugMsg(const std::string& msg, const char* func) {
    if (verbosity() > 4) {
      std::cout << func << ": " << "DEBUG - " << msg << std::endl;
    }
  }


}


#endif