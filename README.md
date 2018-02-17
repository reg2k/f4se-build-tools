# f4se-build-tools
Build scripts for F4SE plugins. The purpose of these scripts is to support automated builds of F4SE plugins in continuous integration services. These build tools prepare a clean development environment for plugin compilation.

## Requirements
- Visual Studio 2017
- Python 3.4+

## What it does
`build_plugin.py` is the entry point for the build tools and executes the other helper scripts.

The build tools do the following:
1. Fetch the specified revision of F4SE from [f4se-mirror](https://github.com/osvein/f4se-mirror). (`build_plugin.py`)
2. Prepare the F4SE codebase for plugin compilation. (`patch_f4se.py`)
3. Generate a plugin project file (`build.vcxproj`) for compilation. (`update_project_references.py`)
4. Generate a solution file (`build.sln`) for command-line compilation with `msbuild`. (`make_solution.py`)
5. Builds the plugin and required F4SE components with `msbuild`. (`build_plugin.py`)
6. Clean up: remove the generated project and solution files. (`build.vcxproj` and `build.sln`) (`build_plugin.py`)


## Credits
Thanks to [osvein](https://github.com/osvein) for maintaining [f4se-mirror](https://github.com/osvein/f4se-mirror).
