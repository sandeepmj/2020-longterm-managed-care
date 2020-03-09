import glob
from pdfminer.high_level import extract_text
import re
import os.path
import csv


path = 'pdfs' # use your path
all_files = glob.glob(path + "/*.pdf")
total = len(all_files)
count = 1
tester = 0
key_terms = ["alzheimer’s", "dementia"]
dates_list = []
mentions_list = []
cognition_list = []
status_list = []
positive_decision_list = []
decision_date_list = []
for file in all_files[0:10]:

    print(f" Processing {count} of {total} document: {file}")
    count += 1
    text = extract_text(file)
    text = text.lower()
    # print(text)
    match = re.findall(('request:\s\w+\s\d{0,2},\s\d{4}'), text)
    # date = match.replace('request:', "")
    date = [item.replace('request:', "").strip() for item in match]
    # print(f"date : {date}")
    dates_list.append(date)
    # print(text.strip())
    decision_date_match = re.findall(('dated:?\s+albany, new york?\n?\n\d{2}/\d{2}/\d{4}'), text.strip(), flags=re.S)
    decision_date = [item.replace('dated: albany, new york\n\n', "").strip() for item in decision_date_match]
    decision_date_list.append(decision_date)
    # print(decision_date_match)
    if len(decision_date_match) == 0:
        tester +=1

# print(f"total empties: {tester}")



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
    # print(appeals_list)
    if any(appeals_list) == True:
        positive = True
    else:
        positive = False
    positive_decision_list.append(positive)


    # print(file)
    # print(text)

    for sentence in file:
        ignore = 'it provides, in relevant part:'
#         print(sentence)
        mentions = [sentence + '.' for sentence in text.split('.') if "dementia" in sentence or "alzheimer’s" in sentence and "it provides, in relevant part:a state" not in sentence]
        mentions = [item.replace('\n\n', "").replace('\n', '').strip() for item in mentions]

        if ignore in mentions and len(mentions) >= 1:
            cognition = [False]
            mentions = ["NO OCCURENCES"]
            # print(f"LALALALA {mentions}")
    #         print(case)
    #         print(len(case))
        elif len(mentions) == 0:
            cognition = [False]
            mentions = ["NO OCCURENCES"]

        else:
            cognition = [True]

    mentions_list.append(mentions)
    cognition_list.append(cognition)
    # print(f"HELLLLLLO: {mentions}")

print(dates_list)
# print(mentions_list)
# print(cognition_list)
# print(positive_decision_list)
# print(decision_date_list)

## flatten dates_list which currently is a list with each date as a list. breaking conversion to csv
appeal_dates_list = []
for sublist in dates_list:
    for item in sublist:
        appeal_dates_list.append(item)
# print(appeal_dates_list)

## Flatten lists of lists because causing probkems with reading csv_file_name
# def firstItems(lst):
#     return [item[0] for item in lst]

flat_mentions_list=[]
for alist in mentions_list:
    together = '..........'.join(alist)
    flat_mentions_list.append(together)
# print(flat_mentions_list)

# flat_occurence_list = firstItems(occurence_list)
# print(flat_occurence_list)

flat_decision_date_list = [item for sublist in decision_date_list for item in sublist]
# print(f'Flat decision: {flat_decision_date_list}')

# flat_positive_decision_list = [item for sublist in positive_decision_list for item in sublist]

files_list = [item.replace("pdfs/Redacted_", "") for item in all_files[11:100]]

decisions_dict_list = []
for (file, date_a, date_d, cog, decision, text) in zip(files_list, appeal_dates_list, flat_decision_date_list, cognition_list, positive_decision_list, flat_mentions_list):
    each_decision = {"file_id": file, 'date_appeal': date_a, 'date_decision': date_d, 'cognition_related': cog, "positive_decision": decision, "dementia-related-words": text}
    decisions_dict_list.append(each_decision)
# print(decisions_dict_list)


labels = ["file_id","date_appeal", "date_decision", "cognition_related", "positive_decision", "dementia-related-words" ]

## csv file to be created with data
csv_file_name = "ltmc_decisions.csv"
file_exists = os.path.isfile(csv_file_name)
try:
    with open(csv_file_name, 'a') as file:
        writer = csv.DictWriter(file, fieldnames = labels )

        if not file_exists:
            writer.writeheader()
        for data_row in decisions_dict_list:
            writer.writerow(data_row)

except IOError:
    print("sorry, some error...grrrr")

print(f"CVS file named {csv_file_name} is ready. Find it in your project folder!")
