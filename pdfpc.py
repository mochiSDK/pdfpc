import os
import argparse
import PyPDF2
from tabulate import tabulate

def main(args):
    if args.range is not None and args.range[0] < 0 or args.range[0] >= args.range[1]:
        parser.error("Invalid range.")
    fileTable = []
    totalPages = 0
    pdfFileCounter = 0
    canAdd = True if args.range is None else False
    for fileName in os.listdir(args.dir):
        if not fileName.endswith('.pdf'):
            continue
        pdfFileCounter += 1
        if pdfFileCounter > args.range[1]:
            break
        if canAdd or pdfFileCounter >= args.range[0] and pdfFileCounter <= args.range[1]:
            # Reconstructing the full file path.
            pages = count_pages(f"{args.dir}{os.path.sep}{fileName}")
            totalPages += pages
            fileTable.append([fileName, pages])

    if pdfFileCounter == 0:
        parser.error("pdfpc: error: No PDF file(s) found in this directory.")

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
    parser.add_argument('-r', '--range', metavar=('start', 'end'), type=int, nargs=2,
                        help='An optional inclusive range to use when considering where to start scanning the files.')
    parser.add_argument('-D', '--days', metavar='days', type=int, nargs='?',
                        help='The amount of available days to study the PDFs.')
    main(parser.parse_args())
