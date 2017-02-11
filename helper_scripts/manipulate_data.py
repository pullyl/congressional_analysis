import os, csv
import xml.etree.ElementTree

#helper scripts to manipulate data.  Need to change the following local variables:
vote_repo = "/Users/lauren/Developer/congress-votes-servo"
meta_fields_to_iter = ['majority', 'congress', 'chamber', 'session', 'rollcall-num', 'legis-num', 'vote-question', 'vote-result', 'vote-desc']
all_fields = meta_fields_to_iter + ['file', 'r-y', 'r-no', 'r-p', 'r-nv', 'd-y', 'd-no', 'd-p', 'd-nv', 'ind-y', 'ind-n', 'i-p', 'i-nv']
export_file = '../raw_data/raw_data.csv'

def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            if filepath.__contains__(".xml"):
                file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

def main():
    # Run the above function and store its results in a variable.
    full_file_paths = get_filepaths(vote_repo)

    count = 0
    export_data = []
    for file in full_file_paths:
        count += 1
        #if count > 100:
        #    break

        if count % 100 == 0:
            print 'analyzing file %d' % (count)

        try:
            root = xml.etree.ElementTree.parse(file).getroot()

            l = []

            for field in meta_fields_to_iter:
                found = False
                for r in root.iter(field):
                    found = True
                    l.append(str(r.text))
                if not found:
                    l.append("")

            l.append(file)

            for f in root.iter('totals-by-party'):
                l.append(f[1].text)
                l.append(f[2].text)
                l.append(f[3].text)
                l.append(f[4].text)

            export_data.append(l)

        except:
            print file

        #print l
    print 'analyzed %d files' % (count)

    #write to file
    f = open(export_file, 'wb')

    s = ""
    for field in all_fields:
        s += '%s|' % (field)
    s += '\n'

    f.write(s)

    for row in export_data:
        s = ""
        for field in row:
            s += '%s|' % (field)
        s += '\n'
        f.write(s)


main()