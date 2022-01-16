# Cisco Unified Communications Manager Free Number Finder
This Python script finds free extensions on Cisco Unified Communications Manager systems.
When run the script will ask for the following information:
- IP address of CUCM Publisher server.
- Username of a user with AXL API privileges - Read Only is sufficient.
- User password - the script does not obfuscate the password when the user enters it. I use Pycharm which does not play friendly with Getpass which is the obvious fix for this.
- Start number for the extension number range being scanned.
- End number for the extension number range being scanned.

The script will connect to the CUCM server, make an AXL SQL query to find free numbers in the range and the write these to a text file.
