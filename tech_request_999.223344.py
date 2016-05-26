from bs4 import BeautifulSoup
import urllib
from urllib import request
import xlwt
import time
import re
import os
import html
from pprint import pprint
wb = xlwt.Workbook()
ws = wb.add_sheet('a test sheet')
history = []
base = r'http://discoverpolicing.org/discover/'
uri = r'index.cfm?fa=searchResult&city=&state=&zip=&radius=&agencyType=1&entryEducation=&authorizedFTswornLow=&authorizedFTswornHigh=50&populationLow=&populationHigh=&entryAgeMin=&entryAgeMax=&startingSalaryLow=&startingSalaryHigh=&startrow=1'
seed = base + uri

def get_headings(seed):
    target = urllib.request.urlopen(seed)
    new_target = target.read()
    data = new_target.decode("utf-8")
    soup = BeautifulSoup(data, "html.parser")

    table = soup.find("table")
    headings = [th.get_text() for th in table.find("tr").find_all("th")]
    data_headings = headings
    return data_headings

def get_subpages(seed, history):
    print("Getting subpages from:", seed)
    queue = []
    del queue[:]
    tmp = []
    target = urllib.request.urlopen(seed)
    new_target = target.read()
    data = new_target.decode("utf-8")
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
def get_data(queue, history):
    while True:
        output = []
        for k in queue:
            time.sleep(7)

            print("Processing site:", k)
            target = urllib.request.urlopen(k)
            new_target = target.read()
            data = new_target.decode("utf-8")
            soup = BeautifulSoup(data, "html.parser")

            table = soup.find("table")
            for row in table.find_all("tr")[1:]:
                tmp = [td.get_text() for td in row.find_all("td")]
                output.append(tmp[:-1])

            history.append(k)
        if k == queue[-1]:
            print("Getting additional pages...")
            new_seed = k
        del queue[:]

        print("The queue is: ", len(queue))
        print("Historical sites processed: ", len(history))
        get_subpages(seed=new_seed, history=history)
        return queue, history, output

def writer(output, data_headings):
    outfile = "tech_request_999.223344"
    src = str(os.path.realpath(outfile))
    wb = xlwt.Workbook()
    style = xlwt.XFStyle()
    style.alignment.HORZ_GENERAL = 1
    style.alignment.NOT_SHRINK_TO_FIT = 1
    style.alignment.wrap = 1
    ransom_sheet = wb.add_sheet('data')
    ransom_headers = data_headings
    (x, y) = (0, 0)
    for domain_column in ransom_headers:
       ransom_sheet.write(x, y, domain_column, style=style)
       y += 1
    del (x, y)
    (x, y) = (0, 0)
    for row in output:
       x += 1
       for domain_row_value in row:
           ransom_sheet.write(x, y, domain_row_value, style=style)
           y += 1
       y = 0
    del (x, y)
    wb.save(src + '.xls')


data_headings = get_headings(seed)
queue, history = get_subpages(seed, history)
queue, history, output = get_data(queue, history)
writer(output, data_headings)