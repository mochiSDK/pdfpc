import sys
import os
import argparse
import PyPDF2
from tabulate import tabulate

def main(args):
    fileTable = []
    totalPages = 0
    pdfFileCounter = 0
    for fileName in os.listdir(args.dir):
        if not fileName.endswith('.pdf'):
            continue
        # Reconstructing the full file path.
        pages = count_pages(f"{args.dir}{os.path.sep}{fileName}")
        totalPages += pages
        fileTable.append([fileName, pages])
        pdfFileCounter += 1

    if pdfFileCounter == 0:
        print("pdfpc: error: No PDF file(s) found in this directory.", file=sys.stderr)
        quit()

    fileTable.append([])
    fileTable.append(['Total', totalPages])

    if args.days is not None:
        if args.days <= 0:
            parser.error("Cannot invoke with a 0 or negative amount of days.")
        pagesPerDay = totalPages / args.days
        fileTable.append(['Pages/Day', round(pagesPerDay)])

    print(tabulate(fileTable, headers=['File', 'Pages']))

def count_pages(filePath):
    """
    Gets the amount of pages of the given pdf file.
    :param fileName: The file name
    :return: The amount of pages
    """
    file = open(filePath, 'rb')
    reader = PyPDF2.PdfFileReader(file)
    return reader.numPages

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='pdfpc',
                                     description='A simple script to count the total amount of pages of multiple PDFs files.')
    parser.add_argument('-d', '--dir', type=str, nargs='?', default=os.getcwd(),
                        help='An optional directory path to look for PDFs. Default is cwd.')
    parser.add_argument('days', metavar='days', type=int, nargs='?',
                        help='The amount of available days to study the PDFs.')
    main(parser.parse_args())
