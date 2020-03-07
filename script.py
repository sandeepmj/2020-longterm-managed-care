import glob
from pdfminer.high_level import extract_text
import re


path = 'pdfs' # use your path
all_files = glob.glob(path + "/*.pdf")

key_terms = ["alzheimer’s", "dementia"]
dates_list = []
occurence_list = []
cognition_list = []
status_list = []
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
    for sentence in file:
#         print(sentence)
        occurence = [sentence + '.' for sentence in text.split('.') if "dementia" in sentence or "alzheimer’s" in sentence]
        cognition = [True]
    #         print(case)
    #         print(len(case))
        if len(occurence) == 0:
            cognition = [False]
            occurence = ["NO OCCURENCES"]
    occurence_list.append(occurence)
    cognition_list.append(cognition)

    #         elif "alzheimer’s" in case and "dementia" in case:
    #             status = "ALZ"
    #         elif "alzheimer’s" not in case and "dementia"

    # print(f"status is {status} and sentence is {case}")
    # print(f"{case} in {file}")
print(dates_list)
print(occurence_list)
print(cognition_list)
