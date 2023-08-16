import sys
import os
import PyPDF2
from tabulate import tabulate

def main():
    num_args = len(sys.argv)
    if num_args > 2:
        print("Cannot invoke with that amount of args.", file=sys.stderr)
        quit()

    currentDir = os.getcwd()
    fileTable = []
    totalPages = 0
    for file in os.listdir(currentDir):
        if not file.endswith('.pdf'):
            continue
        pages = count_pages(file)
        totalPages += pages
        fileTable.append([file, pages])

    fileTable.append([])
    fileTable.append(['Total', totalPages])

    if num_args == 2:
        days = int(sys.argv[1])
        if days <= 0:
            print("Cannot invoke with a 0 or negative amount of days.", file=sys.stderr)
            quit()
        pagesPerDay = totalPages / days
        fileTable.append(['Pages/Day', round(pagesPerDay)])

    print(tabulate(fileTable, headers=['File', 'Pages']))

def count_pages(fileName):
    """
    Gets the amount of pages of the given pdf file.
    :param fileName: The file name
    :return: The amount of pages
    """
    file = open(fileName, 'rb')
    reader = PyPDF2.PdfFileReader(file)
    return reader.numPages

if __name__ == "__main__":
    main()
