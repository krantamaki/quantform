A2 = sprand(10, 10, 0.3);
spsave(A2, "matrix2.dat");
A3 = sprand(10, 10, 0.4);
spsave(A3, "matrix3.dat");

b1 = rand(10, 1);
vecsave(b1, "vector1.dat");

% Test 6
A23_add = A2 + A3;
spsave(A23_add, "matrix2&3_add.dat");

% Test 7
A23_sub = A2 - A3;
spsave(A23_sub, "matrix2&3_sub.dat");

% Test 8
A23_mul = A2 .* A3;
spsave(A23_mul, "matrix2&3_mul.dat");

% Test 9
A2b1_matmul = A2 * b1;
vecsave(A2b1_matmul, "matrix2&vector1_matmul.dat");

% Test 10
% RowDot, not implemented here

% Test 11
A2_T = A2';
spsave(A2_T, "matrix2_transpose.dat");

% Test 12
A23_matmul = A2 * A3;
spsave(A23_matmul, "matrix2&3_matmul.dat");

% Test 13
A2_frobenius = norm(A2, 'fro');
A2_frobenius

% Test 14
% save, n not implemented here


