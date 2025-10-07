#include <string>
#include <vector>
#include <map>

#include "../ulib.hpp"


/**
 * Compile at the main src directory with: 
 * > g++ -std=c++17 -mavx -fopenmp -Wall ulib/tests/utility_tests.cpp -lm -o utility_tests.o
 * Run with: 
 * > ./utility_tests.o
 */



namespace internalUtilityTesting {

  // Test 1
  bool test_formString1() {
    std::string correctString = "Hello World!";
    std::string foundString = ulib::formString("Hello ", "World!");

    bool passed = (correctString == foundString);

    return passed;
  }


  // Test 2
  bool test_formString2() {
    std::string correctString = "1 + 1 = 2";
    std::string foundString = ulib::formString(1, " + ", 1, " = ", 2);

    bool passed = (correctString == foundString);

    return passed;
  }


  // Test 3
  bool test_numTokens1() {
    std::string testString = "   1  2  3  4  ";
    int correctNum = 4;
    int foundNum = ulib::numTokens(testString);

    bool passed = (correctNum == foundNum);

    return passed;
  }


  // Test 4
  bool test_numTokens2() {
    std::string testString = "|||1|2|3||4||";
    int correctNum = 4;
    int foundNum = ulib::numTokens(testString, '|');

    bool passed = (correctNum == foundNum);

    return passed;
  }


  // Test 5
  bool test_split1() {
    std::vector<std::string> correctVector = {"Hello", "World"};
    std::string testString = "   Hello   World";
    std::vector<std::string> foundVector = ulib::split(testString);

    bool passed = true;

    if ( correctVector.size() != foundVector.size() ) {
      passed = false;
    }

    for (int i = 0; i < (int)foundVector.size(); i++) {
      if ( correctVector[i] != foundVector[i] ) {
        passed = false;
      }
    }

    return passed;
  }


  // Test 6
  bool test_split2() {
    std::vector<std::string> correctVector = {"Hello", "World"};
    std::string testString = "|Hello||World|";
    std::vector<std::string> foundVector = ulib::split(testString, '|');

    bool passed = true;

    if ( correctVector.size() != foundVector.size() ) {
      passed = false;
    }

    for (int i = 0; i < (int)foundVector.size(); i++) {
      if ( correctVector[i] != foundVector[i] ) {
        passed = false;
      }
    }

    return passed;
  }


  // Test 7
  bool test_join1() {
    std::string correctString = "Hello World";
    std::vector<std::string> testVector = {"Hello", "World"};
    std::string foundString = ulib::join(testVector);

    bool passed = (correctString == foundString);

    return passed;
  }


  // Test 8
  bool test_join2() {
    std::string correctString = "Hello|World";
    std::vector<std::string> testVector = {"Hello", "World"};
    std::string foundString = ulib::join(testVector, '|');

    bool passed = (correctString == foundString);

    return passed;
  }


  // Test 9
  bool test_toLower() {
    std::string correctString = "hello world";
    std::string testString = "HelLO WoRLd";
    std::string foundString = ulib::toLower(testString);

    bool passed = (correctString == foundString);

    return passed;
  }


  // Test 10
  bool test_toUpper() {
    std::string correctString = "HELLO WORLD";
    std::string testString = "HelLO WoRLd";
    std::string foundString = ulib::toUpper(testString);

    bool passed = (correctString == foundString);

    return passed;
  }


  // Test 11
  bool test_trim1() {
    std::string correctString = "Hello World";
    std::string testString = "      Hello World   ";
    std::string foundString = ulib::trim(testString);

    bool passed = (correctString == foundString);

    return passed;
  }


  // Test 12
  bool test_trim2() {
    std::string correctString = "Hello World";
    std::string testString = "\t\tHello World\n";
    std::string foundString = ulib::trim(testString);

    bool passed = (correctString == foundString);

    return passed;
  }


  // Test 13
  bool test_mapKeys() {
    std::vector<int> correctVector = {1, 2, 3, 4};
    std::map<int, std::string> testMap = {{1, "Hello"}, {2, " "}, {3, "World"}, {4, "!"}};
    std::vector<int> foundVector = ulib::mapKeys(testMap);

    bool passed = true;

    if ( correctVector.size() != foundVector.size() ) {
      passed = false;
    }

    for (int i = 0; i < (int)foundVector.size(); i++) {
      if ( correctVector[i] != foundVector[i] ) {
        passed = false;
      }
    }

    return passed;
  }


  // Test 14
  bool test_mapVals() {
    std::vector<std::string> correctVector = {"Hello", " ", "World", "!"};
    std::map<int, std::string> testMap = {{1, "Hello"}, {2, " "}, {3, "World"}, {4, "!"}};
    std::vector<std::string> foundVector = ulib::mapVals(testMap);

    bool passed = true;

    if ( correctVector.size() != foundVector.size() ) {
      passed = false;
    }

    for (int i = 0; i < (int)foundVector.size(); i++) {
      if ( correctVector[i] != foundVector[i] ) {
        passed = false;
      }
    }

    return passed;
  }


  // Test 15
  bool test_ceil() {
    int correctInt = 3;
    int numerator = 5;
    int denominator = 2;
    int foundInt = ulib::ceil(numerator, denominator);

    bool passed = (correctInt == foundInt);

    return passed;
  }

}


namespace internalTesting {

  bool __addUtilityTests() {
    ulib::tests.addTest(internalUtilityTesting::test_formString1);
    ulib::tests.addTest(internalUtilityTesting::test_formString2);
    ulib::tests.addTest(internalUtilityTesting::test_numTokens1);
    ulib::tests.addTest(internalUtilityTesting::test_numTokens2);
    ulib::tests.addTest(internalUtilityTesting::test_split1);
    ulib::tests.addTest(internalUtilityTesting::test_split2);
    ulib::tests.addTest(internalUtilityTesting::test_join1);
    ulib::tests.addTest(internalUtilityTesting::test_join2);
    ulib::tests.addTest(internalUtilityTesting::test_toLower);
    ulib::tests.addTest(internalUtilityTesting::test_toUpper);
    ulib::tests.addTest(internalUtilityTesting::test_trim1);
    ulib::tests.addTest(internalUtilityTesting::test_trim2);
    ulib::tests.addTest(internalUtilityTesting::test_mapKeys);
    ulib::tests.addTest(internalUtilityTesting::test_mapVals);
    ulib::tests.addTest(internalUtilityTesting::test_ceil);

    return true;
  }

  bool utilityTestsAddedToTestSuite = __addUtilityTests();

}

/*
int main() {
  ulib::verbosity(5);
  ulib::tests.runTests();
}
*/