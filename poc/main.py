from pprint import pprint
from lxml import etree
import random
import numpy as np
import networkx as nx
import node2vec
from gensim.models import Word2Vec


def set_style(elem, key, value):
    s = elem.get('style').split(';')
    for i, ss in enumerate(s):
        sss = ss.split(':')
        if sss[0].strip() == key:
            s[i] = sss[0] + ':' + value
    elem.set('style', ';'.join(s))


def add_line(g, x1, y1, x2, y2):
    # <line x1="0" y1="0" x2="200" y2="200" style="stroke:rgb(255,0,0);stroke-width:2" />
    new_line = etree.Element('line')
    new_line.set('x1', str(x1))
    new_line.set('y1', str(y1))
    new_line.set('x2', str(x2))
    new_line.set('y2', str(y2))
    new_line.set('style', 'stroke:rgb(50,50,50);stroke-width:1')
    g.append(new_line)
    return new_line


def add_text(g, x, y, txt):
    # <text x="0" y="35" font-family="Verdana" font-size="35">Hello, out there</text>
    t = etree.Element('text')
    t.text = txt
    t.set('x', str(x))
    t.set('y', str(y))
    t.set('font-size', '1')
    g.append(t)
    return t


def add_circle(g, x, y, txt):
    # <circle xmlns="http://www.w3.org/2000/svg" style="" id="path4612" cx="23.718006" cy="37.802826" r="1.0394346" sender="A" recipient="B"/>
    c = etree.Element('circle')
    c.set('style',
          'fill:green;fill-opacity:1;stroke:none;stroke-width:0.03527778;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1')
    c.set('cx', str(x))
    c.set('cy', str(y))
    c.set('r', str(1))
    g.append(c)


def div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return a


class LinearRegression:
    # https://machinelearningmastery.com/implement-simple-linear-regression-scratch-python/
    # Calculate the mean value of a list of numbers
    def __init__(self, mail_set):
        self.x0 = 2
        self.x1 = 200
        self.b0 = 0
        self.b1 = 0

        coords = []
        for m in mail_set:
            coords.append([1 * mails[m].x, mails[m].y])
        try:
            self.b0, self.b1 = self._coefficients(coords)
        except ZeroDivisionError:
            pass

    def draw_ideal(self, name):
        ll = add_line(cgroup,
                      self.x0, self.predict(self.x0),
                      self.x1, self.predict(self.x1))
        set_style(ll, 'stroke', 'red')
        add_text(cgroup, self.x1, self.predict(self.x1), name)
        ll.set('person', name)

    def _mean(self, values):
        return sum(values) / float(len(values))

    # Calculate covariance between x and y
    def _covariance(self, x, mean_x, y, mean_y):
        covar = 0.0
        for i in range(len(x)):
            covar += (x[i] - mean_x) * (y[i] - mean_y)
        return covar

    # Calculate the variance of a list of numbers
    def _variance(self, values, mean):
        return sum([(x - mean) ** 2 for x in values])

    # Calculate coefficients
    def _coefficients(self, dataset):
        x = [row[0] for row in dataset]
        y = [row[1] for row in dataset]
        x_mean, y_mean = self._mean(x), self._mean(y)
        b1 = self._covariance(x, x_mean, y, y_mean) / self._variance(x, x_mean)
        b0 = y_mean - b1 * x_mean
        return [b0, b1]

    def predict(self, x):
        return self.b0 + self.b1 * x

    def dist_to_line(self, x, y):
        b0_ = y + (x / self.b1)
        x1 = (self.b1 * (self.b0 - b0_)) / (np.square(self.b1) - 1)
        y1 = self.b1 * x1 + lr.b0
        return np.sqrt(np.square(x - x1) + np.square(y - y1)), x1, y1


class Person:
    def __init__(self, svg, xml_elem, pid, centroid_with_inbox=False, live_update=False):
        self.svg = svg
        self.e = xml_elem
        self._centroid_with_inbox = centroid_with_inbox
        self.live_update = live_update

        def r():
            return random.randint(0, 255)

        self.name = xml_elem.get('person')
        self.id = pid
        self.x = float(xml_elem.get('cx'))
        self.y = float(xml_elem.get('cy'))
        self.sen = []
        self.rec = []
        self.to = set()
        self.fr = set()
        self.colour = '#%02X%02X%02X' % (r(), r(), r())

        set_style(self.e, 'fill', self.colour)
        self.t = add_text(svg.getroot(), self.x, self.y, self.name + '-'+str(self.id))
        self.lines_in = []
        self.lines_out = []

        self.centroid = [0, 0]

    def __str__(self):
        rep = '== Person: %s-%s (%.3f, %.3f)\n' % (self.id, self.name, self.x, self.y)
        rep += ' > Sent: %s\n > Received: %s\n' % (self.sen, self.rec)
        rep += ' > To: %s\n > From: %s' % (self.to, self.fr)
        return rep

    def set_pos(self, x, y):
        self.e.set('cx', str(x))
        self.e.set('cy', str(y))
        self.t.set('x', str(x))
        self.t.set('y', str(y))
        for li in self.lines_in:
            li.set('x2', str(x))
            li.set('y2', str(y))
        for li in self.lines_out:
            li.set('x1', str(x))
            li.set('y1', str(y))
        self.x = x
        self.y = y

    def _calculate_centroid(self):
        x = 0.0
        y = 0.0
        pm = self.sen + self.rec if self._centroid_with_inbox else self.sen
        for m in pm:
            x += mails[m].x
            y += mails[m].y
        self.centroid = [div(x, len(pm)), div(y, len(pm))]

    def pos_to_centroid(self, calculate_centroid=False):
        if calculate_centroid:
            self._calculate_centroid()
        self.set_pos(self.centroid[0], self.centroid[1])

    def add_mail(self, m, is_sender=False):
        if is_sender:
            self.sen.append(m.id)
            self.to.add(m.recipient)
        else:
            self.rec.append(m.id)
            self.fr.add(m.sender)

        if self.live_update:
            self._calculate_centroid()
            self.pos_to_centroid()


class Mail:
    def __init__(self, svg, mail_xml):
        self.svg = svg
        self.e = mail_xml
        self.id = self.e.get('id')
        self.sender = mail_xml.get('sender')
        self.recipient = mail_xml.get('recipient')
        self.x = float(mail_xml.get('cx'))
        self.y = float(mail_xml.get('cy'))

        sender = people[self.sender]
        recipient = people[self.recipient]
        set_style(self.e, 'fill', sender.colour)
        sender.add_mail(self, is_sender=True)
        recipient.add_mail(self, is_sender=False)

        if sender == '2482':
            set_style(self.e, 'fill-opacity', '0.8')
        #else:
        #    set_style(self.e, 'fill-opacity', '0.1')

        d = G.get_edge_data(sender.id, recipient.id)
        if d is not None:
            G[sender.id][recipient.id]['weight'] = d['weight'] + 1
        else:
            G.add_edge(sender.id, recipient.id, weight=1)


if __name__ == '__main__':
    xml = etree.parse('init.svg')

    cgroup = xml.find("/{http://www.w3.org/2000/svg}g[@id='connections']")
    pgroup = xml.findall("/{http://www.w3.org/2000/svg}g[@id='people']/*")
    mgroup = xml.findall("/{http://www.w3.org/2000/svg}g[@id='mails']/*")

    people = {}
    people_map = {}
    mails = {}
    G = nx.DiGraph()

    # read people from SVG
    for i, p in enumerate(pgroup):
        people[p.get('person')] = Person(xml, p, i, centroid_with_inbox=False)
        people_map[i] = p.get('person')

    # read mails from SVG
    for e in mgroup:
        mails[e.get('id')] = Mail(xml, e)

    # init people positions
    for name, p in people.items():
        p.pos_to_centroid(calculate_centroid=True)

    Gu = G.to_undirected()
    # draw connections between people
    for a, b in Gu.edges:
        a = people[people_map[a]]
        b = people[people_map[b]]
        w = Gu.get_edge_data(a.id, b.id)['weight']
        if len(b.sen) > 1 and len(a.sen) > 1:
            line = add_line(cgroup, a.x, a.y, b.x, b.y)
            set_style(line, 'stroke-width', str(0.1*w))
            set_style(line, 'stroke-opacity', '0.3')
            a.lines_out.append(line)
            b.lines_in.append(line)

    for name, p in people.items():
        print(p)

    # draw ideal mail lines
    print('%2s %2s %9s %9s %9s %9s %9s %9s %9s' % ('NM', 'ID', 'dist', 'x1', 'y1', 'x0', 'y0', 'b0', 'b1'))
    for name, p in people.items():
        try:
            lr = LinearRegression(p.sen)
            d, x1, y1 = lr.dist_to_line(p.x, p.y)
            # lr.draw_ideal(p.name)
            # add_circle(xml.getroot(), x1, y1, '')
            print('%2s %2s %9.3f %9.3f %9.3f %9.3f %9.3f %9.3f %9.3f' %
                  (p.name, p.id, d, x1, y1, p.x, p.y, lr.b0, lr.b1))
        except ZeroDivisionError:
            print(p.name, p.id)

    nx_G = G.to_undirected()
    print(nx_G)
    G = node2vec.Graph(nx_G, is_directed=False, p=1, q=1)
    G.preprocess_transition_probs()
    walks = G.simulate_walks(num_walks=10, walk_length=10)  # default 10, 10
    walks = [list(map(str, walk)) for walk in walks]
    model = Word2Vec(walks, size=64, window=10, min_count=0, sg=1, workers=2, iter=2)  # default 128, 10, 0, 1, 2, 1
    model.wv.save_word2vec_format('n2v.emb')
    pprint(G.alias_nodes)
    # pprint(people)
    # pprint(mails)

    # people['A'].set_pos(people['A'].x-10, people['A'].y-10)

    # save
    xml.write('out.svg', pretty_print=True, xml_declaration=True, encoding="utf-8")
