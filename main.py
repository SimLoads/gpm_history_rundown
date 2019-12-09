import os, sys, time, operator, re, string, shutil, random

def format_name(string, escape):
    if escape:
        rep = dict((re.escape(k), v) for k, v in ascreplacements.items())
        pattern = re.compile("|".join(rep.keys()))
        string = pattern.sub(lambda m: rep[re.escape(m.group(0))], string)
    string = string[4:]
    string = string[:-1]
    return string

def format_listen(value):
    value = value.replace("'", '')
    value = value.replace(")", '')
    return value

def format_artist(artist):
    rep = dict((re.escape(k), v) for k, v in ascreplacements.items())
    pattern = re.compile("|".join(rep.keys()))
    if not not artist:
        if u'\u005C' in artist:
            artist.replace(u'\u005C', '')
    try:
        artist = pattern.sub(lambda m: rep[re.escape(m.group(0))], artist)
    except:
        return False
    return artist

def format_dict_artist(artist):
    artist = str(artist.translate(str.maketrans('', '', string.punctuation))).replace(' ','')
    rep = dict((re.escape(k), v) for k, v in dictreplacements.items())
    pattern = re.compile("|".join(rep.keys()))
    try:
        artist = pattern.sub(lambda m: rep[re.escape(m.group(0))], artist)
    except:
        return False
    return artist

dir = "C://Users//sim03.000//Downloads//gpl//Takeout//Google Play Music//Tracks"

os.chdir(dir)
files = []
dm = {} # song name, play count
ats = {} # song name, artist name
ascreplacements = {
"&#39;": "'", 
'&quot;': '"',
 'â€™': "'", 
 "&amp;": "&", 
 "â€¦": "...", 
 "Ã¸": "ø",
 "Ã–y": "Ö",
 "Ã¤": "ä",
 "âˆ†": "∆",
 "Ã¡": "á",
 "Â£": "£",
 "Ãxa0":"à"
 }

dictreplacements = {
 "∆": "",
 "£": ""
 }

for r, d, f in os.walk(dir):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))
for item in files:
    with open(item, 'r') as cs:
        rd = cs.read()
        rdl = rd.split(',')
        nm = rdl[6].replace('"', '')
        nm = nm.replace('Removed','')
        art = rdl[8].replace('"', '')
        rdl = rdl[-2].replace('"', '')
        dm[nm] = rdl
        ats[nm.strip()] = art


st = sorted(dm.items(), key=operator.itemgetter(1))
tsg = 0
cached = False
if os.path.exists("logs"):
    ch = input("Use cached data? [y/n] ")
    if ch.lower() == "y":
        cached = True
    else:
        shutil.rmtree("logs")
        os.mkdir("logs")
else:
    os.mkdir("logs")
os.chdir("logs")
if not cached:
    for val in st:
        xra = str(val).split(',')
        frmt = format_name(xra[0], True)
        litformat = format_listen(xra[1])
        artist = format_artist(ats.get(frmt))
        if artist == False:
            artist = format_artist(ats.get(format_name(xra[0], False)))
        litformat = int(litformat)
        formatted = ("You listened to %s by %s %d times" %(frmt, artist, litformat))
        try:
            artist_forline = format_dict_artist(artist)
            with open(str(artist_forline + "_dict.txt"), 'a') as x:
                x.write("%s: %s\n" %(frmt, litformat))
        except:
            print("Failure. Skipping song.")
            pass

        if litformat > tsg: tsg, tSong, tArt = litformat, frmt, artist
        print(formatted)

    print("\nYour top song was %s by %s which you listened to %d times." %(tSong, tArt, tsg))

while True: 
    atlk = input("Lookup Artist: ")
    print()
    if atlk == '':
        atlk = random.choice(os.listdir(os.getcwd()))
        print("Artist: %s" %(atlk.replace('_dict.txt', '')))
    else: 
        atlk = (str(format_dict_artist(atlk)) + "_dict.txt") 
    if os.path.exists(atlk):
        print("Title | Listen Count")
        with open(str(atlk), 'r') as st:
            list = st.read()
            print(list)
            print()
    else:
        print("No such dictionary.")


