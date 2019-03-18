# Mercer Assistant
The Mercer Assistant learns text and attempts to write back text, mostly as poetry, in it's current state.

## License
This program falls under the  Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license.

[![Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png "Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)")](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Setup
### Basic Setup
Do this setup first, then any or all of the other setup options to unlock their features.
1. Download Git Repo.
2. Ensure Python 3 is installed.
3. Run 'mainControl.py' to start Mercer.
4. Experiment with the features available and teach Mercer words. A larger dictionary will allow for more accurate generation.

### Reddit Interaction Setup
Allows Mercer to interact (in a read only capacity) with Reddit for learning purposes.
1. Install 'praw' with 'pip install praw'.
2. Go to [Reddit App registration](https://www.reddit.com/prefs/apps/).
3. Create a new app (likely as a script). Keep the page open.
4. Fill in the 'client_id' and the 'client_secret' sections, as shown on the Reddit app page, in the 'praw.ini.TEMPLATE' file.
5. (Optional) Fill in the 'username' and 'password' sections in the 'praw.ini.TEMPLATE' file. This is not required for read-only operations.
6. Rename the 'praw.ini.TEMPLATE' file to 'praw.ini'.

### Web Interaction Setup
Allows Mercer to request information from the web generally for learning purposes.
1. Install 'requests' with 'pip install requests' or 'pipenv install requests'.

## To-Do
* Make Mercer Constants and Settings load from an exterior .ini/.json/.txt/etc file and update them through set functions.
* Allow Mercer to learn through PDFs.
* Allow Mercer to establish the types of words (Noun/Verb/Adj/etc) during its own learning process.
* Utilize word type over commonality to create simple Adjective-Noun-Verb sentences, while using commonality as a backup.