import requests

others = []
found = []
strange = []

def readfile(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        #print line
        check_version(line)


def check_version(site):
    print site.strip() + 'CHANGELOG.txt'
    res = requests.get (site.strip() + 'CHANGELOG.txt', verify=False)
    print res.status_code
    if res.status_code > 200:
        others.append(site)

    if res.status_code == 200:
        print "good"
        match = "Drupal 7.63"
        out = res.text
        if match in out:
            found.append(site)
        else:
            strange.append(site)
        print out.split('\n')[:5]

def main():
    filename = 'sitelist.txt'
    readfile(filename)
    print " Others "
    print others
    print " Found "
    print found
    print " Strange "
    print strange


main()
