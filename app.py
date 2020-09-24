import praw
import msvcrt
import webbrowser
import time
from sys import argv
from os import path, system
from colorama import Fore, Back, Style
from helpers import Wrapper
from helpers import Logger
from helpers import TextEditor
logger = Logger()
# Your reddit agent, update with your own bot
agent = praw.Reddit(client_id='',
                     client_secret='',
                     password='',
                     user_agent='',
                     username='')

# List of subreddits to go through
# Here is some sample subreddits
SUBREDDITS          = ["UnethicalLifeProTips", "ShittyLifeProTips", "IllegalLifeProTips"]

# Words that you put in this list will be erased from the post title
# Sample words to erase
BLACKLISTED_WORDS   = [
    'ULPT',
    'SLPT',
    'ILPT',
    ':'
]

class Post(object):
    def __init__(self, id, title, body):
        self.id         = id
        self.title      = title
        self.body       = body

def Editor():
    _posts_json      = Wrapper().read_json(Wrapper().postsPath)
    _editor_json        = Wrapper().read_json(Wrapper().EditedPath)
    _blacklists_json    = Wrapper().read_json(Wrapper().BlacklistPath)

    if not len(_posts_json) == 0:
        while True:
            #Start the editor from the last post edited
            for i in _posts_json['posts'][int(_editor_json['increment']):]:

                clear_console()
                print ( f'{Back.MAGENTA}{Fore.BLACK}EDITOR{Style.RESET_ALL}')
                print (f'{Fore.GREEN}{_editor_json["increment"] + 1}{Style.RESET_ALL} / {_posts_json["total"]}')
                print()
                print(f'{Fore.GREEN}TITLE : {Fore.WHITE}{i["title"]}')
                print(f'{Fore.GREEN}BODY  : {Fore.WHITE}{i["body"]}')
                print()

                print(Fore.MAGENTA + f'{"ENTER":6}' + Fore.WHITE + ': ' + Fore.YELLOW + 'Continue' + '   ' +  Fore.RED +f'{"Q":<6}' + Fore.WHITE + ': ' + Fore.YELLOW + 'Quit')
                print(Fore.MAGENTA + f'{"SPACE":6}' + Fore.WHITE + ': ' + Fore.YELLOW + 'EDIT' + '       ' +  Fore.RED +f'{"U":<6}' + Fore.WHITE + ': ' + Fore.YELLOW + 'Open URL')
                print(Fore.MAGENTA + f'{"ESC":6}' + Fore.WHITE + ': ' + Fore.YELLOW + 'Remove' + Style.RESET_ALL)

                print(f' # ')
                while True:
                    keypress = ord(msvcrt.getch())
                    if keypress == 113:     # Q
                        exit()
                    elif keypress == 117:   # U
                        webbrowser.open_new_tab(i['body'])
                    elif keypress == 13:    # Enter
                        break
                    elif keypress == 32:    # Space bar
                        te = TextEditor()
                        if (te.edit(
                            Post(
                                i['id'],
                                i['title'],
                                i['body']
                            ))):
                            break
                    elif keypress == 27:    # Escape
                        _blacklists_json.append(
                            {
                                'id': i['id']
                            }
                        )
                        _editor_json['blacklisted'] += 1
                        Wrapper().write_json(Wrapper().BlacklistPath, _blacklists_json)

                        # Remove the post from the json
                        for j in _posts_json['posts']:
                            if j['id'] == i['id']:
                                _posts_json['posts'].remove(j)
                                _posts_json['total'] -= 1
                                _editor_json['increment'] -= 1;
                                break

                        Wrapper().write_json(Wrapper().postsPath, _posts_json)

                        break

                _editor_json['increment'] += 1
                Wrapper().write_json(Wrapper().EditedPath, _editor_json)
                clear_console()
            logger.log('All popsts has been evaluated', 2)
            break
    else:
        logger.log('posts.json is empty', 3)
            
#Scrape posts from all subreddits in list
def App(_limit):
    # We need to store the jsons from when this function is called so we can compare and check if post is valid or not
    _posts_json                 = Wrapper().read_json(Wrapper().postsPath)
    blacklist_json              = Wrapper().read_json(Wrapper().BlacklistPath)


    for i in SUBREDDITS:
        subreddit = agent.subreddit(i)
        for j in subreddit.top(limit=_limit):
            _post = Post(
                j.id,
                replace_all(j.title),
                j.selftext if j.is_self else j.url
            )

            if not post_valid(_posts_json['posts'],blacklist_json, _post.id):
                continue
            logger.log(_post.id, 4)
            Wrapper().append_post(_post)

def main():
    try:
        clear_console()
        if ('-e' in argv or '--editor' in argv):
            Editor()
        else:
            count = 10
            try:
                count = int(argv[1])
            except:
                pass
            start_time = time.time()
            App(count)
            logger.log('Execution time: ' + str(round(time.time() - start_time,4)) + ' s')
    finally:
        TextEditor().stop()

# If post is already stored skip it
# We pass the json in since we dont want to repeat the progress
def post_valid(_posts, _blacklist,id):
    for i in _posts:
        if 'id' in i.keys():
            if i['id'] == id:
                logger.log(f'{id} - post is already stored', 3)
                return False
    for i in _blacklist:
        if 'id' in i.keys():
            if i['id'] == id:
                logger.log(f'{id} - post is blacklisted', 3)
                return False
    return True

def clear_console():
    system('cls')

def replace_all(text):
    for i in BLACKLISTED_WORDS:
        text = text.replace(i, '')
    text = text.strip()
    return text


if __name__ == "__main__":
    main()