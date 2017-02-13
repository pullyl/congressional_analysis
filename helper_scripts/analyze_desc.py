import os, csv
import xml.etree.ElementTree

#helper scripts to manipulate data.  Need to change the following local variables:
vote_repo = "/Users/lauren/Developer/congress-votes-servo"
meta_fields_to_iter = ['vote-desc']
export_file = '../raw_data/vote_desc.csv'

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
    export_data = {}
    for file in full_file_paths:
        count += 1
        #if count > 100:
        #     break

        if count % 100 == 0:
            print 'analyzing file %d' % (count)

        # skip if it is not a house bill
        if file.find('/h') == -1:
            print 'skipping %s' % (file)
            continue

        try:
            root = xml.etree.ElementTree.parse(file).getroot()

            vote_desc = ''
            for field in meta_fields_to_iter:
                found = False
                for r in root.iter(field):
                    vote_desc = str(r.text).lower().split(' ')
                    for desc in vote_desc:
                        if desc in export_data.keys():
                            export_data[desc] += 1
                        else:
                            export_data[desc] = 1

        except:
            print file

    print 'analyzed %d files' % (count)

    #write to file
    f = open(export_file, 'wb')

    s = ""
    for field in export_data.keys():
        s += '%s|%d\n' % (field, export_data[field])

    print s

    f.write(s)

    print 'wrote output'


main()