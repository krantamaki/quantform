#ifndef MATRIX_HPP
#define MATRIX_HPP

#include <vector>
#include <tuple>
#include <cmath>
#include <fstream>
#include <iostream>
#include <sstream>

#include "../lalib.hpp"
#include "Vector.hpp"


namespace lalib {


  /*
   * Compressed row storage (CRS) format of matrix implementation.
   * Vectorized using SIMD commands and templated to permit different datatypes.
   * However, the datatype must be vectorizable i.e. float and double are mainly useful
   */
  template <class val_t>
  class Matrix {

    protected:

      // Alias for the vectorized type
      using vect_t = decltype(ulib::choose_simd<val_t, true>());


      // The number of elements in the vector
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


      // Function giving the SIMD vectors string representation
      inline const std::string _toString(const vect_t vect) const {
      std::ostringstream valueStringStream;
        valueStringStream << "{ ";
        for (int vectElem = 0; vectElem < this->vectSize; vectElem++) {
          valueStringStream << vect[vectElem] << " ";
        }
        valueStringStream << "}";
        return valueStringStream.str();
      }


      // Define a vector of zeros and the zero value
      val_t zeroVal = (val_t)0.;
      vect_t zeroVect = this->_fill(zeroVal);


      // Define the actual data arrays
      std::vector<vect_t> values;       // Holds the value vectors themselves
      std::vector<int> colVectIndexes;  // Gives the column indexes for the elements in the vector
      std::vector<int> rowPointers;     // Gives the index for the first vect on a given row


      // Define additional needed variables
      int totalVectCount = 0;
      int vectsPerRow = 0;
      int nCols = 0;
      int nRows = 0;


      // Const function for finding the correct vector index for a given matrix index
      inline const int _vectIndex(int normalIndex) const {
        return normalIndex / this->vectSize;
      }


      // Const function for finding the correct vector element for a given matrix index
      inline const int _vectElem(int normalIndex) const {
        return normalIndex % this->vectSize;
      }


      // Const function that returns a vector with value at given index and rest zeros
      inline const vect_t _valueVect(int vectElem, val_t value) const {
        vect_t newVect = zeroVect;
        newVect[vectElem] = value;

        return newVect;
      }


      // Const function for finding the column index given the index of the SIMD vector and the element in it
      inline const int _colIndex(int vectIndex, int vectElem) const {
        return vectIndex * this->vectSize + vectElem;
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
      Matrix(void) { }


      // Copying constructor
      Matrix(const Matrix<val_t>& that) {

        if ( that.nCols < 1 || that.nRows < 1 ) {
          ERROR("Matrix dimensions must be positive!");
        }

        this->nCols = that.nCols;
        this->nRows = that.nRows;
        this->vectsPerRow = that.vectsPerRow;
        this->totalVectCount = that.totalVectCount;
 
        this->values = that.values;
        this->colVectIndexes = that.colVectIndexes;
        this->rowPointers = that.rowPointers;
      }


      // Zeros constructor
      Matrix(int rows, int cols) {

        if ( cols < 1 || rows < 1 ) {
          ERROR("Matrix dimensions must be positive!");
        }

        this->nCols = cols;
        this->nRows = rows;
        this->vectsPerRow = ulib::ceil(nCols, vectSize);
        this->totalVectCount = 0;

        this->rowPointers = std::vector<int>(rows + 1, 0);
      }


      // Identity matrix constructor
      Matrix(int rows, int cols, val_t scalar) {

        if ( cols < 1 || rows < 1 ) {
          ERROR("Matrix dimensions must be positive!");
        }

        this->nRows = rows;
        this->nCols = cols;

        this->vectsPerRow = ulib::ceil(this->nCols, this->vectSize);
        this->rowPointers = std::vector<int>(this->nRows + 1, 0);

        int rowColMin = rows < cols ? rows : cols;

        this->totalVectCount = rowColMin;

        for (int i = 0; i < rowColMin; i++) {
          this->values.push_back(this->_valueVect(this->_vectElem(i), scalar));
          this->colVectIndexes.push_back(this->_vectIndex(i));

          for (int j = i + 1; j < this->nRows + 1; j++) {
            this->rowPointers[j]++;
          }
        }
      }


      // Diagonal matrix constructor
      Matrix(Vector<val_t> diag) {

        this->nRows = diag.len();
        this->nCols = diag.len();

        this->vectsPerRow = ulib::ceil(this->nCols, this->vectSize);
        this->rowPointers = std::vector<int>(this->nRows + 1, 0);
        this->totalVectCount = this->nRows;

        for (int i = 0; i < this->nRows; i++) {
          this->values.push_back(this->_valueVect(this->_vectElem(i), diag(i + INDEX_OFFSET)));
          this->colVectIndexes.push_back(this->_vectIndex(i));

          for (int j = i + 1; j < this->nRows + 1; j++) {
            this->rowPointers[j]++;
          }
        }
      }


      // CRS array constructor that takes in an array of vectors
      Matrix(int rows, int cols, const std::vector<vect_t>& newValues, const std::vector<int>& newColVectIndexes, const std::vector<int>& newRowPointers) {

        int newVectsPerRow = ulib::ceil(cols, vectSize);

        LOWPRIORITY(ulib::formString(*std::max_element(newRowPointers.begin(), newRowPointers.end()), " ", (int)newColVectIndexes.size()));
        
        if ( (*std::max_element(newColVectIndexes.begin(), newColVectIndexes.end()) >= newVectsPerRow) ||          // Check that no column index is out of bounds
             (*std::max_element(newRowPointers.begin(), newRowPointers.end()) > (int)newColVectIndexes.size()) ||  // Check that the rows pointers are in bounds
             (*std::min_element(newColVectIndexes.begin(), newColVectIndexes.end()) < 0 + INDEX_OFFSET) ||         // Check that column indexes are not less than wanted minimum value
             (*std::min_element(newRowPointers.begin(), newRowPointers.end()) < 0 + INDEX_OFFSET)) {               // Check that row pointers are not less than wanted minimum value
          ERROR("Matrix dimensions out of bounds!");
        }
        
        this->nCols = cols;
        this->nRows = rows;

        this->vectsPerRow = newVectsPerRow;
        this->totalVectCount = newValues.size();

        this->values = newValues;
        this->colVectIndexes = newColVectIndexes;
        this->rowPointers = newRowPointers;
      }


      // CRS array constructor that takes in an array of values. Assumes that indexing starts from 0
      Matrix(int rows, int cols, const std::vector<val_t>& newValues, const std::vector<int>& newColIndexes, const std::vector<int>& newRowPointers) {

        int newVectsPerRow = ulib::ceil(cols, vectSize);
        
        if ( (*std::max_element(newColIndexes.begin(), newColIndexes.end()) >= cols) ||                        // Check that no column index is out of bounds
             (*std::max_element(newRowPointers.begin(), newRowPointers.end()) > (int)newColIndexes.size()) ||  // Check that the rows pointers are in bounds
             (*std::min_element(newColIndexes.begin(), newColIndexes.end()) < 0 + INDEX_OFFSET) ||             // Check that column indexes are not less than wanted minimum value
             (*std::min_element(newRowPointers.begin(), newRowPointers.end()) < 0 + INDEX_OFFSET)) {           // Check that row pointers are not less than wanted minimum value
          ERROR("Matrix dimensions out of bounds!");
        }
        
        this->nCols = cols;
        this->nRows = rows;

        this->vectsPerRow = newVectsPerRow;
        this->rowPointers = std::vector<int>(this->nRows + 1, 0);;

        int nVects = 0;
        int lastVectIndex = -1;

        // Loop over the rows
        for (int row = 0; row < rows; row++) {
          for (int i = newRowPointers[row]; i < newRowPointers[row + 1]; i++) {
            int col = newColIndexes[i];
            val_t val = newValues[i];

            int vectIndex = this->_vectIndex(col);
            int vectElem = this->_vectElem(col);

            if ( val == zeroVal ) {
              continue;  // Assumption is that values cannot be overwritten here
            }
            if ( vectIndex == lastVectIndex ) {
              this->values[nVects - 1][vectElem] = val;
              continue;
            }

            this->colVectIndexes.push_back(vectIndex);
            this->values.push_back(this->_valueVect(vectElem, val));

            lastVectIndex = vectIndex;
            nVects++;
          }

          lastVectIndex = -1;
          this->rowPointers[row + 1] = nVects;
        } 

        this->totalVectCount = nVects;
      }


      /*
       * Load from file constructor
       * Assumes that the values are whitespace separated as <row col val> and the values are ordered by row index
       * The last row of the file is assumed to contain the bottom right element of the matrix (even if zero)
       */
      Matrix(const std::string& path, int offset = 0) {

        // Variables to read the line contents to
        int row, col;
        val_t val;

        // Open the file
        std::ifstream file(path);

        if ( !file ) {
          ERROR(ulib::formString("Couldn't open the given file (", path, ")!"));
        }

        // Read the last line of the file to get the dimensions of the matrix
        std::stringstream lastLine = ulib::lastLine(path);
        int nTokens = ulib::numTokens(lastLine.str());

        if ( nTokens != 3 ) {
          ERROR(ulib::formString("File of an invalid format given (number of tokens = ", nTokens, ")!"));
        }

        lastLine >> row >> col >> val;

        this->nRows = row + 1 - offset;
        this->nCols = col + 1 - offset;

        this->vectsPerRow = ulib::ceil(this->nCols, this->vectSize);

        this->rowPointers = std::vector<int>(this->nRows + 1, 0);

        int nVects = 0;
        int lastSeenRow = 0;
        int lastVectIndex = -1;

        // Go through the file itself
        while (file >> row >> col >> val) {
          int rowOffsetted = row - offset;
          int colOffsetted = col - offset;

          int vectIndex = this->_vectIndex(colOffsetted);
          int vectElem = this->_vectElem(colOffsetted);

          if ( val == zeroVal ) {
            continue;  // Assumption is that values cannot be overwritten here
          }

          if ( (rowOffsetted == lastSeenRow) && (vectIndex == lastVectIndex) ) {
            this->values[nVects - 1][vectElem] = val;
            continue;
          }
          if ( rowOffsetted != lastSeenRow ) {
            int nEmptyRows = rowOffsetted - lastSeenRow;
            for (int i = 1; i < nEmptyRows; i++) {
              this->rowPointers[lastSeenRow + i] = this->rowPointers[lastSeenRow];
            }
            this->rowPointers[rowOffsetted] = nVects;
            lastSeenRow = rowOffsetted;
          }

          this->colVectIndexes.push_back(vectIndex);
          this->values.push_back(this->_valueVect(vectElem, val));

          lastVectIndex = vectIndex;
          nVects++;
        }

        for (int row = lastSeenRow + 1; row <= this->nRows; row++) {
          this->rowPointers[row] = nVects;
        }

        this->totalVectCount = nVects;

        file.close();
      }


      // ====================== PLACEMENT METHODS ======================


      // Single value placement method
      void place(int row, int col, val_t value) {

        int rowOffsetted = row - INDEX_OFFSET;
        int colOffsetted = col - INDEX_OFFSET;

        if ( rowOffsetted < 0 || 
             colOffsetted < 0 || 
             rowOffsetted >= this->nRows || 
             colOffsetted >= this->nCols ) {
              ERROR(ulib::formString("Given dimensions (", row, ", ", col, ") out of bounds for a matrix of size (", this->nRows, ", ", this->nCols, ")!"));
        }

        int vectIndex = this->_vectIndex(colOffsetted);
        int vectElem = this->_vectElem(colOffsetted);

        int rowPointer = rowPointers[rowOffsetted];
        int nextRowPointer = rowPointers[rowOffsetted + 1];

        // Only non-zero value needs to be placed into the matrix
        if ( value != this->zeroVal ) {

          // If there are no elements yet in the matrix just add the value
          if ( this->totalVectCount == 0 ) {
            this->values.push_back(this->_valueVect(vectElem, value));
            this->colVectIndexes.push_back(vectIndex);
            this->totalVectCount++;
          }

          // Otherwise, we need to find the correct location for the value
          else {

            // If the row is empty just add to the row pointers position
            if ( rowPointer == nextRowPointer ) {
              this->values.insert(this->values.begin() + rowPointer, this->_valueVect(vectElem, value));
              this->colVectIndexes.insert(this->colVectIndexes.begin() + rowPointer, vectIndex);
              this->totalVectCount++;
            }

            // Otherwise, iterate over the vectors to find the correct one or a place for a new one
            else {

              int i = rowPointer;
              for (; i < nextRowPointer; i++) {
                int vectIndex_i = this->colVectIndexes[i];

                // If there already is a vector at the given index add to it
                if ( vectIndex_i == vectIndex ) {
                  this->values[i][vectElem] = value;
                  return;
                }

                // If the iterated vector index exceeds the new one, add a new vector before it
                if ( vectIndex_i > vectIndex ) {
                  this->values.insert(this->values.begin() + i, this->_valueVect(vectElem, value));
                  this->colVectIndexes.insert(this->colVectIndexes.begin() + i, vectIndex);
                  this->totalVectCount++;
                  break;
                }
              }

              // New vector index is the largest one for the given row
              if ( i == nextRowPointer ) {
                this->values.insert(this->values.begin() + nextRowPointer, this->_valueVect(vectElem, value));
                this->colVectIndexes.insert(this->colVectIndexes.begin() + nextRowPointer, vectIndex);
                this->totalVectCount++;
              }
            }
          }

          // Increment the row pointers accordingly
          for (int row_i = rowOffsetted + 1; row_i <= this->nRows; row_i++) {
            this->rowPointers[row_i] += 1;
          }
        }

        // Otherwise, check if a non-zero value gets replaced
        else {

          // If the row is empty zero cannot replace a non-zero value
          if ( rowPointer == nextRowPointer ) {
            return;
          }

          // Otherwise, iterate over the vectors to find the correct one
          int i = rowPointer;
          for (; i < nextRowPointer; i++) {
            int vectIndex_i = this->colVectIndexes[i];

            // If there already is a vector at the given index add the zero value to it
            if ( vectIndex_i == vectIndex ) {
              this->values[i][vectElem] = this->zeroVal;
              
              // If only a zero vector is left delete it
              if ( this->_vectEq(this->values[i], this->zeroVect) ) {
                this->values.erase(this->values.begin() + i);
                this->colVectIndexes.erase(this->colVectIndexes.begin() + i);
                this->totalVectCount--;
                break;
              }
              else {
                return;
              }
            }

            // If the iterated vector index is larger than the given vector then the zero didn't replace a non-zero
            if ( vectIndex_i > vectIndex ) {
              return;
            }
          }

          // If the new vector would have the largest index then it cannot replace a non-zero element
          if ( i == nextRowPointer ) {
            return;
          }

          // Decrement the row pointers accordingly
          for (int row_i = row + 1; row_i <= this->nRows; row_i++) {
            this->rowPointers[row_i] -= 1;
          }
        }
      }


      // SIMD vector placement method
      void place(int row, int vectIndex, vect_t vect) {

        // Either the vector already exists and the placements can be done quickly
        // or the first placement creates the vector and rest can be done quickly
        for (int vectElem = 0; vectElem < this->vectSize; vectElem++) {
          int col = this->_colIndex(vectIndex, vectElem);

          // Don't try to place padding zeros
          if ( col < this->nCols ) {
            this->place(row + INDEX_OFFSET, col + INDEX_OFFSET, vect[vectElem]);
          }
        }
      }


      // ====================== ACCESSING METHODS ======================


      // Accessing method for matrix values. Note that the round brackets are used for this
      val_t operator() (int row, int col) const {

        int rowOffsetted = row - INDEX_OFFSET;
        int colOffsetted = col - INDEX_OFFSET;

        if ( rowOffsetted < 0 || 
             colOffsetted < 0 || 
             rowOffsetted >= this->nRows || 
             colOffsetted >= this->nCols ) {
          ERROR(ulib::formString("Given dimensions (", row, ", ", col, ") out of bounds for a matrix of size (", this->nRows, ", ", this->nCols, ")!"));
        }

        int vectIndex = this->_vectIndex(colOffsetted);
        int vectElem = this->_vectElem(colOffsetted);

        int rowPointer = this->rowPointers[rowOffsetted];
        int nextRowPointer = this->rowPointers[rowOffsetted + 1];

        // Empty row, return zero
        if ( rowPointer == nextRowPointer ) {
          return zeroVal;
        }

        for (int i = rowPointer; i < nextRowPointer; i++) {
          int vectIndex_i = this->colVectIndexes[i];

          if ( vectIndex_i == vectIndex ) {
            return this->values[i][vectElem];
          }
          if ( vectIndex_i > vectIndex ) {
            return zeroVal;
          }
        }

        return zeroVal;
      }


      // SIMD accessing method
      vect_t getSIMD(int row, int vectIndex) const {

        int rowOffsetted = row - INDEX_OFFSET;

        if ( rowOffsetted < 0 || 
             vectIndex < 0 || 
             rowOffsetted >= this->nRows || 
             vectIndex >= this->vectsPerRow ) {
          ERROR("Given dimensions out of bounds!");
        }

        int rowPointer = this->rowPointers[rowOffsetted];
        int nextRowPointer = this->rowPointers[rowOffsetted + 1];

        for (int i = rowPointer; i < nextRowPointer; i++) {
          int vectIndex_i = this->colVectIndexes[i];

          if ( vectIndex_i == vectIndex ) {
            return this->values[i];
          }
          if ( vectIndex_i > vectIndex ) {
            return zeroVect;
          }
        }

        return zeroVect;
      }


      // ====================== BASIC OPERATORS ======================


      // Assignment operator
      Matrix& operator= (const Matrix& that) {

        // Check for self-assignment ie. case where a = a is called by comparing the pointers of the objects
        if ( this == &that ) return *this;

        this->nRows = that.nRows;
        this->nCols = that.nCols;

        this->vectsPerRow = that.vectsPerRow;
        this->totalVectCount = that.totalVectCount;

        this->values = that.values;
        this->colVectIndexes = that.colVectIndexes;
        this->rowPointers = that.rowPointers;

        return *this;
      }


      // Equality comparison operator
      bool operator== (const Matrix& that) {

        if ( this->nRows != that.nRows || this->nCols != that.nCols ) {
          return false;
        }

        if ( this->totalVectCount != that.totalVectCount ) {
          return false;
        }

        for (int i = 0; i < this->totalVectCount; i++) {
          if ( !this->_vectEq(this->values[i], that.values[i]) || 
               this->colVectIndexes[i] != that.colVectIndexes[i] ) {
            return false;
          }
        }

        return true;
      }


      // Inequality comparison operator
      bool operator!= (const Matrix& that) {
        return !(*this == that);
      }


      // ====================== ELEMENT-WISE OPERATORS ======================

      // Note that these are by no means optimal implementations


      // Element-wise addition assignment
      Matrix& operator+= (const Matrix& that) {

        if (this->nCols != that.nCols || this->nRows != that.nRows) {
          ERROR("Matrix dimensions must match!");
        }

        for (int row = 0; row < that.nRows; row++) {
          for (int vectIndex = 0; vectIndex < this->vectsPerRow; vectIndex++) {
            vect_t thisVect = this->getSIMD(row + INDEX_OFFSET, vectIndex);
            vect_t thatVect = that.getSIMD(row + INDEX_OFFSET, vectIndex);

            if ( this->_vectEq(thisVect, this->zeroVect) && this->_vectEq(thatVect, this->zeroVect) ) {
              continue;
            }

            this->place(row + INDEX_OFFSET, vectIndex, thisVect + thatVect);
          }
        }

        return *this;
      }


      // Element-wise addition
      const Matrix operator+ (const Matrix& that) const {
        return Matrix<val_t>(*this) += that;
      }


      // Element-wise subtraction assignment
      Matrix& operator-= (const Matrix& that) {

        if (this->nCols != that.nCols || this->nRows != that.nRows) {
          ERROR("Matrix dimensions must match!");
        }

        for (int row = 0; row < that.nRows; row++) {
          for (int vectIndex = 0; vectIndex < this->vectsPerRow; vectIndex++) {
            vect_t thisVect = this->getSIMD(row + INDEX_OFFSET, vectIndex);
            vect_t thatVect = that.getSIMD(row + INDEX_OFFSET, vectIndex);

            if ( this->_vectEq(thisVect, this->zeroVect) && this->_vectEq(thatVect, this->zeroVect) ) {
              continue;
            }

            this->place(row + INDEX_OFFSET, vectIndex, thisVect - thatVect);
          }
        }

        return *this;
      }


      // Element-wise subtraction
      const Matrix operator- (const Matrix& that) const {
        return Matrix<val_t>(*this) -= that;
      }


      // Element-wise multiplication assignment
      Matrix& operator*= (const Matrix& that) {

        if (this->nCols != that.nCols || this->nRows != that.nRows) {
          ERROR("Matrix dimensions must match!");
        }

        for (int row = 0; row < that.nRows; row++) {
          for (int vectIndex = 0; vectIndex < this->vectsPerRow; vectIndex++) {
            vect_t thisVect = this->getSIMD(row + INDEX_OFFSET, vectIndex);
            vect_t thatVect = that.getSIMD(row + INDEX_OFFSET, vectIndex);

            if ( this->_vectEq(thisVect, this->zeroVect) ) {
              continue;
            }

            this->place(row + INDEX_OFFSET, vectIndex, thisVect * thatVect);
          }
        }

        return *this;
      }


      // Element-wise multiplication
      const Matrix operator* (const Matrix& that) const {
        return Matrix<val_t>(*this) *= that;
      }


      // Scalar (right) multiplication assignment
      Matrix& operator*= (val_t that) {

        if ( this->nCols < 1 || this->nRows < 1 ) {
          return *this;
        }

        vect_t thatVect = this->_fill(that);

        #pragma omp parallel for schedule(dynamic, 1)
        for (int i = 0; i < this->totalVectCount; i++) {
          this->values[i] *= thatVect;
        }

        return *this;
      }


      // Scalar (right) multiplication
      const Matrix operator* (const val_t that) const {
        return Matrix<val_t>(*this) *= that;
      }


      // Element-wise division is not a sensible operation as it will most likely not lead
      // to a sparse matrix. So it will not be implemented. Scalar division from the right can
      // be sensible and as it is easy to incorporate it is implemented.


      // Scalar (right) division assignment
      Matrix& operator/= (val_t that) {

        if ( that == zeroVal ) {
          ERROR("Division by zero!");
        }

        return this->operator*= ((val_t)1. / that);
      }


      // Scalar (right) division
      const Matrix operator/ (const val_t that) const {

        if ( that == zeroVal ) {
          ERROR("Division by zero!");
        }

        return Matrix<val_t>(*this) /= that;
      }


      // ====================== MATRIX MULTIPLICATION ======================


      // Sparse matrix-matrix multiplication
      const Matrix matmul(const Matrix& that) const {

        if ( this->nCols != that.nRows ) {
          ERROR("Improper dimensions!");
        }

        // The arrays for the resulting matrix
        std::vector<vect_t> newValues;
        std::vector<int> newColVectIndexes;
        std::vector<int> newRowPointers = std::vector<int>(this->nRows + 1, 0);

        // Transpose 'that' matrix to have a constant time access to the columns
        Matrix thatT = that.T();

        for (int row = 0; row < this->nRows; row++) {
          
          int nVectsOnThisRow = this->rowPointers[row + 1] - this->rowPointers[row];
          if ( nVectsOnThisRow == 0 ) continue;
          
          else {
            int lastSeenVectIndex = 0;
            vect_t lastVect = zeroVect;

            for (int col = 0; col < that.nCols; col++) {

              int vectIndex = this->_vectIndex(col);
              int vectElem = this->_vectElem(col);
        
              int nVectsOnThatTRow = thatT.rowPointers[col + 1] - thatT.rowPointers[col];
              if ( nVectsOnThatTRow == 0 ) continue;

              else {
                vect_t sum = zeroVect;

                for (int thatT_i = thatT.rowPointers[col]; thatT_i < thatT.rowPointers[col + 1]; thatT_i++) {
                  int thatTVectIndex = that.colVectIndexes[thatT_i];
                  vect_t thatTVect = thatT.values[thatT_i];
                  vect_t thisVect = this->getSIMD(row, thatTVectIndex);
                  sum += thatTVect * thisVect;
                }

                if ( !(this->_vectEq(sum, this->zeroVect)) ) {
                  if ( vectIndex == lastSeenVectIndex ) {
                    lastVect[vectElem] = this->_reduce(sum);
                  }
                  else {
                    newValues.push_back(lastVect);
                    newColVectIndexes.push_back(lastSeenVectIndex);

                    for (int row_i = row + 1; row_i <= this->nRows; row_i++) {
                      newRowPointers[row_i] += 1;
                    }

                    lastVect = zeroVect;
                    lastVect[vectElem] = this->_reduce(sum);
                    lastSeenVectIndex = vectIndex;
                  }
                }
              }
            }
          }
        }
        
        return Matrix<val_t>(this->nRows, that.nCols, newValues, newColVectIndexes, newRowPointers);
      }


      // Sparse matrix-vector multiplication
      const Vector<val_t> matmul(const Vector<val_t>& that) const {

        if ( this->nCols != that.len() ) {
          ERROR("Improper dimensions!");
        }

        Vector<val_t> ret = Vector<val_t>(this->nRows);

        #pragma omp parallel for schedule(dynamic, 1)
        for (int row = 0; row < this->nRows; row++) {

          int nVectsOnThisRow = this->rowPointers[row + 1] - this->rowPointers[row];
          if ( nVectsOnThisRow == 0 ) continue;

          vect_t sumVect = zeroVect;

          for (int i = this->rowPointers[row]; i < this->rowPointers[row + 1]; i++) {

            int vectIndex = this->colVectIndexes[i];
            vect_t vect = this->values[i];

            sumVect += vect * that.getSIMD(vectIndex);
          }

          val_t sum = this->_reduce(sumVect);

          ret.place(row + INDEX_OFFSET, sum);
        }

        return ret;
      }


      // Dot product between a row and a given vector
      const val_t rowDot(int row, const Vector<val_t>& that) const {

        int rowOffsetted = row - INDEX_OFFSET;

        if ( this->nCols != that.len() ) {
          ERROR("Improper dimensions!");
        }

        if ( rowOffsetted < 0 || rowOffsetted >= this->nRows ) {
          ERROR("Improper row index!");
        }


        int nVectsOnThisRow = this->rowPointers[row + 1] - this->rowPointers[row];
        if ( nVectsOnThisRow == 0 ) return (val_t)0.;

        vect_t sumVect = zeroVect;

        for (int i = this->rowPointers[row]; i < this->rowPointers[row + 1]; i++) {

          int vectIndex = this->colVectIndexes[i];
          vect_t vect = this->values[i];

          sumVect += vect * that.getSIMD(vectIndex);
        }

        return this->_reduce(sumVect);
      }


      // ====================== OTHER METHODS ======================


      // Method that prints the CRS arrays of the matrix into ostream. Used for debugging
      void _printArrays() const {
        // The values themselves (in vector format)
        std::ostringstream valueStringStream;
        valueStringStream << "values:         [ ";
        for (int i = 0; i < this->totalVectCount; i++) {
          valueStringStream << this->_toString(this->values[i]) << " ";
        }
        valueStringStream << "]";
        INFO(valueStringStream.str());

        // The column vector indexes
        std::ostringstream colVectIndexesStringStream;
        colVectIndexesStringStream << "colVectIndexes: [ ";
        for (int vectIndex: this->colVectIndexes) colVectIndexesStringStream << vectIndex << " ";
        colVectIndexesStringStream << "]";
        INFO(colVectIndexesStringStream.str());

        // The row pointers
        std::ostringstream rowPointerStringStream;
        rowPointerStringStream << "rowPointers:    [ ";
        for (int rowPointer: this->rowPointers) rowPointerStringStream << rowPointer << " ";
        rowPointerStringStream << "]";
        INFO(rowPointerStringStream.str());
      }


      // Getter for the value array
      std::vector<vect_t> getValues() const {
        std::vector<vect_t> ret = this->values;
        return ret;
      }


      // Getter for the column vector index array
      std::vector<int> getColVectIndexes() const {
        std::vector<int> ret = this->colVectIndexes;
        return ret;
      }


      // Getter for the row pointer array
      std::vector<int> getRowPointers() const {
        std::vector<int> ret = this->rowPointers;
        return ret;
      }


      // Number of columns
      const int numCols() const { return this->nCols; }


      // Number of rows
      const int numRows() const { return this->nRows; }


      // The shape of the matrix
      const std::tuple<int, int> shape() const { return std::make_tuple(this->nRows, this->nCols); }


      // Add rows from another matrix to this one
      const Matrix addRows(const Matrix<val_t>& that) {

        if ( this->nCols != that.nCols ) {
          ERROR("Matrices must have the same number of columns!");
        }

        std::vector<vect_t> newValues = this->values;
        std::vector<int> newColVectIndexes = this->colVectIndexes;
        std::vector<int> newRowPointers = std::vector<int>(std::begin(this->rowPointers), std::end(this->rowPointers) - 1);
        std::vector<int> thatRowPointers = that.rowPointers;

        newValues.insert(std::end(newValues), std::begin(that.values), std::end(that.values));
        newColVectIndexes.insert(std::end(newColVectIndexes), std::begin(that.colVectIndexes), std::end(that.colVectIndexes));
        
        for (int& elem : thatRowPointers) { elem += this->totalVectCount; }

        newRowPointers.insert(std::end(newRowPointers), std::begin(thatRowPointers), std::end(thatRowPointers));
        
        return Matrix<val_t>(this->nRows + that.nRows, this->nCols, newValues, newColVectIndexes, newRowPointers);
      }


      // TODO: Add apply function
      // const Matrix apply(...) {}


      // Naive transpose. Not the most efficient implementation, but should be guaranteed to work
      const Matrix naiveTranspose() const {

        if ( this->nCols < 1 || this->nRows < 1 ) {
          return *this;
        }

        // The arrays for the transpose
        std::vector<vect_t> valuesT;
        std::vector<int> colVectIndexesT;
        std::vector<int> rowPointersT = std::vector<int>(this->nCols + 1, 0);

        int nVects = 0;
        int lastSeenVectIndex = -1;

        for (int col = 0; col < this->nCols; col++) {
          for (int row = 0; row < this->nRows; row++) {
            val_t value = this->operator() (row, col);

            int vectIndex = this->_vectIndex(row);
            int vectElem = this->_vectElem(row);

            if ( value != zeroVal ) {

              if ( vectIndex == lastSeenVectIndex ) {
                valuesT[nVects - 1][vectElem] = value;
                continue;
              }
              
              valuesT.push_back(this->_valueVect(vectElem, value));
              colVectIndexesT.push_back(vectIndex);
              lastSeenVectIndex = vectIndex;
              nVects++;

              for (int col_i = col + 1; col_i <= this->nCols; col_i++) {
                rowPointersT[col_i] += 1;
              }
            }
          }

          lastSeenVectIndex = -1;
        }
        
        return Matrix<val_t>(this->nCols, this->nRows, valuesT, colVectIndexesT, rowPointersT);
      }


      /*
       * More efficient transpose implementation.
       * Essentially equivalent to Scipy implementation https://github.com/scipy/scipy/blob/8a64c938ddf1ae4c02a08d2c5e38daeb8d061d38/scipy/sparse/sparsetools/csr.h#L419
       * Doesn't have a constant space complexity due to a need for an auxiliary array of size O(nCols)
       */ 
      const Matrix transpose() const {

        if ( this->nCols < 1 || this->nRows < 1 ) {
          return *this;
        }

        // The arrays for the transpose
        std::vector<vect_t> valuesT;
        std::vector<int> colVectIndexesT;

        // Note that additional zero is stored so that in main loop the row pointer values can be incremented
        std::vector<int> rowPointersT = std::vector<int>(this->nCols + 2, 0);

        // Auxiliary array needed for keeping track of what SIMD vectors are already counted
        std::vector<int> rowPointersTLastVectIndex = std::vector<int>(this->nCols, -1);

        // Form the row pointer array for the transpose
        for (int row = 0; row < this->nRows; row++) {
          for (int i = this->rowPointers[row]; i < this->rowPointers[row + 1]; i++) {
            vect_t vect = this->values[i];
            int colVectIndex = this->colVectIndexes[i];

            for (int colVectElem = 0; colVectElem < this->vectSize; colVectElem++) {
              if ( vect[colVectElem] != zeroVal ) {
                int col = this->_colIndex(colVectIndex, colVectElem);
                int rowVectIndex = this->_vectIndex(row);

                if ( rowPointersTLastVectIndex[col] != rowVectIndex ) {
                  rowPointersTLastVectIndex[col] = rowVectIndex;
                  rowPointersT[col + 1]++;
                }
              }
            }
          }
        }

        int cumulativeSum = 0;
        for (int col = 1; col < this->nCols + 1; col++) {
          int tmp = rowPointersT[col];
          rowPointersT[col] = cumulativeSum;
          cumulativeSum += tmp;
        }

        rowPointersT[this->nCols + 1] = cumulativeSum;

        int nVects = cumulativeSum;

        // Allocate memory for the transpose arrays
        valuesT = std::vector<vect_t>(nVects, zeroVect);
        colVectIndexesT = std::vector<int>(nVects, 0);

        // Do the actual transpose
        for (int row = 0; row < this->nRows; row++) {
          for (int i = this->rowPointers[row]; i < this->rowPointers[row + 1]; i++) {
            vect_t rowVect = this->values[i];
            int rowVectIndex = this->colVectIndexes[i];

            for (int rowVectElem = 0; rowVectElem < this->vectSize; rowVectElem++) {
              val_t value = rowVect[rowVectElem];

              if ( value != zeroVal ) {

                int col = this->_colIndex(rowVectIndex, rowVectElem);
                int i_T = rowPointersT[col + 1];
                int colVectIndex = this->_vectIndex(row);
                int colVectElem = this->_vectElem(row);

                if ( this->_vectEq(valuesT[i_T], this->zeroVect) ) {
                  colVectIndexesT[i_T] = colVectIndex;
                  valuesT[i_T][colVectElem] = value;
                  continue;
                }

                if ( colVectIndexesT[i_T] != colVectIndex ) {
                  colVectIndexesT[i_T + 1] = colVectIndex;
                  valuesT[i_T + 1][colVectElem] = value;
                  rowPointersT[col + 1]++;
                  continue;
                }

                valuesT[i_T][colVectElem] = value;
              }
            }
          }
        }

        // Remove the now unnecessary last row pointer element
        rowPointersT.pop_back();

        // Increment the row pointers by one as the last vector per row doesn't accumulate total
        for (int col = 1; col < this->nCols + 1; col++) {
          rowPointersT[col]++;
        }

        return Matrix<val_t>(this->nCols, this->nRows, valuesT, colVectIndexesT, rowPointersT);
      }


      // Alias for transpose
      const Matrix T() const {
        return this->transpose();
      }


      // Frobenius norm
      val_t frobenius() const {

        if ( this->nCols < 1 || this->nRows < 1 ) {
          ERROR("Matrix must be initialized!");
        }

        val_t ret = zeroVal;

        for (int vectIndex = 0; vectIndex < this->totalVectCount; vectIndex++) {
          vect_t vect = this->values[vectIndex];

          for (int vectElem = 0; vectElem < this->vectSize; vectElem++) {
            ret += std::pow(vect[vectElem], (val_t)2.);
          }
        }

        return std::sqrt(ret);
      }


      // Approximative comparison. The default tolerance is 10^(-6)
      bool isClose(const Matrix& that, val_t tol = (val_t)1e-6) {
        
        if ( this->nRows != that.nRows || this->nCols != that.nCols ) {
          return false;
        }

        if ( this->totalVectCount != that.totalVectCount ) {
          return false;
        }

        for (int i = 0; i < this->totalVectCount; i++) {

          if ( this->colVectIndexes[i] != that.colVectIndexes[i] ) {
            return false;
          }

          vect_t thisVect = this->values[i];
          vect_t thatVect = that.values[i];

          for (int vectElem = 0; vectElem < vectSize; vectElem++) {
            if ( std::abs(thisVect[vectElem] - thatVect[vectElem]) > tol ) {
              return false;
            }
          }
        }

        return true;
      }


      // Matrix saving. By default uses a space ' ' as the delimeter between the indexes and the value
      bool save(const std::string& path, char delim = ' ') {

        if ( this->nCols <= 0 || this->nRows <= 0 ) {
          ERROR("Cannot save an unitialized matrix!");
        }

        bool success = true;

        std::ofstream file(path);

        for (int row = 0; row < this->nRows; row++) {
          for (int i = this->rowPointers[row]; i < rowPointers[row + 1]; i++) {
            int vectIndex = this->colVectIndexes[i];

            for (int vectElem = 0; vectElem < this->vectSize; vectElem++) {

              int col = this->_colIndex(vectIndex, vectElem);

              if ( col >= this->nCols ) continue;  // Don't add the padding zeros

              val_t val = this->values[i][vectElem];

              if ( !(file << row << delim << col << delim << val << std::endl) ) {
                success = false;
              }
            }
          }
        }

        if ( this->operator() (this->nRows - 1, this->nCols - 1) == zeroVal ) {
          if ( !(file << this->nRows - 1 << delim << this->nCols - 1 << delim << zeroVal << std::endl) ) {
            success = false;
          }
        }
        
        file.close();
        
        return success;
      }

  };


  // Insertion operator. Inserts the full matrix
  template <class val_t>
  std::ostream& operator<<(std::ostream& os, Matrix<val_t>& A) {
    if (A.numCols() == 0 || A.numRows() == 0) {
      os << "[]" << std::endl;  // Signifies uninitialized matrix
          
      return os;
    }
      
    os << "[";
    for (int row = 0; row < A.numRows(); row++) {
      if (row > 0) os << ' ';

      os << "[";
      for (int col = 0; col < A.numCols() - 1; col++) {
        os << A(row, col) << ' ';
      }
      os << A(row, A.numCols() - 1) << "]";

      if (row < A.numRows() - 1) os << std::endl; 
    }
    os << "]" << std::endl;

    return os;
  }


  // Scalar (left) multiplication
  template <class val_t>
  const Matrix<val_t> operator* (val_t scalar, const Matrix<val_t>& matrix) {
    return Matrix(matrix) *= scalar;
  }


  // Stacking matrices
  template <class val_t>
  const Matrix<val_t> stack(std::vector<Matrix<val_t>> matrices) {
    
    if ( matrices.size() < 1 ) {
      ERROR("There must be at least one matrix to stack!");
    }

    Matrix<val_t> tmp = matrices[0];

    for (int i = 1; i < matrices.size(); i++) {
      tmp = tmp.addRows(matrices[i]);
    }

    return tmp;
  }


}

#endif