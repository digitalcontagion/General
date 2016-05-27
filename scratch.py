testing = [['tewksbury', '', 'address here', '999-999-999', '5', '5000', 'local'], ['tewksbury', '', 'address here', '999-999-999', '5', '5030', 'local']]
import hashlib

h = hashlib.md5()
h.update(b'test')
print(h.hexdigest())
for i in testing:
    print(i)


history = []
base = r'http://discoverpolicing.org/discover/'
uri = r'index.cfm?fa=searchResult&city=&state=&zip=&radius=&agencyType=1&entryEducation=&authorizedFTswornLow=&authorizedFTswornHigh=50&populationLow=&populationHigh=&entryAgeMin=&entryAgeMax=&startingSalaryLow=&startingSalaryHigh=&startrow=1'
seed = base + uri

def opener(seed):
    import urllib
    target = urllib.request.urlopen(seed)
    new_target = target.read()
    output = new_target.decode("utf-8")
    return output

def get_headings(seed):
    from bs4 import BeautifulSoup
    data = opener(seed)
    soup = BeautifulSoup(data, "html.parser")
    table = soup.find("table")
    headings = [th.get_text() for th in table.find("tr").find_all("th")]
    data_headings = headings
    return data_headings

def get_subpages(seed, history):
    from bs4 import BeautifulSoup
    import re
    import html
    print("Getting subpages from:", seed)
    queue = []
    del queue[:]
    tmp = []
    data = opener(seed)
    soup = BeautifulSoup(data, "html.parser")
    table = soup.find("table")
    if seed not in history:
        queue.append(seed)
    else:
        pass
    for row in table.find_all("tr")[1:]:
        links = (row.find_all("td"))

    subpage_regex = re.compile('\"(.*)\"')

    for data in links:
        pages = data.find_all('a', href=True)
    for i in pages:
        tmp.append(str(i))
    for k in tmp:
        stuff = re.findall(subpage_regex, k)
        addition = base + html.unescape(stuff[0])
        if addition not in history:
            queue.append(addition)
        else:
            pass
    get_data(queue, history)

def get_data():
    pass

def write_data():
    #DBStuff
    pass

