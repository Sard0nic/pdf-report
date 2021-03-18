from bs4 import BeautifulSoup as bs
import functions as fu
import pandas as pd

# URL to mainpage
url = "https://apym.hcdn.gob.ar/comisiones-especiales/nazis/inventario"

# Loading Site Content
text = fu.loadHTML_JS_New(url)

# Read from textfile
#textfile = open('html.txt')
#text = textfile.read().replace('\n', ' ')
#textfile.close()

# Parse html in text format and pass to bs
fu.startProgress('Parsing html files')
soup = []
i = 0
for list in text:
    soup.append(bs(list, 'lxml'))

    # Progress bar
    pct = int(100 / len(text) * i)
    fu.progress(pct)
    i += 1

fu.endProgress()

# Create List of sections containing a File
fu.startProgress('Filtering content')
j = 0
filediv = []
for site in soup:
    for i in site.findAll('div', class_='col-2-1'):
        filediv.append(i)

    # Progress bar
    pct = int(100 / len(soup) * j)
    fu.progress(pct)
    j += 1

fu.endProgress()

# Initialising lists to store Data
link = []
files = []

# Initialize progress bar for parsing data
fu.startProgress('Parsing data')

y = 0
for div in filediv:
    fileattrs = []
    obj = bs(str(div), 'lxml')
    files.append([])
    for i in obj.findAll('div', class_='blk-1'):
        divt = bs(str(i), 'lxml')
        files[y].append(divt.find('div').text)

    target = obj.find('a', class_='btn-basic')

    if target != None:
        link.append(target.attrs['href'])
    else:
        link.append('-')

    # Calculate percentage
    pct = int(100 / len(filediv) * y)
    fu.progress(pct)

    y += 1

fu.endProgress()

# Adjust links
nlink = []
for item in link:
    if item != '-':
        partial = item.split('/', 2)
        if partial[1] == 'uploads':
            nlink.append('https://apym.hcdn.gob.ar'+item)
        else:
            nlink.append(item)
    else:
        nlink.append(item)

### Creating Dataframe ###

# Generating the list of columns
dfcolumns = []
for file in files:
    for attr in file:
        name, val = attr.split(':\xa0\xa0')
        if name not in dfcolumns:
            dfcolumns.append(name)
dfcolumns.append('Target')

# Create DataFrame
df = pd.DataFrame(columns=dfcolumns)

# Write data to DataFrame
fu.startProgress('Generating dataframe')
i = 0
for file in files:
    for attr in file:
        name, val = attr.split(':\xa0\xa0')
        df.at[i, name] = val

    df.at[i, 'Target'] = nlink[i]

    # Calculate progress in percent
    pct = int(100 / len(files) * i)
    fu.progress(pct)
    i += 1

fu.endProgress()

### Write data to Excel ###
print('Writing data to excel...')
df.to_excel('output.xlsx')
print('Sucessfully safed data in output.xlsx')