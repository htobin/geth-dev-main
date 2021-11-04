import subprocess
import json
#create geth accounts
def local_account_setup(node_count):
    i = 0
    while i < int(node_count):
        p = subprocess.Popen(['geth','account', 'new','--datadir','./tmp_data', '--password','./password.txt','--keystore','./keystore'])
        subprocess.Popen.wait(p)
        i+=1
    key_list = subprocess.check_output(['ls','./keystore'])
    return key_list.decode('UTF-8')

def import_keyfiles(key_list):
    keyfiles = str(key_list).splitlines()
    files_obj= {}
    i = 0
    for file in keyfiles:
        path = "./keystore/"+ file
        d_key = "geth-dev-node_" + str(i)
        try:
            with open(path) as f:
                config_data = json.load(f)
        except OSError:
            print(f"could not open {file} file")
            exit()
        files_obj[d_key] = {
                            "address": str(config_data["address"]),
                            "file": str(file)
                           }
        i+=1
    return files_obj

#accounts are created
def create_keyfile_obj(node_count):
    key_list = local_account_setup(node_count)
    return import_keyfiles(key_list)