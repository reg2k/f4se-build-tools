import os, sys, io, re, codecs

#================================================================
# # About
# This script replaces $(SolutionDir) in the reference paths of the supplied
# project file with the specified directory.
# If the supplied argument is a directory then the first vcxproj found
# in the directory will be used.
#================================================================

#===================
# Configuration
#===================
# Get arguments
if len(sys.argv) > 2:
    PROJECT_PATH = sys.argv[1]
    NEW_DIR      = sys.argv[2]
else:
    print('FATAL: No project or value provided.')
    sys.exit(0)
    
if os.path.isdir(PROJECT_PATH):
    for file in os.listdir(PROJECT_PATH):
        if file.endswith(".vcxproj"):
            PROJECT_PATH = os.path.join(PROJECT_PATH, file)
            break

print('Project Path: {}'.format(PROJECT_PATH))
            
#===========================
# Update project file
#===========================
# Regex Patterns
re_projectReference = re.compile('(<ProjectReference Include=")(\$\(SolutionDir\))(.+">[\S\s]*?<\/ProjectReference>)', re.MULTILINE)

# Read vcxproj to string
with open(PROJECT_PATH, encoding='utf-8') as f:
    fileStr = f.read()

# Update project references
fileStr = re_projectReference.sub(r'\1{}\3'.format(NEW_DIR), fileStr)
    
# Write new vcxproj    
with codecs.open('output.vcxproj', 'w', 'utf-8') as f:
    f.write(fileStr)