import os, sys, io, re, codecs

#================================================================
# # About
# This script creates a solution file to compile the specified project.
# Result sln is output to OUTPUT_FILE.
#
# # Arguments
# [1] PROJECT_PATH - vcxproj file or directory containing vcxproj file.
# [2] OUTPUT_FILE - sln will be output here.
#================================================================

#===================
# Configuration
#===================
BUILD_TOOLS_PATH = os.path.dirname(os.path.abspath(__file__))
SOLUTION_PATH = os.path.join(BUILD_TOOLS_PATH, 'f4se_plugin.sln')

# Get arguments
if len(sys.argv) > 2:
    PROJECT_PATH = sys.argv[1]
    OUTPUT_FILE  = sys.argv[2]
else:
    print('FATAL: No project or output path provided.')
    sys.exit(1)
    
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
re_project = re.compile('(Project\("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}"\) = ")PLUGIN_NAME(", ")PLUGIN_DIR(", "{00000000-0000-0000-0000-000000000000}"\nEndProject)', re.MULTILINE)
re_guid = re.compile('(.*){00000000-0000-0000-0000-000000000000}(.*)')

# Backreference 2 holds the values
re_proj_name = re.compile('(<PropertyGroup.*Label="Globals">[\S\s]*?<RootNamespace>)(.*)(<\/RootNamespace>[\S\s]*?<\/PropertyGroup>)', re.MULTILINE)
re_proj_guid = re.compile('(<PropertyGroup.*Label="Globals">[\S\s]*?<ProjectGuid>)(.*)(<\/ProjectGuid>[\S\s]*?<\/PropertyGroup>)', re.MULTILINE)

# Read vcxproj file
with open(PROJECT_PATH, 'r') as f:
    fileStr = f.read()

# Extract name and GUID
name_search = re_proj_name.search(fileStr)
guid_search = re_proj_guid.search(fileStr)
if not name_search or not guid_search:
    print('FATAL: Cannot extract name or GUID from project file.')
    sys.exit(1)
plugin_name = name_search.group(2)
plugin_guid = guid_search.group(2)
plugin_project_path = os.path.abspath(os.path.join(os.path.dirname(PROJECT_PATH), 'build.vcxproj')).replace('\\', '/')

# Read template sln file
with open(SOLUTION_PATH, 'r') as f:
    fileStr = f.read()

# Update project references
fileStr = re_project.sub(r'\1{}\2{}\3'.format(plugin_name, plugin_project_path), fileStr)
fileStr = re_guid.sub(r'\1{}\2'.format(plugin_guid), fileStr)
    
# Write new sln    
with codecs.open(OUTPUT_FILE, 'w', 'utf-8') as f:
    f.write(fileStr)