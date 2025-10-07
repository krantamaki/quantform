function success = vecsave(b, filename)
    file = fopen(filename, "w");

    for i=1:length(b)
        fprintf(file, '%i %e\n', i, b(i));
    end
   
    fclose(file);

    success = 1;
end