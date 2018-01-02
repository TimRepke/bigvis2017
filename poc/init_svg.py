import numpy as np
import pandas as pd
from lxml import etree

xml = etree.parse('empty.svg')

cgroup = xml.find("/{http://www.w3.org/2000/svg}g[@id='connections']")
pgroup = xml.find("/{http://www.w3.org/2000/svg}g[@id='people']")
mgroup = xml.find("/{http://www.w3.org/2000/svg}g[@id='mails']")

df = pd.read_csv('emails.emb2d.csv', escapechar='\\')
rows = df.to_dict(orient='records')
persons = set()
for row in rows:
    row['2d'] = np.fromstring(row['2d'][1:-1], sep=' ')
    row['vec'] = np.fromstring(row['vec'][1:-1], sep=' ')
    persons.add(row['from'])
    persons.add(row['to'])
# df = pd.DataFrame(rows)

vex = np.array([r['2d'] for r in rows])
area = [[vex[:, 0].min(), vex[:, 0].max()],
        [vex[:, 1].min(), vex[:, 1].max()]]

canvas_size = [350, 350]
stretch = [-1*canvas_size[0]/(abs(area[0][0])+abs(area[0][1])),
           -1 * canvas_size[1]/(abs(area[1][0])+abs(area[1][1]))]

person_index = {}
for i, p in enumerate(persons):
    person_index[p] = i

    c = etree.Element('circle')
    c.set('style',
          'fill:#0073ff;fill-opacity:1;stroke:black;stroke-width:0.03527778;'
          'stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1')
    c.set('cx', str(1))
    c.set('cy', str(1))
    c.set('r', str(2))
    c.set('person', str(i))
    c.set('name', p)
    pgroup.append(c)

for row in rows:
    c = etree.Element('circle')
    c.set('style', 'fill:#0073ff;fill-opacity:0.2;stroke:none;')
    c.set('cx', str((row['2d'][0]+area[0][0])*stretch[0]))
    c.set('cy', str((row['2d'][1]+area[1][0])*stretch[1]))
    c.set('r', str(1))
    c.set('sender', str(person_index[row['from']]))
    c.set('recipient', str(person_index[row['to']]))
    c.set('id', row['id'])
    mgroup.append(c)

xml.write('init.svg', pretty_print=True, xml_declaration=True, encoding="utf-8")

# <circle
#        style="fill:#0073ff;fill-opacity:1;stroke:none;stroke-width:0.03527778;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
#        id="path4504"
#        cx="22.2061"
#        cy="13.234371"
#        r="1.984375"
#        person="A" />

# <circle
# style="fill:#00ff7c;fill-opacity:1;stroke:none;stroke-width:0.03527778;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
# id="path4612"
# cx="23.718006"
# cy="37.802826"
# r="1.0394346"
# sender="A"
# recipient="B" />
