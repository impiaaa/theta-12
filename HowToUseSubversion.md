# Mac/Linux #
## Initial Setup ##
Open a command prompt. This is where all of the commands here will be typed. You can find the command prompt (terminal) in /Applications/Utilities on a Mac, and Applications>Utilities on Linux.

First, change directory to where you want the project directory to be, for example:
`cd Documents`
Next, type in the command and password given to you [here](http://code.google.com/p/theta-12/source/checkout). The command should look something like this:
`svn checkout https://theta-12.googlecode.com/svn/trunk/ theta-12 --username bob123`
This will create the project directory. All of the commands below need to be executed inside the project directory, so:
`cd theta-12`

If the svn command fails, you'll need to install Subversion. It should be available in most Linux package repositories, and Mac users can eiter download a binary [here](http://subversion.apache.org/packages.html) or run the developer tools installer from your system install disk. Once you've installed it, run the above commands again.

## Updating to last revision ##
Do this every so often (especially before editing) to make sure you have the most recent version of the code.
`svn up`

## Changing a file ##
Issue this command when you are done making an edit (revision):
`svn commit -message="commit message goes here"`
Replace the text inside the quotes with a summary of the changes you made.

## Adding a file ##
When you add a new file to the project, you need to tell SVN. Replace path/to/file with the relative path and file name of the new file:
`svn add path/to/file`

# Windows #
You can download TorsoiseSVN [here](http://tortoisesvn.net/). Documentation is [here](http://tortoisesvn.net/support), but the CLI is the same as above.