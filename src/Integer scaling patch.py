# Created by Particle#0001
# Changes the "Double" option in the screen scaling to instead multiply the screen's size by the largest integer value that will fit in the window.

import glob
import re
import os


# List of tuples defining what is to be modified
# 1 - File we are modifying
# 2 - Text to be replaced
# 3 - Text we are replacing it with
commandList = [
  ("**/game.compiled.js", ":a=c*2;b=d*2;break;", r":a=Math.floor(Math.min(f/d,b/c));a=a<1?1:a;b=d*a;a=c*a;break;"),
  ("**/gui.en_US.json", '"Original","Double","Fit","Stretch"', r'"Original","Scaled","Fit","Stretch"'),
]


# ======================================================
# ================== Helper Function(s) ================
# ======================================================
def findPath(searchString):
  paths = glob.glob(searchString, recursive=True)
  if (len(paths) > 0):
    return paths[0]
  else:
    return None



# ======================================================
# ================== Begin Execution ===================
# ======================================================
commandsAttempted = 0
commandsCompleted = 0

for fileName,findString,replaceString in commandList:
  commandsAttempted = commandsAttempted + 1

  # Read the file
  filePath = findPath(fileName)
  if (filePath == None):
    continue
  with open(filePath) as fileObject:
    moddedLines = fileObject.readlines()

  # Find and replace lines
  foundIt = False
  findStringEscaped = re.escape(findString)
  for i, line in enumerate(moddedLines):
    if findString in line:
      moddedLines[i] = re.sub(findStringEscaped,replaceString,line)
      foundIt = True
      break
    elif replaceString in line:
      foundRep = True

  if foundIt:
    # keep the original file as a backup
    if (os.access(filePath+".backup", os.F_OK)):
      i = 0
      while (os.access(filePath+".backup"+str(i), os.F_OK)):
        i += 1
      os.rename(filePath, filePath+".backup"+str(i))
    else:
      os.rename(filePath, filePath+".backup")
    # replace it with the modified file
    with open(filePath, 'w') as moddedFile:
      for line in moddedLines:
        moddedFile.write(line)
    commandsCompleted = commandsCompleted + 1

if commandsCompleted == commandsAttempted:
  print("Files modified successfully :)")
elif commandsCompleted > 0:
  print("Mod was only partially applied, some of the target code was missing or already changed.")
elif foundRep:
  print("Failed to apply mod, Looks like it may have already been applied.")
else:
  print("Failed to apply mod, couldn't find the code to be modified :(")
