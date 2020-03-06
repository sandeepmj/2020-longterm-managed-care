import glob
from pdfminer.high_level import extract_text


path = 'pdfs' # use your path
all_files = glob.glob(path + "/*.pdf")

key_terms = ["dementia", "alzheimer’s"]

for file in all_files:
    text = extract_text(file)
    text = text.lower()
    # print(file)
    # print(text)
    for term in key_terms:
        case = [sentence + '.' for sentence in text.split('.') if term in sentence]
        print(type(case))
        print(len(case))
        if len(case) == 0:
            pass
        else:
            print(f"{case} in {file}")
