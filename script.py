import glob
from pdfminer.high_level import extract_text


path = 'pdfs' # use your path
all_files = glob.glob(path + "/*.pdf")

for file in all_files:
    text = extract_text(file)
    # print(file)
    # print(text)
    case = [sentence + '.' for sentence in text.split('.') if 'Alzheimer’s' in sentence]
    print(type(case))
    print(len(case))
    if len(case) == 0:
        pass
    else:
        print(f"{case} in {file}")
