#ifndef VECTOR_HPP
#define VECTOR_HPP

#include <vector>
#include <cmath>
#include <fstream>
#include <functional>

#include "../lalib.hpp"
#include "Matrix.hpp"


namespace lalib {


  /*
   * Dense vector implementation. Doesn't differentiate between row and column vectors
   */
  template <class val_t>
  class Vector {

    protected:

      // Alias for the vectorized type
      using vect_t = decltype(ulib::choose_simd<val_t, true>());


      // The number of elements in the SIMD vector
      int vectSize = SIMD_SIZE / (int)sizeof(val_t);


      // Const function that sums together the elements in a SIMD vector
      inline const val_t _reduce(const vect_t vect) const {
        val_t ret = (val_t)0.;
        for (int i = 0; i < vectSize; i++) {
          ret += vect[i];
        }

        return ret;
      }


      // Const function that fills the SIMD vector with wanted value
      inline const vect_t _fill(const val_t val) const {
          vect_t ret;
          for (int i = 0; i < vectSize; i++) {
            ret[i] = val;
          }

          return ret;
      }


      // Define a vector of zeros and the zero value
      val_t zeroVal = (val_t)0.;
      vect_t zeroVect = this->_fill(zeroVal);


      // The array of SIMD vectors
      std::vector<vect_t> values;


      // Define additional needed variables
      int totalVectCount = 0;
      int nElems = 0;


      // Const function for finding the correct vector index for a given matrix index
      inline const int _vectIndex(int normalIndex) const {
        return normalIndex / vectSize;
      }


      // Const function for finding the correct vector element for a given matrix index
      inline const int _vectElem(int normalIndex) const {
        return normalIndex % vectSize;
      }


      // Const function that returns a vector with value at given index and rest zeros
      inline const vect_t _valueVect(int vectElem, val_t value) const {
        vect_t newVect = zeroVect;
        newVect[vectElem] = value;

        return newVect;
      }


      // SIMD vector comparison function
      inline const bool _vectEq(vect_t vect1, vect_t vect2) const {

        for (int vectElem = 0; vectElem < this->vectSize; vectElem++) {
          if ( vect1[vectElem] != vect2[vectElem] ) {
            return false;
          }
        }
    
        return true;
      }


    public:


      // ====================== CONSTRUCTORS ======================


      // Default constructor
      Vector(void) { }


      // Copying constructor
      Vector(const Vector<val_t>& that) {

        if ( that.nElems < 1 ) {
          ERROR("Vector length must be positive!");
        }

        this->nElems = that.nElems;
        this->totalVectCount = that.totalVectCount;
 
        this->values = that.values;
      }


      // Zeros constructor
      Vector(int nElems) {

        if ( nElems < 1 ) {
          ERROR("Vector length must be positive!");
        }

        this->nElems = nElems;
        this->totalVectCount = ulib::ceil(nElems, vectSize);
        this->values = std::vector<vect_t>(this->totalVectCount, zeroVect);
      }


      // Default value constructor
      Vector(int nElems, val_t value) {

        if ( nElems < 1 ) {
          ERROR("Vector length must be positive!");
        }

        this->nElems = nElems;
        this->totalVectCount = ulib::ceil(nElems, vectSize);
        this->values = std::vector<vect_t>(this->totalVectCount, this->_fill(value));
      }


      // Vector copying constructor
      Vector(int nElems, std::vector<val_t>& elems) {

        if ( nElems < 1 ) {
          ERROR("Vector length must be positive!");
        }
          
        if ( nElems != (int)elems.size() ) {
          ERROR("Given dimensions don't match with the size of the std::vector!");
        }

        this->nElems = nElems;
        this->totalVectCount = ulib::ceil(nElems, vectSize);

        for (int vectIndex = 0; vectIndex < this->totalVectCount; vectIndex++) {
          vect_t vect = zeroVect;

          for (int vectElem = 0; vectElem < vectSize; vectElem++) {
            int arrIndex = vectIndex * vectSize + vectElem;
            vect[vectElem] = elems[arrIndex];
          }

          this->values.push_back(vect);
        }
      }


      // SIMD vector copying constructor
      Vector(int nElems, std::vector<vect_t>& elems) {

        if ( nElems < 1 ) {
          ERROR("Vector length must be positive!");
        }
        // TODO: Add other checks

        this->nElems = nElems;
        this->totalVectCount = ulib::ceil(nElems, vectSize);
        this->values = elems;
      }


      /*
       * Load from file constructor
       * Assumes that the values are whitespace separated as <index val>
       */
      Vector(const std::string& path, int offset = 0) {

        // Variables to read the line contents to
        int index;
        val_t val;
        
        // Open the file
        std::ifstream file(path);

        if ( !file ) {
          ERROR("Couldn't open the given file!");
        }

        // Read the last line of the file to get the dimensions of the matrix
        std::stringstream lastLine = ulib::lastLine(path);
        int nTokens = ulib::numTokens(lastLine.str());

        if ( nTokens != 2 ) {
          ERROR("File of an invalid format given!");
        }

        lastLine >> index >> val;
        
        this->nElems = index - offset + 1;
        this->values = std::vector<vect_t>(this->nElems, zeroVect);
        this->totalVectCount = ulib::ceil(this->nElems, this->vectSize);

        while (file >> index >> val) {
          this->place(index - offset, val);
        }

        file.close();
      }


      // ====================== PLACEMENT METHODS ======================


      // Single value placement
      void place(int index, val_t value) {

        int indexOffsetted = index - INDEX_OFFSET;

        if ( indexOffsetted < 0 || indexOffsetted >= this->nElems ) {
          ERROR(ulib::formString("Index ", index," out of bounds on a vector of length ", this->nElems,"!"));
        }

        this->values[this->_vectIndex(indexOffsetted)][this->_vectElem(indexOffsetted)] = value;
      }


      // SIMD placement
      void place(int vectIndex, vect_t vect) {

        if ( vectIndex < 0 || vectIndex >= this->totalVectCount ) {
          ERROR(ulib::formString("SIMD vector index ", vectIndex," out of bounds on a vector of length ", this->nElems,"!"));
        }

        this->values[vectIndex] = vect;
      }


      // ====================== ACCESSING METHODS ======================


      // Accessing method. Note the use of round brackets
      val_t operator() (int index) const {
        
        int indexOffsetted = index - INDEX_OFFSET;

        if ( indexOffsetted < 0 || indexOffsetted >= this->nElems ) {
          ERROR(ulib::formString("Index ", index," out of bounds on a vector of length ", this->nElems,"!"));
        }

        return this->values[this->_vectIndex(indexOffsetted)][this->_vectElem(indexOffsetted)];
      }


      // SIMD accessing method
      vect_t getSIMD(int vectIndex) const {

        if ( vectIndex < 0 || vectIndex >= this->totalVectCount ) {
          ERROR(ulib::formString("SIMD vector index ", vectIndex," out of bounds on a vector of length ", this->nElems,"!"));
        }

        return this->values[vectIndex];
      }


      // Function for slicing a subset of the vector. Exclusive from the end
      const Vector slice(int start, int end) const {
        
        int startOffsetted = start - INDEX_OFFSET;
        int endOffsetted = end - INDEX_OFFSET;

        if ( startOffsetted > endOffsetted ||
             startOffsetted < 0            ||
             endOffsetted > this->nElems ) {
          ERROR(ulib::formString("Given bounds ", start, " and ", end, " are out of bounds for a vector of length ", this->nElems, "!"));
        }

        std::vector<val_t> newValues = std::vector<val_t>(end - start, this->zeroVal);

        for (int i = startOffsetted; i < endOffsetted; i++) {
          newValues[i] = this->operator() (i + INDEX_OFFSET);
        }

        Vector<val_t> ret = Vector<val_t>(end - start, newValues);

        return ret;
      }


      // ====================== BASIC OPERATORS ======================


      // Assignment operator
      Vector& operator= (const Vector& that) {
        // Check for self-assignment ie. case where a = a is called by comparing the pointers of the objects
        if ( this == &that ) return *this;

        this->values = that.values;
        this->totalVectCount = that.totalVectCount;
        this->nElems = that.nElems;

        return *this;
      }


      // Equality comparison operator
      bool operator== (const Vector& that) {
        if ( this->nElems != that.nElems ) return false;

        for (int i = 0; i < this->nElems; i++) {
          if (this->operator() (i) != that(i)) {
            return false;
          }
        }

        return true;
      }


      // Inequality comparison operator
      bool operator!= (const Vector& that) {
        return !(*this == that);
      }


      // ====================== ELEMENT-WISE OPERATORS ======================


      // Element-wise addition assignment
      Vector& operator+= (const Vector& that) {
        if ( this->nElems != that.nElems ) {
          ERROR("Vector dimensions must match!");
        }

        #pragma omp parallel for schedule(dynamic, 1)
        for (int vectIndex = 0; vectIndex < totalVectCount; vectIndex++) {
          this->values[vectIndex] += that.values[vectIndex];
        }

        return *this;
      }


      // Element-wise addition
      const Vector operator+ (const Vector& that) const {
        return Vector<val_t>(*this) += that;
      }


      // Element-wise subtraction assignment
      Vector& operator-= (const Vector& that) {
        if ( this->nElems != that.nElems ) {
          ERROR("Vector dimensions must match!");
        }

        #pragma omp parallel for schedule(dynamic, 1)
        for (int vectIndex = 0; vectIndex < totalVectCount; vectIndex++) {
          this->values[vectIndex] -= that.values[vectIndex];
        }

        return *this;
      }


      // Element-wise subtraction
      const Vector operator- (const Vector& that) const {
        return Vector<val_t>(*this) -= that;
      }


      // Element-wise multiplication assignment
      Vector& operator*= (const Vector& that) {
        if ( this->nElems != that.nElems ) {
          ERROR("Vector dimensions must match!");
        }

        #pragma omp parallel for schedule(dynamic, 1)
        for (int vectIndex = 0; vectIndex < totalVectCount; vectIndex++) {
          this->values[vectIndex] *= that.values[vectIndex];
        }

        return *this;
      }


      // Element-wise multiplication
      const Vector operator* (const Vector& that) const {
        return Vector<val_t>(*this) *= that;
      }


      // Scalar (right) multiplication assignment
      Vector& operator*= (val_t that) {

        if ( this->nElems < 1 ) {
          return *this;
        }

        vect_t thatVect = this->_fill(that);

        #pragma omp parallel for schedule(dynamic, 1)
        for (int vectIndex = 0; vectIndex < totalVectCount; vectIndex++) {
          this->values[vectIndex] *= thatVect;
        }

        return *this;
      }


      // Scalar (right) multiplication
      const Vector operator* (const val_t that) const {
        return Vector<val_t>(*this) *= that;
      }


      // Element-wise division assignment
      Vector& operator/= (const Vector& that) {
        if ( this->nElems != that.nElems ) {
          ERROR("Vector dimensions must match!");
        }

        #pragma omp parallel for schedule(dynamic, 1)
        for (int vectIndex = 0; vectIndex < totalVectCount; vectIndex++) {
          this->values[vectIndex] /= that.values[vectIndex];
        }

        return *this;
      }


      // Element-wise division
      const Vector operator/ (const Vector& that) const {
        return Vector<val_t>(*this) /= that;
      }


      // Scalar (right) division assignment
      Vector& operator/= (val_t that) {

        if ( that == zeroVal ) {
          ERROR("Division by zero!");
        }

        return this->operator*= ((val_t)1. / that);
      }


      // Scalar (right) multiplication
      const Vector operator/ (const val_t that) const {

        if ( that == zeroVal ) {
          ERROR("Division by zero!");
        }

        return Vector<val_t>(*this) /= that;
      }


      // ====================== MATRIX MULTIPLICATION ======================


      // Sparse vector-matrix multiplication


      // Dot product
      val_t dot(const Vector<val_t>& that) const {
        if ( this->nElems != that.nElems ) {
          ERROR("Vector dimensions must match!");
        }

        val_t ret = zeroVal;

        vect_t sum = zeroVect;

        for (int vectIndex = 0; vectIndex < this->totalVectCount; vectIndex++) {
          sum += this->values[vectIndex] * that.values[vectIndex];
        }

        ret += this->_reduce(sum);

        return ret;
      }


      // ====================== OTHER METHODS ======================


      // Number of columns
      const int numElems() const { return this->nElems; }


      // Alias for the number of elements
      const int len() const { return this->nElems; }


      // Getter for the value array
      std::vector<vect_t> getValues() const {
        std::vector<vect_t> ret = this->values;
        return ret;
      }


      // Getter for the value array, without the SIMD vectors
      std::vector<val_t> getElems() const {
        std::vector<val_t> ret(this->nElems, this->zeroVal);

        for (int i = 0; i < this->nElems; i++) {
          ret[i] = this->operator() (i);
        }

        return ret;
      }


      // Add rows from another vector to this
      const Vector addRows(const Vector<val_t>& that) const {
        std::vector<vect_t> newValues = this->values;
        newValues.insert(std::end(newValues), std::begin(that.values), std::end(that.values));
        
        return Vector<val_t>(this->nElems + that.nElems, newValues);
      }


      // Method that applies a function to each element of the vector
      const Vector apply(std::function<val_t(val_t)> func) const {
        Vector<val_t> ret = Vector<val_t>(this->nElems);

        for (int i = 0; i < this->nElems; i++) {
          ret.place(i + INDEX_OFFSET, func(this->operator() (i + INDEX_OFFSET)));
        }

        return ret;
      }


      // The p-norm. Defaults to 2nd norm (Euclidean distance)
      val_t pNorm(int p = 2) const {

        if ( p < 1 ) {
          ERROR("Invalid p value (< 1) passed!");
        }

        if ( this->nElems < 1 ) {
          ERROR("Vector must be initialized!");
        }

        val_t ret = zeroVal;

        for (int vectIndex = 0; vectIndex < this->totalVectCount; vectIndex++) {
          vect_t vect = this->values[vectIndex];

          for (int vectElem = 0; vectElem < this->vectSize; vectElem++) {
            ret += std::pow(vect[vectElem], (val_t)p);
          }
        }

        return std::pow(ret, (val_t)(1. / p));
      }


      // Approximative comparison. The default tolerance is 10^(-6)
      bool isClose(const Vector& that, val_t tol = (val_t)1e-6) {
        if ( this->nElems != that.nElems ) return false;

        for (int i = 0; i < this->nElems; i++) {
          if ( std::abs(this->operator() (i) - that(i)) > tol ) {
            return false;
          }
        }

        return true;
      }


      // Vector saving. By default uses a space ' ' as the delimeter between the index and the value
      bool save(const std::string& path, char delim=' ') {
        if ( this->nElems < 1 ) {
          ERROR("Cannot save an unitialized vector!");
        }

        std::ofstream file(path);
        bool success = true;

        for (int i = 0; i < this->nElems; i++) {
          val_t val = this->operator() (i);
          if ( !(file << i << delim << val << std::endl) ) {
            success = false;
          }
        }

        file.close();

        return success;
      }

  };


  // Default insertion operator
  template <class val_t>
  std::ostream& operator<<(std::ostream& os, Vector<val_t>& v) {
    if (v.len() == 0) {
      os << "[]" << std::endl;  // Signifies uninitialized vector
          
      return os;
    }
      
    os << "[";
    for (int i = 0; i < v.len(); i++) {
      if (i > 0) {
        os << std::endl << ' ';
      }
      os << v(i);
    }
    os << "]" << std::endl;
    
    return os;
  }


  // Scalar (left) multiplication
  template <class val_t>
  const Vector<val_t> operator* (val_t scalar, const Vector<val_t>& vector) {
    return Vector<val_t>(vector) *= scalar;
  }


    // Stacking vectors
    template <class val_t>
    const Vector<val_t> stack(std::vector<Vector<val_t>> vectors) {

      if ( vectors.size() < 1 ) {
        ERROR("There must be at least one vector to stack!");
      }
  
      Vector<val_t> tmp = vectors[0];
  
      for (int i = 1; i < vectors.size(); i++) {
        tmp = tmp.addRows(vectors[i]);
      }
  
      return tmp;
    }


}


#endif