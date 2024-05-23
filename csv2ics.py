import csv
import sys
import uuid

print("""BEGIN:VCALENDAR
VERSION:2.0
PRODID:bla""")

def conjoin(strings):
    strings = list(strings)
    strings[-1] = "and " + strings[-1]
    return ", ".join(strings)

def reader(file):
    for line in file:
        if '#' in line:
            line = line[:line.index('#')]
        if line.strip() == '':
            continue
        yield line

for record in csv.reader(reader(sys.stdin)):
    record = list(record)
    while len(record) < 4:
        record.append("")
    try:
        date, name, title, cls = record
    except ValueError:
        print(record, file=sys.stderr)
        raise
    if ";" in name:
        names = name.split(";")
        names = [name.strip() for name in names]
        titles = title.split(";")
        titles = [title.strip() for title in titles]
        summ = conjoin(names)
        desc = conjoin(f"{name}, {title}" for (name, title) in zip(names, titles))
    else:
        summ = name
        desc = name
        if title != "": desc += f", {title}"
    cls = cls.strip()
    if cls != "":
        cls = {"OM": "optional memorial", "M": "memorial", "F": "feast", "S": "solemnity"}.get(cls, cls)
        desc += f" ({cls})"
    if date >= "1130": year = 2019
    else: year = 2020
    print(f"""BEGIN:VEVENT
UID:{uuid.uuid4()}
DTSTAMP:20190624T000000Z
DTSTART:{year}{date}
DTEND:{year}{date}
RRULE:FREQ=YEARLY
SUMMARY:{summ}
DESCRIPTION:{desc}
END:VEVENT""")
    
print("""END:VCALENDAR""")
