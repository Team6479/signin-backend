import time

def log(msg: str, fname: str = 'data/dummy_server_log'):
    with open(fname, 'a') as logfile:
        logfile.write(msg + '\n')

def get_user_data(id: int):
    try:
        with open('data/users/' + str(id), 'r') as userfile:
            return {
                'id': id,
                'name': userfile.read()
                }
    except:
        return None

def create_user(id: int, name: str):
    with open('data/users/' + str(id), 'x') as userfile:
        userfile.write(name)

def push_entry(id: int, start: int, end: int):
    log('[' + time.strftime('%Y-%m-%d', time.localtime(start)) + '] ' + str(id) + ' from ' + str(start) + '-' + str(end) + ' (' + str(end - start) + 's)')