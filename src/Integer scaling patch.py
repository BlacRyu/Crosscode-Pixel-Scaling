# Created by Particle#0001
# Changes the "Double" option in the screen scaling to instead multiply the screen's size by the largest integer value that will fit in the window.

import glob
import re
import os





def findPath(searchString):
  paths = glob.glob(searchString, recursive=True)
  if (len(paths) > 0):
    return paths[0]
  else:
    return None






gamePath = findPath('**/game.compiled.js')
langPath = findPath('**/gui.en_US.json')

if (gamePath == None or langPath == None):
    print("Game files not found, please run this from the game\'s install directory")
    quit()

with open(gamePath) as gameFile:
  moddedLines = gameFile.readlines()
findString = ":a=c*2;b=d*2;break;"
findStringEscaped = re.escape(findString)
replaceString = r":a=Math.floor(Math.min(f/d,b/c));a=a<1?1:a;b=d*a;a=c*a;break;"
foundIt = False
foundRep = False
for i, line in enumerate(moddedLines):
  if findString in line:
    foundIt = True
    moddedLines[i] = re.sub(findStringEscaped,replaceString,line)
    break
  elif replaceString in line:
    foundRep = True

if foundIt:
  # keep the original file as a backup
  if (os.access(gamePath+".backup", os.F_OK)):
    i = 0
    while (os.access(gamePath+".backup"+str(i), os.F_OK)):
      i += 1
    os.rename(gamePath, gamePath+".backup"+str(i))
  else:
    os.rename(gamePath, gamePath+".backup")
  # replace it with the modified file
  with open('game.compiled.js', 'w') as moddedFile:
    for line in moddedLines:
      moddedFile.write(line)
  print("Files modified successfully!")
elif foundRep:
  print("Failed to apply mod, Looks like it was already applied!")
else:
  print("Failed to apply mod, couldn't find what we were supposed to replace :(")
