import glob
from pdfminer.high_level import extract_text
import re


path = 'pdfs' # use your path
all_files = glob.glob(path + "/*.pdf")
total = len(all_files)
count = 1
tester = 0
key_terms = ["alzheimer’s", "dementia"]
dates_list = []
occurence_list = []
cognition_list = []
status_list = []
positive_decision_list = []
decision_date_list = []
for file in all_files[200:250]:

    print(f" Processing {count} of {total} document: {file}")
    count += 1
    text = extract_text(file)
    text = text.lower()
    # print(text)
    match = re.findall(('request: .+'), text)
    # date = match.replace('request:', "")
    date = [item.replace('request:', "").strip() for item in match]
    # print(f"date : {date}")
    dates_list.append(date)
    # print(text.strip())
    decision_date_match = re.findall(('dated:?\s+albany, new york?\n?\n\d{2}/\d{2}/\d{4}'), text.strip(), flags=re.S)
    decision_date = [item.replace('dated: albany, new york\n\n', "").strip() for item in decision_date_match]
    decision_date_list.append(decision_date)
    print(decision_date_match)
    if len(decision_date_match) == 0:
        tester +=1

print(f"total empties: {tester}")


#
#     decision_keys = [
#     "is not correct and is reversed",
#     "as required by 18 nycrr 358-6.4",
#      "must comply immediately"
#      ]
#     # print(decision_keys)
#     appeals_list =[]
#     for decision in decision_keys:
#         appeal_decision = text.count(decision)
#         appeals_list.append(appeal_decision)
#     # print(appeals_list)
#     if any(appeals_list) == True:
#         positive = True
#     else:
#         positive = False
#     positive_decision_list.append(positive)
#
#
#     # print(file)
#     # print(text)
#     for sentence in file:
# #         print(sentence)
#         occurence = [sentence + '.' for sentence in text.split('.') if "dementia" in sentence or "alzheimer’s" in sentence]
#         cognition = [True]
#     #         print(case)
#     #         print(len(case))
#         if len(occurence) == 0:
#             cognition = [False]
#             occurence = ["NO OCCURENCES"]
#     occurence_list.append(occurence)
#     cognition_list.append(cognition)
#

#
# print(dates_list)
# print(occurence_list)
# print(cognition_list)
# print(positive_decision_list)
print(decision_date_list)
