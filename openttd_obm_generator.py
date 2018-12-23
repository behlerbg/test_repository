# ! python3
## openttd_obm_generator.py
## Generates a .obm file for use by OpenTTD from a directory
## Brett Behler 12.20.2018

import hashlib, os

class OBM_File(object):
    def __init__(self):
        self.read_directory()

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def read_directory(self):
        # get list of valid midi files in current directory
        self.name = os.path.split(os.getcwd())[-1]
        i = 0
        self.obm_files_text = ['[files]']
        self.obm_md5s_text = ['[md5s]']
        self.obm_names_text = ['[names]']

        for f in os.listdir('.'):
            if os.path.isfile(f) and f[-4:] == '.mid' or f[-5:] == '.midi':
                extension = os.path.splitext(f)[1]
                if i == 0:
                    prefix = 'theme'
                elif i < 11:
                    prefix = 'old_' + str(i-1)
                elif i < 21:
                    prefix = 'new_' + str((i-1) % 10)
                else:
                    prefix = 'ezy_' + str((i-1) % 10)
                prefix += ' = '
                self.obm_files_text.append(prefix + f)
                self.obm_md5s_text.append(f + ' = ' + self.md5(f))
                # file naming convention XX_track_title_name.mid where XX is the numerical track number
                self.obm_names_text.append(f + ' = ' + ' '.join(f[3:-len(extension)].split('_')).title())
                i += 1
        # if the [files] section is shorter than the required 31 tracks, finish the [files] section.
        if len(self.obm_files_text) - 1 < 31:
            start = len(self.obm_files_text) - 1
            for i in range(start, 31):
                if i == 0:
                    prefix = 'theme'
                elif i < 11:
                    prefix = 'old_' + str(i-1)
                elif i < 21:
                    prefix = 'new_' + str((i-1) % 10)
                else:
                    prefix = 'ezy_' + str((i-1) % 10)
                prefix += ' = '
                self.obm_files_text.append(prefix)


    def create_file(self):
        with open(self.name+'.obm', 'w') as obm_file:
            text = [
                '[metadata]', 
                'name = ' + self.name,
                'shortname = '+ self.name[:4].upper(),
                'version = *',
                'description = *',
                '\n'
                ]
            obm_file.write('\n'.join(text))
            obm_file.write('\n'.join(self.obm_files_text))
            obm_file.write('\n\n')
            obm_file.write('\n'.join(self.obm_md5s_text))
            obm_file.write('\n\n')
            obm_file.write('\n'.join(self.obm_names_text))
            obm_file.write('\n\n')
            obm_file.write('\n'.join(['[origin]', 'default = *']))

if __name__ == '__main__':
    gen_obm = OBM_File()
    gen_obm.create_file()