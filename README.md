# CustomKeys
Scripts for games, written on python and its libraries.
Works mainly on binds over keyboard or mouse.
Check for key key_trigger field, to see what bind used.

**GENERAL:**
dist folder + dist.zip file has the run file for the script.

**SETTINGS\CONFIG.txt:**
========================================
**TO ADJUST CONFIG.TXT USE JSON SYNTAX**
========================================
Adjust to yours needs: 0 = OFF \ 1 = ON
stat - displays the state of the scripts.

0. General - general settings.
   * display - Changes between plain text and emojis of the tuggles(due the display in console, not every consoles can use emoji).
1. Kill Switch - Switches on and off the entire script.
2. Auto Click Clip - Clicker, by default ll click 20 times on given action key on keyboard.
   * mode - Swicthes between 20 clicks and infinte clicks(by default ON, if set on OFF, it wont wait for users signal).
   * mouse - Switches between LMB clicks and Keyboard clicks(by default OFF, check action key for keyboard clicks).
   * trigger - Displays if script got users signal or not.
   * count - Counts clicks made by clicker, wont work as mode is OFF(infinite).
3. Smart AFK - Fakes yours presence in a game, if turned ON, ll press random keys on W,A,S,D every few minutes.
   * lock - Shows if script is set, ll switch to ON as scripts works.
   * time - Will show time, till next moment it will fake again.
4. Quick Insert - Presses the keys from the "quick insert text.txt" after key_action, as you use the bind(Used to push stuff in to games chat).
5. Saves Snatcher - Looks for the "path_from" foldier and for any updates copies in to "path_to" foldier(Used to make copies of "Hardcore" games with saves delete).
   * backup time - As script is ON, and there is NEW update, it ll display the last time update.
   * dir files - Amount files in the original directory.
   * self replace - Copies files from backup to original foldier, if original miss files or deleted completley.


