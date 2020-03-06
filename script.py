import glob
from pdfminer.high_level import extract_text
import re


path = 'pdfs' # use your path
all_files = glob.glob(path + "/*.pdf")

key_terms = ["alzheimer’s", "dementia"]
dates_list = []
case_list = []
cognitive_list = []
for file in all_files:
    text = extract_text(file)
    text = text.lower()
    match = re.findall(('request: .+'), text)
    # date = match.replace('request:', "")
    date = [item.replace('request:', "").strip() for item in match]
    # print(f"date : {date}")
    dates_list.append(date)

    # print(file)
    # print(text)
    if "alzheimer’s" in text:
        print("A-True")
        case = [sentence + '.' for sentence in text.split('.') if "alzheimer’s" in sentence]
    elif "dementia" in text:
        print("M-True")
    else:
        print("false")
    # for term in key_terms:
    #     case = [sentence + '.' for sentence in text.split('.') if term in sentence]
    #     # print(type(case))
    #     # print(len(case))
    #     if len(case) == 0:
    #         cognitive = False
    #         case = "Not cognitive"
    #         case_list.append(case)
    #         cognitive_list.append(cognitive)
    #     else:
    #         cognitive = True
    #         case_list.append(case)
    #         cognitive_list.append(cognitive)
    # print(f"{case} in {file}")
print(dates_list)
print(case_list)
print(cognitive_list)
