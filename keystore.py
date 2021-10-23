import subprocess
#create geth accounts
def local_account_setup(node_count):
    i = 0
    while i < node_count:
        p = subprocess.Popen(['geth','account', 'new','--datadir','./tmp_data', '--password','./password.txt','--keystore','./keystore'])
        subprocess.Popen.wait(p)
        i+=1
    key_list = subprocess.check_output(['ls','./keystore'])
    return key_list.decode('UTF-8')

def import_keyfiles(key_list):
    key_files = str(key_list).splitlines()
    files_obj= []
    new_files_obj = []
    for line in key_files:
        files_obj.append(line)
    i = 0
    for file in files_obj:
        new_file_string = str(8545+i)+".key"
        p = subprocess.Popen(['cp', "./keystore/"+file, "./keystore/"+new_file_string])
        subprocess.Popen.wait(p)
        i+=1
        new_files_obj.append(new_file_string)
    return new_files_obj

#accounts are created
def main():
    key_list = local_account_setup(2)
    return import_keyfiles(key_list)