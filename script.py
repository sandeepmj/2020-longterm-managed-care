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
positive_decision_list = []
for file in all_files[:10]:
    print(f"Processing document {file}")
    text = extract_text(file)
    text = text.lower()
    match = re.findall(('request: .+'), text)
    # date = match.replace('request:', "")
    date = [item.replace('request:', "").strip() for item in match]
    # print(f"date : {date}")
    dates_list.append(date)

    decision_keys = [
    "is not correct and is reversed",
    "as required by 18 nycrr 358-6.4",
     "must comply immediately"
     ]
    # print(decision_keys)
    appeals_list =[]
    for decision in decision_keys:
        appeal_decision = text.count(decision)
        appeals_list.append(appeal_decision)
    print(appeals_list)
    if any(appeals_list) == True:
        positive = True
    else:
        positive = False
    positive_decision_list.append(positive)


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


#
print(dates_list)
print(occurence_list)
print(cognition_list)
print(positive_decision_list)
