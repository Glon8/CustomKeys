import time;
import random;
import threading;
import json;
import os;
import shutil;
import platform

from pynput.mouse import Controller as M, Listener as mL,  Button;
from pynput.keyboard import Controller as K, Listener as kL, HotKey, Key;
from rich.console import Console;

#===================================< PREP
console = Console();
temp_timer = None;

k = K();
m = M();

operations = [
    {
    'name': 'General',
    'note': "display is either 'emoji' or 'plain'",
    'display': 'plain'
    },
    {
        'name': 'Kill Switch',
        'key_trigger': 'c+0',
        'key_action': 'None',
        'stat': 0,
    },
    {
        'name': 'Auto Click Clip',
        'key_trigger': 'c+1',
        'key_action': 'v',
        'mode': 1,
        'mouse': 0,
        'stat': 0,
        'trigger': 0,
        'count': 0,
    },
    {
        'name': 'Smart AFK',
        'key_trigger': 'c+2',
        'key_action': 'None',
        'stat': 0,
        'lock': 0,
        'time': 0,
    },
    {
        'name': 'Quick Insert',
        'key_trigger': 'c+3',
        'key_action': 't',
        'stat': 0,
    },
    {
        'name': 'Saves Snatcher',
        'key_trigger': 'c+4',
        'key_action': 'None',
        'path_from': '',
        'path_to': 'essentials/snatched files',
        'backup_time': -1,
        'dir_files': 0,
        'self_replace': 0,
        'stat': 0,
    },
];

op = operations;
seperator = f"===========================<";
#===================================< SWITCH
# dic - dictionary to use
# key - from the dictionary to flip
def switch(dic, key):
    dic[key] = 1 - dic[key];

#===================================< KEY PRESS
# key - to press
# delay - between press and release
def key_press(key, min_delay, max_delay):
    k.press(key);

    timeout = random.randint(min_delay, max_delay) / 1000;
    time.sleep(timeout);

    k.release(key);

#===================================< READ FILE
# file_path - to read from
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip();
    except FileNotFoundError:
        return None;

#===================================< PATH MTIME
# folder_path - to check mtime for
def dir_mtime(folder_path):
    newest = 0;

    for root, dirs, files in os.walk(folder_path):
        try:
            newest = max(newest, os.path.getmtime(root));
        except OSError:
            pass;

        for file in files:
            path = os.path.join(root, file);
            try:
                mtime = os.path.getmtime(path);
                if mtime > newest:
                    newest = mtime;
            except OSError:
                pass;


    return newest;

#===================================< CONFIG PARSER
# string - to pars in to config
def config_parse(string):
    if string == '' or string is None:
        return;

    config_pack = json.loads(string);

    for ind in range(len(config_pack)):
        for key, val in config_pack[ind].items():
            if key != 'name':
                op[ind][key] = val;

#===================================< FILES COUNT
def files_count(file_path):
    return sum(len(files) for _, _, files in os.walk(file_path));

#===================================< VISUALS
def render():
    if platform.system() == 'Windows':
        os.system('cls');
    else:
        os.system('clear');

    pos = 'on' if op[0]['display'] == 'plain' else chr(0x2705);
    neg = 'off' if op[0]['display'] == 'plain' else chr(0x274C);

    for thing in op:
        for att, stat in thing.items():
            if att == 'name':
                console.print(seperator + ' ' + str(stat));
            elif att == 'key_action' or att == 'key_trigger' or att == 'text' or att == 'path_from' or att == 'path_to' or att == 'note' or att == 'display' or att == 'dir_files':
                console.print(f"{att} : {stat}");
            elif att == 'count':
                console.print(f"{att} : {int(stat)} clicks");
            elif att == 'time':
                time_seconds = stat % 60;
                console.print(f"{att} : {int((stat-time_seconds)/60)} minutes {int(time_seconds)} seconds");
            elif att == 'backup_time':
                if stat == -1:
                    console.print(f"{att} : {stat}");
                else:
                    console.print(f"{att} : {time.ctime( stat )}");
            else:
                console.print(f"{att} : { pos if stat else neg}");

#===================================< KILL SWITCH
def ks_switch():
    ks = op[1]['stat'];
    acc = op[2];
    afk = op[3];

    acc['stat'] = 0;
    op[4]['stat'] = 0; # qi
    op[5]['stat'] = 0;

    switch(op[1], 'stat');

    if ks:
        acc['count'] = 0;
        afk['time'] = 0;
    else:
        afk.update({'stat': 0, 'lock': 0});

    render();

#===================================< AUTO CLICK CLIP
def acc_switch():
    ks = op[1]['stat'];
    acc = op[2];

    switch(op[2], 'stat');

    if acc['mouse'] == 0:
        acc['trigger'] = 0;
    else:
        switch(op[2], 'trigger');

    if ks:
        render();

    if acc['stat'] and acc['mode']:
        acc['count'] = 0;

    # to use just switch, flip trigger and stat together!

def acc_handler():
    ks = op[1]['stat'];
    acc = op[2];

    if ks and acc['stat']:
        switch(acc, 'trigger');
        render();

def acc_prot():
    acc = op[2];

    if acc['stat'] and acc['trigger']:
        if acc['mouse'] == 0:
            key_press(acc['key_action'], 37, 50);
        else:
            m.click(Button.left);

        if acc['mode'] and acc['count'] < 20:
            op[2]['count'] += 1;

    if acc['mode'] and acc['trigger'] and acc['count'] >= 20:
        if acc['mouse'] == 1:
            switch(acc, 'stat');
        switch(acc, 'trigger');
        render();
        acc['count'] = 0;
    else:
        timeoutNd = random.randint(90, 111) / 1000;
        time.sleep(timeoutNd);

#===================================< SMART AFK
def smartAFK_switch():
    ks = op[1]['stat'];
    afk = op[3]['stat'];

    switch(op[3], 'stat');

    if afk:
        op[3]['lock'] = 0;

    if ks:
        render();

def afk_reset_timer():
    afk = op[3];
    global temp_timer;

    minute = 60;

    keys = ['w', 'a', 's', 'd'];
    interactions = random.randint(2,6);

    console.print(seperator + f' Keys Auto AFK Sequence');

    for i in range(interactions):
        rand_key = random.randint(0,3);

        key_press(keys[rand_key], 178, 300);

        timeoutNd = random.randint(178, 300) / 1000;
        time.sleep(timeoutNd);


    if afk['stat'] and afk['lock']:
        op[3]['time'] = random.randint(int(2 * minute), int(3.5 * minute));

        render();

        temp_timer = threading.Timer(op[3]['time'], afk_reset_timer);
        temp_timer.start();

def smartAFK_prot():
    afk = op[3];
    global temp_timer;

    minute = 60;

    if afk['stat'] and not afk['lock']:
        op[3]['lock'] = 1;
        op[3]['time'] = random.randint(int(2 * minute), int(3.5 * minute));

        render();

        temp_timer = threading.Timer(op[3]['time'], afk_reset_timer);
        temp_timer.start();
    elif not afk['stat'] and temp_timer and temp_timer.is_alive():
            temp_timer.cancel();
            op[3]['lock'] = 0;

#===================================< QUICK INSERT
def qi_switch():
    ks = op[1]['stat'];

    switch(op[4], 'stat');

    if ks:
        render();

def qi_prot():
    qi = op[4];

    text = read_file('essentials/quick insert text.txt');

    if text is None or text == '':
        text = 'Hello There!'

    if qi['stat']:
        render();

        key_press(qi['key_action'], 178, 250);

        for char in text:
            if qi['stat'] == 0:
                break;

            key_press(char,178, 250);

        key_press(Key.enter, 178, 250);

        qi['stat'] = 0;

        render();

#===================================< SAVES SNATCHER
def snt_switch():
    ks = op[1]['stat'];

    switch(op[5], 'stat');

    if ks:
        render();

def snt_prot():
    snt = op[5];

    if snt['stat']:
        p_from = snt['path_from'];
        p_to = snt['path_to'];
        # raw dst name
        dst_name = os.path.basename(p_from.rstrip('\\/'));
        # edited destination
        dst_path = os.path.join(p_to, dst_name);

        if p_from != '' and os.path.exists(p_from) and os.path.exists(p_to):
            # mtime of the origins + inner files check
            new_time = dir_mtime(p_from);
            new_count = files_count(p_from);

            if new_time > snt['backup_time'] and new_count > snt['dir_files']:
                # slight delay < game has a delay between ~0 to 3 seconds to overwrite
                time.sleep(3);
                # delete old backed file
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path);
                # copy creation
                shutil.copytree(p_from, dst_path, dirs_exist_ok=True);
                # time update
                snt['backup_time'] = new_time;
                snt['dir_files'] = new_count;
                render();

        # self_replace - ll replace the backed up, in to original folder
        if snt['self_replace']:
            # check if backup has files
            backup = files_count(dst_path);
            # files count in original folder
            origin = files_count(p_from);
            # mtime check may break, flag may be needed!
            if (not os.path.exists(p_from) or origin == 0 or origin < backup) and (os.path.exists(dst_path) and backup > 0):
                # slight delay < game may delete files to rewrite < may trigger a loop
                time.sleep(0.3)
                # double check files count in original folder
                origin = files_count(p_from);
                # if folder size stays the same then copy
                if origin == origin:
                    # copy creation
                    shutil.copytree(dst_path, p_from, dirs_exist_ok=True);

#===================================< CONTROL PANNEL
def control_panel():
    while True:
        if op[1]['stat']:
            acc_prot();
            smartAFK_prot();
            qi_prot();
            snt_prot();

#===================================< MAIN
def main():
    config_parse(read_file('essentials/config.txt'));

    # \/===================================< HOTKEYS SETTINGS
    def mouse_click(x, y, button, pressed):
        if button == Button.left and pressed:
            if op[2]['mouse'] == 0:
                acc_handler();

    hotkeys = [
        HotKey(HotKey.parse(op[1]['key_trigger']), ks_switch),
        HotKey(HotKey.parse(op[2]['key_trigger']), acc_switch),
        HotKey(HotKey.parse(op[3]['key_trigger']), smartAFK_switch),
        HotKey(HotKey.parse(op[4]['key_trigger']), qi_switch),
        HotKey(HotKey.parse(op[5]['key_trigger']), snt_switch),
    ];

    def on_press(key):
        for thing in hotkeys:
            thing.press(key);

    def on_release(key):
        for thing in hotkeys:
            thing.release(key);
    # /\===================================< HOTKEYS SETTINGS

    render();

    with kL(on_press=on_press, on_release=on_release), mL(on_click=mouse_click):
        control_panel();

#===================================< MAIN START
if __name__ == '__main__':
    main();