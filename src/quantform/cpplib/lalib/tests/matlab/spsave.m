function success = spsave(A, filename)

    file = fopen(filename, "w");
    [row, col, val] = find(A);

    data = [row, col, val];
    sorted_data = sortrows(data, [1, 2]);

    for i=1:length(row)
        fprintf(file, '%i %i %e\n', sorted_data(i, 1), sorted_data(i, 2), sorted_data(i, 3));
    end

    if A(size(A, 1), size(A, 2)) == 0
        fprintf(file, '%i %i %e\n', size(A, 1), size(A, 2), 0);
    end
   
    fclose(file);

    success = 1;
end