import glob
from pdfminer.high_level import extract_text


path = 'pdfs' # use your path
all_files = glob.glob(path + "/*.pdf")

for file in all_files:
    text = extract_text(file)
    print(text)
