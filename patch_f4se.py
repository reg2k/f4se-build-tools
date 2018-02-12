import os, sys, io, re, codecs

#================================================================
# # About
# This script makes changes to F4SE for plugin development under VS2015.
#
# # Arguments
# [1] F4SE_PATH - Path to src/f4se.
#
# # Changes
# ## src/f4se/f4se/f4se.vcxproj
# - Output a static library instead of a dynamic library for linking with plugins.
#
# ## src/f4se/f4se/BSSkin.h
# - Add missing header #include <xmmintrin.h> for use of __m128 type.
#
# ## src/f4se/f4se/PapyrusObjects.h
# - Add missing header #include <algorithm> for use of std::min.
#================================================================

#===================
# Configuration
#===================
# Get F4SE path (src/f4se)
if len(sys.argv) > 1:
    F4SE_PATH = sys.argv[1]
else:
    print('FATAL: No F4SE directory provided.')
    sys.exit(1)

print('F4SE Path: {}'.format(F4SE_PATH))

#===========================
# Update F4SE project file
#===========================
# # Changes:
# ## f4se.vcxproj
# PropertyGroup[@Label="Configuration"].ConfigurationType = StaticLibrary

# Regex Patterns
re_configType = re.compile('(<PropertyGroup.*Label="Configuration">[\S\s]*?<ConfigurationType>)(.*)(<\/ConfigurationType>[\S\s]*?<\/PropertyGroup>)', re.MULTILINE)

# Read vcxproj
with open(os.path.join(F4SE_PATH, 'f4se/f4se.vcxproj'), encoding='utf-8') as f:
    fileStr = f.read()

# Set Configuration Type to Static Library (original: Dynamic Library)
fileStr = re_configType.sub(r'\1StaticLibrary\3', fileStr)

# Write new vcxproj    
with codecs.open(os.path.join(F4SE_PATH, 'f4se/f4se.vcxproj'), 'w', 'utf-8') as f:
    f.write(fileStr)

#===========================
# Update F4SE source code
#===========================
# Adds a line to the specified file 
def add_line(filepath, lineToAdd):
    with open(os.path.join(F4SE_PATH, filepath), 'r+') as f:
        fileStr = f.readlines()
        if not (lineToAdd + '\n') in fileStr:
            f.seek(0)
            for i, line in enumerate(fileStr):
                if i == 1:
                    f.write(lineToAdd + '\n')
                f.write(line)
            f.truncate()
            return True
        return False

num_patched = 0
num_patched += add_line('f4se/BSSkin.h', '#include <xmmintrin.h>')
num_patched += add_line('f4se/PapyrusObjects.h', '#include <algorithm>')

print("Patched: {}/2".format(num_patched))