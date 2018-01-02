import os
import json
import pandas as pd


def process_annotation(anno):
    keep = ["Body",
            "Header/Sent/Date",
            "Header/Sent/Time"
            "Header/Person/From",
            "Header/Person/To",
            "Header/Org/From",
            "Header/Org/To"]
    # BelongsTo, Alias

    header = anno['meta']['header']
    dt = header['Date'].split(' ')

    submails = []
    if 'To' not in header:
        return []

    stack = {'from': header['From'], 'to': header['To'].split(','), 'date': ' '.join(dt[1:3]), 'time': dt[4]}
    relevant = sorted([d for d in anno['denotations'] if d['type'] in keep], key=lambda k: k['start'])

    def clean(part):
        for k in part:
            part[k] = part[k].replace('\t', ' ').replace('\n', ' ').strip()
        return part

    def try_unstack(stack):
        if 'from' in stack and 'to' in stack and 'body' in stack:
            for recipient in stack['to']:
                submails.append(clean({'from': stack['from'], 'to': recipient, 'body': stack['body'],
                                       'date': stack.get('date', ''), 'time': stack.get('time', ''),
                                       'origin': header['X-Origin'], 'id': fname[len(basefolder):]}))
            stack = {}
        return stack

    for deno in relevant:
        stack = try_unstack(stack)
        if deno['type'] in ["Header/Person/To", "Header/Org/To"]:
            if 'to' not in stack:
                stack['to'] = [deno['text']]
            else:
                stack['to'].append(deno['text'])
        elif deno['type'] == 'Body':
            stack['body'] = deno['text']
        elif deno['type'] == 'Header/Sent/Date':
            stack['date'] = deno['text']
        elif deno['type'] == 'Header/Sent/Time':
            stack['time'] = deno['text']
        elif deno['type'] in ['Header/Person/From', 'Header/Org/From']:
            stack['from'] = deno['text']
    try_unstack(stack)
    return submails


if __name__ == '__main__':
    mails = []
    basefolder = 'emails/'
    for root, _, files in os.walk(basefolder):
        for file in files:
            if file.endswith('.txt.ann'):
                fname = os.path.join(root, file)
                try:
                    f = open(fname, 'r')
                    mails += process_annotation(json.load(f))
                    f.close()
                except json.decoder.JSONDecodeError:
                    print('Error loading JSON Annotation File: ' + file)
                    raise
    df = pd.DataFrame(mails)
    df.to_csv('emails.csv', escapechar="\\", index=False)
