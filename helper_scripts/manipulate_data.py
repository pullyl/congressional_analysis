import os, csv
import xml.etree.ElementTree

#helper scripts to manipulate data.  Need to change the following local variables:
vote_repo = "/Users/lauren/Developer/congress-votes-servo"
meta_fields_to_iter = ['majority', 'congress', 'chamber', 'session', 'rollcall-num', 'legis-num', 'vote-question', 'vote-result', 'vote-desc']
all_fields = meta_fields_to_iter + ['file', 'r-y', 'r-no', 'r-p', 'r-nv', 'd-y', 'd-no', 'd-p', 'd-nv', 'ind-y', 'ind-n', 'i-p', 'i-nv', 'category']
export_file = '../raw_data/raw_data.csv'

#TO DO
### Turn rows into a dictionary

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

        # skip if it is not a house bill
        if file.find('/h') == -1:
            print 'skipping %s' % (file)
            continue

        try:
            root = xml.etree.ElementTree.parse(file).getroot()

            l = []

            vote_desc = ''
            for field in meta_fields_to_iter:
                found = False
                for r in root.iter(field):
                    found = True
                    l.append(str(r.text))
                    if field == 'vote-desc':
                        vote_desc = str(r.text)
                if not found:
                    l.append("")

            l.append(file)

            for f in root.iter('totals-by-party'):
                l.append(f[1].text)
                l.append(f[2].text)
                l.append(f[3].text)
                l.append(f[4].text)

            #find category
            category = find_category(vote_desc)
            l.append(category)

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

#categorize based on vote description
def find_category(desc):
    categories = {'gun_control': ['gun'],
                  'health_care': ['affordable care act', 'aca', 'obamacare'],
                  'education': ['school', 'education', 'student'],
                  'immigration': ['immigration'],
                  'budget': ['irs', 'business', 'trade'],
                  'tax': ['tax'],
                  'economy' : ['economy', 'Wall Street'],
                  'military': ['military', 'veteran', 'VA', 'veterans', 'defense', 'iran', 'homeland'],
                  'energy': ['energy', 'pipeline'],
                  'environment': ['environment', 'water'],
                  'infrastructure': ['infrastructure', 'transportation']
                  }

    desc_list = desc.lower().split(' ')

    possible_categories = []
    for cat in categories:
        f = list(set(categories[cat]) & set(desc_list))
        if len(f) > 0:
            possible_categories.append(cat)

    if len(possible_categories) == 0:
        return 'other'

    if len(possible_categories) == 1:
        return possible_categories[0]

    else:
        cat_list = ''
        for cat in possible_categories:
            cat_list += cat + ' '
        print 'returning cat list: %s' % (cat_list)
        return cat_list


main()