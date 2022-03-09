import os
import re
from pathlib import Path
'''

 Function: renameFiles
 Parameters: 
    @path: The path to the folder you want to traverse
    @depth: How deep you want to traverse the folder. Defaults to 99 levels. 
    
'''

# TODO store images in a db (Redis? check efficiency vs other DB types/frameworks)
def renameFiles(path="./images/new_pics", depth=99):
	# Once we hit depth, return
	if depth < 0: return

	# checks path is a real directory, not a symlink
	if os.path.isdir(path) and not os.path.islink(path):
		image_index_tag = 00
		for folder in os.listdir(path):
			fullpath = path + os.path.sep + folder
			if not os.path.islink(fullpath):
				if os.path.isdir(fullpath):
					renameFiles(fullpath, depth - 1)
				else:
					extension = os.path.splitext(fullpath)[1]
					# Ensures we ignore erroneous data. Here, we have image types. Change as needed.
					if extension in ('.jpg', '.jpeg', '.png', '.gif'):
						# We want to make sure that we change the directory we are in
						# If you do not do this, you will not get to the subdirectory names
						os.chdir(path)
						dir_path = os.path.basename(os.path.dirname(os.path.realpath(folder)))
						newpath = os.path.dirname(fullpath) + os.path.sep + dir_path \
								  + '_' + "{0:0=2d}".format(image_index_tag) + extension
						while os.path.exists(newpath):
							image_index_tag += 1
							newpath = os.path.dirname(fullpath) + os.path.sep + dir_path \
									  + '_' + "{0:0=2d}".format(image_index_tag) + extension
						os.rename(fullpath, newpath)
						image_index_tag += 1
	print("\nDone renaming images\n")
	return
renameFiles()

