class TableWriter:
    def __init__(self, file_name):
        self.__curr_column = 0
        self.__column_number = 0
        self.__file = open(file_name, 'w')

    def begin(self, column_number):
        self.__column_number = column_number
        preamble = "\\begin{table}[h]\n" + \
                   "\\centering\n" + \
                   "\\begin{tabular}{ |" + "c|" * column_number + " }\n" + \
                   "\\hline \n"

        self.__file.writelines(preamble)

    def append(self, val):
        if self.__curr_column > 0:
            self.__file.write(" & ")
        self.__file.write(val)

        self.__curr_column += 1
        if self.__curr_column == self.__column_number:
            self.next_line()

    def next_line(self):
        for i in range(self.__curr_column, self.__column_number - 1):
            self.__file.write(" & ")
        self.__file.write("\\\\ \n" +
                          "\\hline \n")
        self.__curr_column = 0

    def end(self, table_name):
        if self.__curr_column != 0:
            self.next_line()

        postamble = "\\end{tabular} \n" + \
                    "\\caption{" + table_name + "} \n" + \
                    "\\end{table} \n\n"

        self.__file.writelines(postamble)
