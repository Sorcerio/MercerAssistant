# Mercer Assistant
The Mercer Assistant learns text and attempts to write back text, mostly as poetry, in it's current state.

## Setup
## Basic Setup
Do this setup first, then any or all of the other setup options to unlock their features.
1. Download Git Repo.
2. Ensure Python 3 is installed.
3. Run 'mainControl.py' to start Mercer.
4. Experiment with the features avalible and teach Mercer words.

## Reddit Interaction Setup
Allows Mercer to interact (in a read only capacity) with Reddit for learning purposes.
1. Install 'praw' with 'pip install praw'.
2. Go to [Reddit App registration](https://www.reddit.com/prefs/apps/).
3. Create a new app (likely as a script). Keep the page open.
4. Fill in the 'client_id' and the 'client_secret' sections, as shown on the Reddit app page, in the 'praw.ini' file.
5. (Optional) Fill in the 'username' and 'password' sections in the 'praw.ini' file. This is not required for read-only operations.