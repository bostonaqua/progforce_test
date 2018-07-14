from collections import Counter
mails = []
with open('mbox.txt', 'r') as f:
    for line in f:
        if line.startswith('From: ', 0):
            mail = {}
            mail['from'] = line.split(' ')[1].strip()
        elif line.startswith('Subject: ', 0):
            mail['subject'] = ' '.join(line.split(' ')[1:]).strip()
        elif line.startswith('Date: ', 0) and len(line.split()[1]) == 10:
            mail['date'] = ' '.join(line.split(' ')[1:3])
            mails.append(mail)
for item in mails:
    print(f'{item["from"]} ({item["date"]}): {item["subject"]}')
res = Counter(mail["from"] for mail in mails)
for key, val in res.items():
    print(f'{key}: {val}')
