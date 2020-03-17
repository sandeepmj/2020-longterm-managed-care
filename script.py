## IMPORT LIBRARIES

import glob
from pdfminer.high_level import extract_text
import re
import os.path
import csv

## IMPORT PDFs
path = 'pdfs' # use your path
all_files = glob.glob(path + "/*.pdf")

## track how many PDFs for counters
total = len(all_files)
count = 1
tester = 0



## key words to search
key_terms = ["alzheimer’s", "dementia"]

## LIST OF DICTIONARIES
dates_list = []
mentions_list = []
cognition_list = []
status_list = []
positive_decision_list = []
decision_date_list = []
s_care_bool = []
twenty_four_care_bool =[]

## how many PDFs to process
start = 0
end = 10
process_num = end - start

## Process PDFs
for file in all_files[start:end]:
    ## counters
    print(f" Processing {count} of {process_num} document: {file}")
    count += 1

    ## extract text from PDFs
    text = extract_text(file)
    text = text.lower()

    ## Matches dates of appeals request
    match = re.findall(('request:\s\w+\s\d{0,2},\s\d{4}'), text)
    # date = match.replace('request:', "")

    ## LC (list comprehension to create list of stripped down dates)
    date = [item.replace('request:', "").strip() for item in match]

    ## append to list of lists
    dates_list.append(date)

    ## Find decision date
    decision_date_match = re.findall(('dated:?\s+albany, new york?\n?\n\d{2}/\d{2}/\d{4}'), text.strip(), flags=re.S)
    ## LC to create decision date list
    decision_date = [item.replace('dated: albany, new york\n\n', "").strip() for item in decision_date_match]

    ## Some dates don't follow regex pattern by going to next line.
    ## Convert any entries with no date to Date off page
    if len(decision_date) == 0:
        decision_date = ["Date off Page"]

    decision_date_list.append(decision_date)
    # print(decision_date_match)
    ## NOT SURE WHY I ADDED THIS - perhaps in case no match found to begin with in a PDF
    if len(decision_date_match) == 0:
        tester +=1

### Checks if split care was requested
    s_care_request = []
    split_hours = "split-shift care"
    s_care = text.count(split_hours)
    s_care_request.append(s_care)
    if any(s_care_request) == True:
        print("split care found")
        split_care = True
    else:
        split_care = False
    s_care_bool.append(split_care)

## checks if 24-hour care was requested
    care24_request = []
    twofour_hours = "24-hour care"
    twofour_care = text.count(twofour_hours)
    care24_request.append(twofour_care)
    if any(care24_request) == True:
        print("24 hour care found")
        twenty_four_care = True
    else:
        twenty_four_care = False
    twenty_four_care_bool.append(split_care)


## Appeals decision

## Look for these phrases
    decision_keys = [
    "is not correct and is reversed",
    "was not correct and is reversed",
    "as required by 18 nycrr 358-6.4",
     "must comply immediately"
     ]
    # print(decision_keys)

## if the phrase appears, put in list
## if they appear 1 or more times, make it true otherwise false.
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
## Check to see if alzheimer's or dementia related.
## need to ignore some mentions of ALZ and Dementia because in boilerplate notice
## Notice begins with what is in ignore variable
## if both either word is found in sentence that begins with Ignore, it removes that sentence from mentions
    for sentence in file:
        ignore = 'it provides, in relevant part'
#         print(sentence)
        mentions = [sentence + '.' for sentence in text.split('.') if "dementia" in sentence or "alzheimer’s" in sentence and "it provides, in relevant part:a state" not in sentence]
        mentions = [item.replace('\n\n', "").replace('\n', '').strip() for item in mentions]
    # print(mentions)
    # print(len(mentions))
    for mention in mentions:
        if ignore in mention:
            mentions.remove(mention)
                # print(mention)
    if len(mentions) == 0:
        cognition = [False]
        mentions = ["NO OCCURENCES"]

    else:
            cognition = [True]

    mentions_list.append(mentions)
    cognition_list.append(cognition)
    # print(f"HELLLLLLO: {mentions}")

## test printing all the lists
# print(dates_list)
# print(mentions_list)
# print(cognition_list)
# print(positive_decision_list)
# print(decision_date_list)

## flatten dates_list which currently is a list with each date as a list. breaking conversion to csv
# appeal_dates_list = []
# for sublist in dates_list:
#     for item in sublist:
#         appeal_dates_list.append(item)

        ## LC version:
appeal_dates_list = [item for sublist in dates_list for item in sublist]
print(appeal_dates_list)

## Flatten lists of lists because causing probkems with reading csv_file_name


# flat_mentions_list=[]
# for alist in mentions_list:
#     together = '..........'.join(alist)
#     flat_mentions_list.append(together)
## LC version:
flat_mentions_list = ['..........'.join(alist) for alist in mentions_list]

# print(flat_mentions_list)

# flat_occurence_list = firstItems(occurence_list)
# print(flat_occurence_list)

flat_decision_date_list = [item.strip().replace("dated:\n\nalbany, new york\n\n", "") for sublist in decision_date_list for item in sublist]
# print(f'Flat decision: {flat_decision_date_list}')


## TURN OFF breaks csv builder
##flat_positive_decision_list = [item for sublist in positive_decision_list for item in sublist]

## Simply removes the folder and redacted file name on pdf file names
files_list = [item.replace("pdfs/Redacted_", "") for item in all_files[start:end]]

## Zip various lists into dictionary
decisions_dict_list = []
for (file, date_a, date_d, cog, decision, split, twenty4, text) in zip(files_list, appeal_dates_list, flat_decision_date_list, cognition_list, positive_decision_list, s_care_bool, twenty_four_care_bool, flat_mentions_list):
    each_decision = {"file_id": file, 'date_appeal': date_a, 'date_decision': date_d, 'cognition_related': cog, "positive_decision": decision, "split_care": split, "24_hour_care": twenty4, "dementia-related-words": text}
    decisions_dict_list.append(each_decision)
# print(decisions_dict_list)
# print(s_care_bool)
# print(twenty_four_care_bool)

labels = ["file_id","date_appeal", "date_decision", "cognition_related", "positive_decision", "split_care", "24_hour_care", "dementia-related-words"]

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
