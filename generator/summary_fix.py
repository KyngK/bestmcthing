import json

with open('./generator/things.json', 'r') as file:
    data = json.load(file)

empty_summaries = 0
fixed = 0
newdata = []

for index, item in enumerate(data):
    if item["summary"] == "":
        empty_summaries += 1
    else:
        summary_list = item["summary"].split(". ", 1)
        if len(summary_list) == 1:
            summary_list = item["summary"].split(".\n", 1)
        item["summary"] = summary_list[0]
        fixed += 1
    newdata.append(item)

# write data to file
with open('./summary_fix.json', 'w') as file:
    json.dump(newdata, file, indent=4)

print(f"Finished!\nEmpty Summaries: {empty_summaries}\nSummaries Fixed: {fixed}")