import os, sys, shutil, glob, re
from contextlib import contextmanager, suppress

#================================================================
# # About
# Uses src/Config.h to build a release package.
#
# # Arguments
# [1] PLUGIN_LOCATION_PATTERN - Pathname pattern of the DLL file.
# [2] DIST_DIR - Directory containing files to package with the plugin.
# [3] OUTPUT_LOCATION - Path of directory to output the archive.
# [4] SRC_PATH - Path of source directory that has Config.h (optional)
#================================================================

#===================
# Configuration
#===================
# Get arguments
if len(sys.argv) > 3:
    PLUGIN_LOCATION_PATTERN = sys.argv[1]
    DIST_DIR        = sys.argv[2]
    OUTPUT_LOCATION = sys.argv[3]
    SRC_PATH = ''
    
    if len(sys.argv) > 4:
        SRC_PATH = sys.argv[4]
else:
    print('FATAL: Invalid arguments.')
    sys.exit(1)

# Defaults (if Config.h does not exist)
OUT_NAME = 'Packaged'
    
#===================
# Read Config.h
#===================
CONFIG_PATH = os.path.join(SRC_PATH, 'Config.h')
if os.path.exists(CONFIG_PATH):
    with open(os.path.join(SRC_PATH, 'Config.h')) as f:
        for line in f:
            # Find all #define statements
            property = re.search('^#define\s+(\w+)\s+"?([\w\d\s\.]*)"?$', line)
            if property:
                name  = property.group(1)
                value = property.group(2)
                # print("Property: {} | Value: {}".format(name, value))
                if (name == 'PLUGIN_VERSION_STRING'):
                    PLUGIN_VERSION_STRING = value
                elif (name == 'PLUGIN_NAME_SHORT'):
                    PLUGIN_NAME_SHORT = value
                elif (name == 'PLUGIN_NAME_LONG'):
                    PLUGIN_NAME_LONG = value
                
    # Make sure vars exist
    PLUGIN_VERSION_STRING
    PLUGIN_NAME_SHORT
    PLUGIN_NAME_LONG
    
    OUT_NAME = "{} {}".format(PLUGIN_NAME_LONG, PLUGIN_VERSION_STRING)
    
#===================
# Packaging
#===================
packageOK = 1 # Exit code (0 is success)
if os.path.exists(DIST_DIR):
    # Build path to output directory
    OUT_DIR = os.path.join(OUTPUT_LOCATION, OUT_NAME)
    print("Output directory: {}".format(OUT_DIR))
    
    # Remove any previously packaged archive.
    with suppress(FileNotFoundError):
        shutil.rmtree(OUT_DIR)
        os.remove(OUTPUT_LOCATION)
    
    # Copy dist folder to temporary folder.
    shutil.copytree(DIST_DIR, OUT_DIR)
    
    # Copy plugin files to Data/F4SE/Plugins.
    for file in glob.glob(PLUGIN_LOCATION_PATTERN):
        print("Copied file: {}".format(file))
        shutil.copy(file, os.path.join(OUT_DIR, 'Data/F4SE/Plugins'))
        
    # Create archive.
    OUTPUT_FILENAME = os.path.join(OUTPUT_LOCATION, OUT_NAME)
    shutil.make_archive(OUTPUT_FILENAME, 'zip', OUT_DIR)
    print('Archive created at: {}'.format(OUTPUT_FILENAME + '.zip'))
    
    # Status update
    print('Packaging complete.')
    packageOK = 0
    
sys.exit(packageOK)