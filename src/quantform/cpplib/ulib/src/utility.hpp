#ifndef UTILITY_HPP
#define UTILITY_HPP


#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <map>
#include <cctype>

#include "logging.hpp"


namespace ulib {


  // Function that returns the used C++ standard
  inline std::string getcppStandard() {
    if (__cplusplus == 202101L) return "C++23";
    else if (__cplusplus == 202002L) return "C++20";
    else if (__cplusplus == 201703L) return "C++17";
    else if (__cplusplus == 201402L) return "C++14";
    else if (__cplusplus == 201103L) return "C++11";
    else if (__cplusplus == 199711L) return "C++98";
    else return "C++??";
  }

  /*
   * Function that forms a string from the given (arbitrary) arguments. Note that the function
   * does not add any whitespaces so these are up to the user. Should not be mistaken with _join function
   */
  template<class... Args>
  std::string formString(Args... args) {
    std::ostringstream msg;
    (msg << ... << args);

    return msg.str();
  }


  /*
   * Function that counts the number of tokens in a string as divided by a delimeter.
   * Default delimeter is space ' '. Doesn't count empty strings as tokens
   */
  inline int numTokens(const std::string& str, char delim=' ') {
    std::istringstream stream(str);
    std::string token;
    int count = 0;

    while (std::getline(stream, token, delim)) {
      if (token != "") {
        count++;
      }
    }

    return count;
  }


  /*
   * Function that splits a string by a wanted delimeter.
   * Default delimeter is space ' '. Doesn't count empty strings as tokens
   */ 
  inline std::vector<std::string> split(const std::string& str, char delim=' ') {
    std::istringstream stream(str);
    std::string token;

    std::vector<std::string> ret;

    while (std::getline(stream, token, delim)) {
      if (token != "") {
        ret.push_back(token);
      }
    }

    return ret;
  }


  // Function that joins multiple strings together by a delimeter. Default delimeter is space ' '
  inline std::string join(const std::vector<std::string> strs, char delim=' ') {
    std::ostringstream stream;

    for (const std::string str : strs) {
      stream << delim << str;
    }

    return stream.str();
  }


  // Convert a given string to lowercase
  inline std::string toLower(const std::string& str) {
    std::string ret;
    ret.reserve(str.size());
    for (int i = 0; i < (int)str.size(); i++) {
      char c = (char)tolower(str[i]);
      ret.push_back(c);
    }

    return ret;
  } 


  // Convert a given string to uppercase
  inline std::string toUpper(const std::string& str) {
    std::string ret;
    ret.reserve(str.size());
    for (int i = 0; i < (int)str.size(); i++) {
      char c = (char)toupper(str[i]);
      ret.push_back(c);
    }

    return ret;
  } 


  // Remove leading and trailing whitespaces from a string
  inline std::string trim(const std::string& str) {

    if (str == "") {
      ERROR("Cannot trim an empty string!");
    }

    // Find the index of the first non-whitespace character
    int start = -1;
    for (int i = 0; i < (int)str.size(); i++) {
      if (!isspace(str[i])) {
        start = i;
        break;
      } 
    }

    if (start == -1) {
      WARNING("Whitespace string trimmed!");
      return "";
    }

    // Find the index of the last non-whitespace character
    int end;
    for (int i = (int)str.size() - 1; i >= 0; i--) {
      if (!isspace(str[i])) {
        end = i;
        break;
      } 
    }

    return str.substr(start, end - start + 1);
  }


  // Template function that retrieves all keys in a std::map
  template<class keyType, class valueType>
  std::vector<keyType> mapKeys(std::map<keyType, valueType> map) {
    std::vector<keyType> ret;
    for (const auto& [key, val] : map) {
        ret.push_back(key);
    }

    return ret;
  }


  // Template function that retrieves all values in a std::map
  template<class keyType, class valueType>
  std::vector<valueType> mapVals(std::map<keyType, valueType> map) {
    std::vector<valueType> ret;
    for (const auto& [key, val] : map) {
        ret.push_back(val);
    }

    return ret;
  }


  // Function for "dividing up" two integers
  inline int ceil(int a, int b) {
    return (a + b - 1) / b;
  }


  // Function for reading the last line of a given text file
  // Inspired by: https://stackoverflow.com/questions/11876290/c-fastest-way-to-read-only-last-line-of-text-file
  inline std::stringstream lastLine(const std::string& filepath) {
    std::ifstream _file(filepath);

    if ( !_file ) {
      ERROR("Couldn't open the given file!");
    }

    char c;
    _file.seekg(-1, std::ios_base::end);  // Go to last non EOF char

    _file.get(c);

    if ( c == '\n' ) {  // File ends with a newline char. Ignore it
      _file.seekg(-2, std::ios_base::cur);
      _file.get(c);
    }

    bool cont = true;
    while ( cont ) {

      if ( c == '\n' ) {  // End of the last line found
        _file.seekg(1, std::ios_base::cur);
        cont = false; 
      }

      // Continue
      _file.seekg(-2, std::ios_base::cur);
      _file.get(c);
    }

    std::string lastLine;
    std::getline(_file, lastLine);

    std::stringstream ret(lastLine);

    _file.close();

    return ret;
  }

}


#endif