import os
from dataclasses import dataclass

LOGOPATH = f"{os.getcwd()}\\images\\logo.png"
DARKLOGOPATH = f"{os.getcwd()}\\images\\darklogo.png"


@dataclass(slots=True)
class FileMode:
    read = 'r'
    write = 'w'
    read_bytes = 'rb'
    write_bytes = 'wb'
    create = 'x'
    append = 'a'

@dataclass(slots=True)
class CompileMode:
    evaluate = 'eval'
    execute = 'exec'
    single = 'single'
    
@dataclass(slots=True)
class Pyinstaller:
    flags = [
        "--onedir", "--onefile", "--clean", "--strip", "--noupx", "--console", "--windowed", 
        '--disable-windowed-traceback', "--no-embedded-manifest", "--uac-admin", "--uac-uiaccess", 
        "--win-private-assemblies", "--win-no-prefer-redirects", "--bootloader-ignore-signals", "--argv-emulation", "--bootloader-ignore-signals"
    ]
    fkeys = [x for x in flags]
    flag_descriptions = [
        "Create a one-folder bundle containing an executable (default)", "Create a one-file bundled executable.", "Clean PyInstaller cache and remove temporary files before building",
        "Apply a symbol-table strip to the executable and shared libs (not recommended for Windows)", "Do not use UPX even if it is available (works differently between Windows and *nix)",
        "Open a console window for standard i/o (default). On Windows this option has no effect if the first script is a '.pyw' file.", "Windows and Mac OS X: do not provide a console window for standard i/o. On Mac OS this also triggers building a Mac OS .app bundle. On Windows this option is automatically set if the first script is a ‘.pyw’ file. This option is ignored on *NIX systems.",
        "Disable traceback dump of unhandled exception in windowed (noconsole) mode (Windows and macOS only), and instead display a message that this feature is disabled.", "Generate an external .exe.manifest file instead of embedding the manifest into the exe. Applicable only to onedir mode; in onefile mode, the manifest is always embedded, regardless of this option.",
        "Using this option creates a Manifest that will request elevation upon application start.", "Using this option allows an elevated application to work with Remote Desktop.",
        "Any Shared Assemblies bundled into the application will be changed into Private Assemblies. This means the exact versions of these assemblies will always be used, and any newer versions installed on user machines at the system level will be ignored.",
        "While searching for Shared or Private Assemblies to bundle into the application, PyInstaller will prefer not to follow policies that redirect to newer versions, and will try to bundle the exact versions of the assembly.",
        "Tell the bootloader to ignore signals rather than forwarding them to the child process. Useful in situations where for example a supervisor process signals both the bootloader and the child (e.g., via a process group) to avoid signalling the child twice.",
        "Enable argv emulation for macOS app bundles. If enabled, the initial open document/URL event is processed by the bootloader and the passed file paths or URLs are appended to sys.argv.",
        "Tell the bootloader to ignore signals rather than forwarding them to the child process. Useful in situations where for example a supervisor process signals both the bootloader and the child (e.g., via a process group) to avoid signalling the child twice."
    ]
    windows_flags = ["--no-embed-manifest", "--uac-uiaccess", "--win-private-assemblies", "--win-no-prefer-redirects", "--uac-admin"]
    windows_options = ["--version-file", "--manifest",  "--resource"]
    mac_flags = ["--argv-emulation"]
    mac_options = ["--osx-bundle-identifier", "--target-architecture", "--codesign-identity", "--osx-entitlements-file"]
    options = [
        "--name", "--add-binary", "--paths", "--hidden-import", "--collect-submodules", "--collect-data", "--collect-binaries", "--collect-all", "--specpath",
        "--add-data", "--copy-metadata", "--recursive-copy-metadata", "--additional-hooks-dir", "--runtime-hook", "--exclude-module", "--splash", "--osx-bundle-identifier",
        "--target-architecture", "--codesign-identity", "--osx-entitlements-file", "--runtime-tmpdir"
    ]
    okeys = [x for x in options]
    option_descriptions = [
        "Name to assign to the bundled app and spec file (default: first script's basename)", "Additional binary files to be added to the executable. See the --add-data option for more details. This option can be used multiple times.",
        "A path to search for imports (like using PYTHONPATH). Multiple paths are allowed, separated by ':', or use this option multiple times. Equivalent to supplying the pathex argument in the spec file.", "Name an import not visible in the code of the script(s). This option can be used multiple times.",
        "Collect all submodules from the specified package or module. This option can be used multiple times.", "Collect all data from the specified package or module. This option can be used multiple times.", "Collect all binaries from the specified package or module. This option can be used multiple times.",
        "Collect all submodules, data files, and binaries from the specified package or module. This option can be used multiple times.", "Folder to store the generated spec file (default: current directory)",
        "Additional non-binary files or folders to be added to the executable. The path separator is platform specific, os.pathsep (which is ; on Windows and : on most unix systems) is used. This option can be used multiple times.",
        "Copy metadata for the specified package. This option can be used multiple times.", "Copy metadata for the specified package and all its dependencies. This option can be used multiple times.", "An additional path to search for hooks. This option can be used multiple times.",
        "Path to a custom runtime hook file. A runtime hook is code that is bundled with the executable and is executed before any other code or module to set up special features of the runtime environment. This option can be used multiple times.",
        "Optional module or package (the Python name, not the path name) that will be ignored (as though it was not found). This option can be used multiple times.", "(EXPERIMENTAL) Add an splash screen with the image IMAGE_FILE to the application. The splash screen can display progress updates while unpacking.",
        "Mac OS .app bundle identifier is used as the default unique program name for code signing purposes. The usual form is a hierarchical name in reverse DNS notation. For example: com.mycompany.department.appname (default: first script's basename)",
        "Target architecture (macOS only; valid values: x86_64, arm64, universal2). Enables switching between universal2 and single-arch version of frozen application (provided python installation supports the target architecture). If not target architecture is not specified, the current running architecture is targeted.",
        "Code signing identity (macOS only). Use the provided identity to sign collected binaries and generated executable. If signing identity is not provided, ad- hoc signing is performed instead.",
        "Entitlements file to use when code-signing the collected binaries (macOS only).",
        "Where to extract libraries and support files in onefile-mode. If this option is given, the bootloader will ignore any temp-folder location defined by the run-time OS. The _MEIxxxxxx-folder will be created here. Please use this option only if you know what you are doing."  
    ]
    flag_map = {key:value for key,value in zip(flags, flag_descriptions)}
    option_map = {key:value for key,value in zip(options, option_descriptions)} 
    
@dataclass(slots=True)
class Nuikta:
    
    all_actions = [
        "--module", "--standalone", "--onefile", "--python-debug", "--python-flag", "--python-for-scons", "--include-package", 
        "--include-module", "--include-plugin-directory", "--include-plugin-files", "--prefer-source-code", "--follow-imports", "--follow-import-to", 
        "--nofollow-import-to", "--nofollow-imports", "--follow-stdlib", "--onefile-tempdir-spec", "--onefile-child-grace-time", "--include-package-data", 
        "--include-package-data", "--include-data-files", "--include-data-dir", "--noinclude-data-files", "--list-package-data", "--noinclude-dlls", 
        "--list-package-dlls", "--warn-implicit-exceptions", "--warn-unusual-code", "--assume-yes-for-downloads", "--nowarn-mnemonic", "--run", "--debugger", 
        "--execute-with-pythonpath", "--user-package-configuration-file", "--full-compat", "--file-reference-choice", "--module-name-choice", 
        "--output-filename", "--output-dir", "--remove-output", "--no-pyi-file", "--debug", "--unstripped", "--profile", "--internal-graph", 
        "--trace-execution", "--recompile-c-only", "--xml", "--generate-c-only", "--experimental", "--low-memory", "--create-environment-from-report", 
        "--clang", "--mingw64", "--msvc", "--jobs", "--lto", "--static-libpython", "--disable-cache", "--clean-cache", "--disable-bytecode-cache", 
        "--disable-ccache", "--disable-dll-dependency-cache", "--pgo", "--pgo-args", "--pgo-executable", 
        "--report", "--report-template", "--show-memory", "--enable-console", "--force-stdout-spec", "--force-stderr-spec", 
        "--windows-icon-from-ico", "--windows-icon-from-exe", "--onefile-windows-splash-screen-image", "--windows-uac-admin", "--windows-uac-uiaccess", 
        "--macos-target-arch", "--macos-create-app-bundle", "--macos-app-icon", "--macos-signed-app-name", "--macos-app-name", "--macos-app-mode", 
        "--macos-sign-identity", "--macos-sign-notarization", "--macos-app-version", "--macos-app-protected-resource", "--linux-icon", "--company-name", 
        "--product-name", "--file-version", "--enable-plugin", "--disable-plugin", 
        "--plugin-no-detection", "--plugin-list", "--user-plugin", "--show-source-changes", "--show-anti-bloat-changes", "--noinclude-setuptools-mode", 
        "--noinclude-pytest-mode", "--noinclude-unittest-mode", "--noinclude-IPython-mode", "--noinclude-dask-mode", "--noinclude-numba-mode", 
        "--noinclude-default-mode", "--noinclude-custom-mode"
        
    ]
    all_descriptions = [
        "Create an extension module executable instead of a program. Defaults to off.",
        "Enable standalone mode for output. This allows you to transfer the created binary to other machines without it using an existing Python installation. This also means it will become big. It implies these option: 'follow-imports' and 'to off.'",
        "On top of standalone mode, enable onefile mode. This means not a folder, but a compressed executable is created and used. Defaults to off.",
        "Use debug version or not. Default uses what you are using to run Nuitka, most likely a non-debug version.",
        "run Nuitka, this enforces a specific mode. These are options that also exist to standard Python executable. Currently supported: '-S' (alias 'no_site'), static_hashes (do not use hash randomization), no_warnings (do not give Python run time warnings), O (alias 'no_asserts'), 'no_docstrings' (do not use doc strings), '-u' (alias 'unbuffered') and '-m'. Default empty.",
        "If using Python3.3 or Python3.4, provide the path of a Python binary to use for Scons. Otherwise Nuitka can use what you run Nuitka with or a Python installation from Windows registry. On Windows Python 3.5 or higher is needed. On non-Windows, Python 2.6 or 2.7 will do as well.",
        "Include a whole package. Give as a Python namespace, e.g. 'some_package.sub_package' and Nuitka will then find it and include it and all the modules found below that disk location in the binary or extension module it creates, and make it available for import by the code. To avoid unwanted sub packages, e.g. tests you can e.g. do this '',Default empty.",
        "Include a single module. Give as a Python namespace, e.g. 'some_package.some_module' and Nuitka will then find it and include it in the binary or extension module it creates, and make it available for import by the code. Default empty.",
        "Include also the code found in that directory, considering as if they are each given as a main file. Overrides all other inclusion options. You ought to prefer other inclusion options, that go by names, rather than filenames, those find things through being in 'sys.path'. This option is for very special use cases only. Can be given multiple times. Default empty.",
        "Include into files matching the PATTERN. Overrides all other follow options. Can be given multiple times. Default empty.",
        "For already compiled extension modules, where there is both a source file and an extension module, normally the extension module is used, but it should be better to compile the module from available source code for best performance. If not desired, there is 'prefer-source-code' to disable warnings about it. Default off.",
        "Descend into all imported modules. Defaults to on in standalone mode, otherwise off.",
        "Follow to that module if used, or if a package, to the whole package. Can be given multiple times. Default empty.",
        "Do not follow to that module name even if used, or if a package name, to the whole package in any case, overrides all other options. Can be given multiple times. Default empty.",
        "Do not descend into any imported modules at all, overrides all other inclusion options and not usable for standalone mode. Defaults to off.",
        "Also descend into imported modules from standard library. This will increase the compilation time by a lot and is also not well tested at this time and sometimes won't work. Defaults to off.",
        "Use this as a folder to unpack to in onefile mode. Defaults to '%TEMP%/onefile_%PID%_%TIME%', i.e. user temporary directory and being non-static it's removed. Use e.g. a string like CACHE_DIR%/%COMPANY%/%PRODUCT%/%VERSION%' which is a good static cache path, this will then not be removed.",
        "When stopping the child, e.g. due to CTRL-C or shutdown, etc. the Python code gets a KeyboardInterrupt, that it may handle e.g. to flush data. This is the amount of time in ms, before the child it killed in the hard way. Unit is ms, and default 5000.",
        "Include data files for the given package name. DLLs and extension modules are not data files and never included like this. Can use patterns the filenames as indicated below. Data files of packages are not included by default, but package configuration can do it. This will only include non-DLL, non-extension modules, i.e. actual data files. After a ':' optionally a filename pattern can be given as well, selecting only matching files. Examples: (concrete file) Default empty.",
        "Include data files by filenames in the distribution. There are many allowed forms. With ---- will copy a single file and complain if it's multiple. With '--- all matching files into that folder. For recursive copy there is a form with 3 values that will preserve directory structure. Default empty.",
        "Include data files from complete directory in the distribution. This is recursive.Check 'data-files' with patterns if you want non-recursive inclusion. An example would be ' the whole directory. All files are copied, if you want to exclude files you need to remove them beforehand, or use '-data-files' option to remove them. Default empty.",
        "include data directories",
        "Do not include data files matching the filename pattern given. This is against the target filename, not source paths. So to ignore a file pattern from package data for 'package_name' should be matched as package_name/*.txt'. Or for the whole directory simply use 'package_name'. Default empty.",
        "Output the data files found for a given package name. Default not done.",
        "Do not include DLL files matching the filename pattern given. This is against the target filename, not source paths. So ignore a DLL 'someDLL' contained in the package 'package_name' it should be matched as package_name/someDLL.*. Default empty.",
        "Output the DLLs found for a given package name. Default not done.",
        "Enable warnings for implicit exceptions detected at compile time.",
        "Enable warnings for unusual code detected at compile time.",
        "Allow Nuitka to download external code if necessary, e.g. dependency walker, ccache, and even gcc on Windows. To disable, redirect input from nul device, e.g. '</dev/null or <NUL:. Default is to prompt.",
        "Disable warning for a given mnemonic. These are given to make sure you are aware of certain topics, and typically point to the Nuitka website. The mnemonic is the part of the URL at the end, without the HTML suffix. Can be given multiple times and accepts shell pattern. Default empty.",
        "Execute immediately the created binary (or import the compiled module). Defaults to off.",
        "Execute inside a debugger, e.g. gdb or lldb to automatically get a stack trace. Defaults to off.", 
        "When immediately executing the created binary or module using '', don't reset 'PYTHONPATH' environment. When all modules are successfully included, you ought to not need PYTHONPATH anymore, and definitely not for standalone mode.",
        "User provided Yaml file with package configuration. You can include DLLs, remove bloat, add hidden dependencies. Check User Manual for a complete description of the format to use. Can be given multiple times. Defaults to empty.",
        "Enforce absolute compatibility with CPython. Do not even allow minor deviations from CPython behavior, e.g. not having better tracebacks or exception messages which are not really incompatible, but only different or worse. This is intended for tests only and should *not* be used.",
        "Select what value __file__ is going to be. With runtime (default for standalone binary mode and module mode), the created binaries and modules, use the location of themselves to deduct the value of __file__. Included packages pretend to be in directories below that location. This allows you to include data files in deployments. If you merely seek acceleration, it's better for you to use the original value, where the source files location will be used. With frozen a notation <frozen module_name> is used. For compatibility reasons, the __file__ value will always have .py suffix independent of what it really is.",
        "Select what value __name__ and __package__ are going to be. With 'runtime' (default for module mode), the created module uses the parent package to deduce the value of __package__, to be fully compatible. The value 'original' (default for other modes) allows for more static optimization to happen, but is incompatible for modules that normally can be loaded into any package.",
        "Specify how the executable should be named. For extension modules there is no choice, also not for standalone mode and using it will be an error. This may include path information that needs to exist though. Defaults to '<program_name>' on this platform. exe",
        "Specify where intermediate and final output files should be put. The DIRECTORY will be populated with build folder, dist folder, binaries, etc. Defaults to current directory.",
        "Removes the build directory after producing the module or exe file. Defaults to off.",
        "Do not create a '.pyi' file for extension modules created by Nuitka. This is used to detect implicit imports. Defaults to off.",
        "Executing all self checks possible to find errors in Nuitka, do not use for production. Defaults to off.",
        "Keep debug info in the resulting object file for better debugger interaction. Defaults to off.",
        "Enable vmprof based profiling of time spent. Not working currently. Defaults to off.",
        "Create graph of optimization process internals, do not use for whole programs, but only for small test cases. Defaults to off.",
        "Traced execution output, output the line of code before executing it. Defaults to off.",
        "This is not incremental compilation, but for Nuitka development only. Takes existing files and simply compile them as C again. Allows compiling edited C files for quick debugging changes to the generated source, e.g. to see if code is passed by, values output, etc, Defaults to off. Depends on compiling Python source to determine which files it should look at.", 
        "optimization in XML form to given filename.",
        "Generate only C source code, and do not compile it to binary or module. This is for debugging and code coverage analysis that doesn't waste CPU. Defaults to off. Do not think you can use this directly.",
        "Use features declared as 'experimental'. May have no effect if no experimental features are present in the code. Uses secret tags (check source) per experimented feature.",
        "Attempt to use less memory, by forking less C compilation jobs and using options that use less memory. For use on embedded machines. Use this in case of out of memory problems. Defaults to off.",
        "Create a new virtualenv in that non-existing path from the report file given with e.g. 'report.xml'. Default not done.",
        "Enforce the use of clang. On Windows this requires a working Visual Studio version to piggy back on. Defaults to off.",
        "Enforce the use of MinGW64 on Windows. Defaults to off unless MSYS2 with MinGW Python is used.",
        "Enforce the use of specific MSVC version on Windows. Allowed values are e.g. '14.3 (MSVC 2022) and other MSVC version numbers, specify 'list' for a list of installed compilers, or use 'latest'.  Defaults to latest MSVC being used if installed, otherwise MinGW64 is used.",
        "jobs. Defaults to the system CPU count.",
        "Allowed values are 'yes', 'no', and 'auto' (when it's known to work). Defaults to 'auto'.",
        "Use static link library of Python. Allowed values are 'yes', 'no', and 'auto' (when it's known to work). Defaults to 'auto'.",
        "Disable selected caches, specify 'all' for all cached. Currently allowed values are: 'all','ccache','bytecode','dll-dependencies'. can be given multiple times or with comma separated values. Default none.",
        "Clean the given caches before executing, specify 'all' for all cached. Currently allowed values are: 'all','ccache','bytecode','dll-dependencies'. can be given multiple times or with comma separated values. Default none.",
        "Do not reuse dependency analysis results for modules, esp. from standard library, that are included as bytecode. Same as ",
        "Do not attempt to use ccache (gcc, clang, etc.) or clcache (MSVC, clangcl). Same as  Disable the dependency walker cache. Will result in much longer times to create the distribution folder, but might be used in case the cache is suspect to cause errors. Same as dependencies.",
        "For an update of the dependency walker cache. Will result in much longer times to create the distribution folder, but might be used in case the cache is suspect to cause errors or known to need an update.",
        "Enables C level profile guided optimization (PGO), by executing a dedicated build first for a profiling run, and then using the result to feedback into the C compilation. Note: This is experimental and not working with standalone modes of Nuitka yet. Defaults to off.",
        "Arguments to be passed in case of profile guided optimization. These are passed to the special built executable during the PGO profiling run. Default empty.",
        "Command to execute when collecting profile information. Use this only, if you need to launch it through a script that prepares it to run. Default use created program.",
        "Report module, data files, compilation, plugin, etc. details in an XML output file. This is also super useful for issue reporting. These reports can e.g. be used to re-create the environment easily using it with environment-from-report', but contain a lot of information. Default is off.",
        "Report via template. Provide template and output filename 'template.rst.j2:output.rst'. For built-in templates, check the User Manual for what these are. Can be given multiple times. Default is empty.",
        "Provide memory information and statistics. Defaults to off.",
        "When compiling for Windows or macOS, enable the console window and create a console application. This disables hints from certain modules, e.g. 'PySide' that suggest to disable it. Defaults to true.",
        "Force standard output of the program to go to this location. Useful for programs with disabled console and programs using the Windows Services Plugin of Nuitka commercial. Defaults to not active, use e.g. PROGRAM%.out.txt', i.e. file near your program.",
        "Force standard error of the program to go to this location. Useful for programs with disabled console and programs using the Windows Services Plugin of Nuitka commercial. Defaults to not active, use e.g. PROGRAM%.err.txt', i.e. file near your program.",
        "Add executable icon. Can be given multiple times for different resolutions or files with multiple icons inside. In the later case, you may also suffix with n> where n is an integer index starting from 1, specifying a specific icon to be included, and all others to be ignored.",
        "Copy executable icons from this existing executable Windows only).",
        "When compiling for Windows and onefile, show this while loading the application. Defaults to off.",
        "Request Windows User Control, to grant admin rights on execution. (Windows only). Defaults to off.",
        "Request Windows User Control, to enforce running from a few folders only, remote desktop access. (Windows only). Defaults to off.",
        "What architectures is this to supposed to run on. Default and limit is what the running Python allows for. Default is 'native' which is the architecture the Python is run with.",
        "When compiling for macOS, create a bundle rather than a plain binary application. Currently experimental and incomplete. Currently this is the only way to unlock disabling of console.Defaults to off.",
        "Add icon for the application bundle to use. Can be given only one time. Defaults to Python icon if available.",
        "Name of the application to use for macOS signing. Follow 'com.YourCompany.AppName' naming results for best results, as these have to be globally unique, and will potentially grant protected API accesses.",
        "Name of the product to use in macOS bundle information. Defaults to base filename of the binary.",
        "Mode of application for the application bundle. When launching a Window, and appearing in Docker is desired, default value 'gui' is a good fit. Without a Window ever, the application is a 'background' application. For UI elements that get to display later, 'ui-element' is in-between. The application will not appear in dock, but get full access to desktop when it does open a Window later.",
        "When signing on macOS, by default an ad-hoc identify will be used, but with this option your get to specify another identity to use. The signing of code is now mandatory on macOS and cannot be disabled. Default ad-hoc' if not given.",
        "When signing for notarization, using a proper TeamID identity from Apple, use the required runtime signing option, such that it can be accepted.",
        "Product version to use in macOS bundle information. Defaults to '1.0' if not given.",
        "Request an entitlement for access to a macOS protected resources, e.g. NSMicrophoneUsageDescription:Microphone access for recording audio.' requests access to the microphone and provides an informative text for the user, why that is needed. Before the colon, is an OS identifier for an access right, then the informative text. Legal values can be found on https://developer.apple.com/doc umentation/bundleresources/information_property_list/p rotected_resources and the option can be specified multiple times. Default empty.",
        "Add executable icon for onefile binary to use. Can be given only one time. Defaults to Python icon if available.",
        "Name of the company to use in version information. Defaults to unused.",
        "Name of the product to use in version information. Defaults to base filename of the binary.",
        "File version to use in version information. Must be a sequence of up to 4 numbers, e.g. 1.0 or 1.0.0.0, no more digits are allowed, no strings are allowed. Defaults to unused.",
        "Enabled plugins. Must be plug-in names. Use 'list' to query the full list and exit. Default empty.",
        "Disabled plugins. Must be plug-in names. Use 'plugin-list' to query the full list and exit. Most standard plugins are not a good idea to disable. Default empty.",
        "Plugins can detect if they might be used, and the you can disable the warning via 'that-warned', or you can use this option to disable the mechanism entirely, which also speeds up compilation slightly of course as this detection code is run in vain once you are certain of which plugins to use. Defaults to off.",
        "Show source changes to original Python file content before compilation. Mostly intended for developing plugins. Default False.",
        "Annotate what changes are by the plugin done.",
        "Show the source changes.", 
        "Show changes made to prevent bloat",
        "What to do if a 'setuptools' or import is encountered. This package can be big with dependencies, and should definitely be avoided. Also handles 'setuptools_scm'.",
        "What to do if a 'pytest' import is encountered. This package can be big with dependencies, and should definitely be avoided. Also handles 'nose' imports.",
        "What to do if a unittest import is encountered. This package can be big with dependencies, and should definitely be avoided.",
        "What to do if a IPython import is encountered. This package can be big with dependencies, and should definitely be avoided.",
        "What to do if a 'dask' import is encountered. This package can be big with dependencies, and should definitely be avoided.",
        "What to do if a 'numba' import is encountered. This package can be big with dependencies, and is currently not working for standalone. This package is big with dependencies, and should definitely be avoided.",
        "This actually provides the default 'warning' value for above options, and can be used to turn all of these on.",
        "What to do if a specific import is encountered. Format is module name, which can and should be a top level package and then one choice, error, warning, nofollow, e.g. PyQt5:error.",
    ]

    flags = [
        "--module", "--standalone", "--onefile", "--python-debug", "--prefer-source-code", "--follow-imports", 
        "--nofollow-imports", "--follow-stdlib",
        "--include-data-", "--noinclude-data-files", "--warn-implicit-exceptions", "--warn-unusual-code", "--assume-yes-for-downloads", 
        "--run", "--debugger", "--execute-with-pythonpath", "--run", "--full-compat", "--remove-output", "--no-pyi-file", "--debug", 
        "--unstripped", "--profile", "--internal-graph", "--trace-execution", "--recompile-c-only", "--generate-c-only", "--low-memory", "--clang", 
        "--mingw64", "--disable-bytecode-cache", "--disable-ccache", "--disable-", "--disable-dll-dependency-cache", "--force-dll-dependency-cache-update", 
        "--pgo", "--create-environment-from-report", "--quiet", "--show-scons", "--no-progressbar", "--show-progress", "--show-memory", 
        "--show-modules", "--report'fileinstead.", "--show-modules", "--verbose", "--verbose", "--disable-console", "--enable-console", 
        "--windows-uac-admin", "--windows-uac-uiaccess", "--macos-create-app-bundle", "--macos-sign-notarization", "--plugin-no-detection", 
        "--plugin-list", "--show-source-changes", "--show-anti-bloat-changes" 
    ]
    
    options = [
        "--python-flag","--python-for-scons","--include-package","--nofollow-import-to","--include-module",
        "--include-plugin-directory","--include-plugin-files","--follow-import-to","--nofollow-import-to","--onefile-tempdir-spec",
        "--onefile-child-grace-time","--include-package-data","--include-package-data","--include-data-files","--include-data-dir",
        "--noinclude-data-files","--list-package-data","--noinclude-dlls","--list-package-dlls","--nowarn-mnemonic",
        "--user-package-configuration-file","--file-reference-choice","--module-name-choice","--output-filename","--output-dir",
        "--xml","--experimental","--create-environment-from-report","--report","--msvc","--jobs","--lto","--static-libpython",
        "--disable-cache","--clean-cache","--disable-cache","--disable-cache","--pgo-args","--pgo-executable","--report","--report-template",
        "--show-modules-output","--verbose-output","--force-stdout-spec","--force-stderr-spec","--windows-icon-from-ico","--windows-icon-from-exe",
        "--onefile-windows-splash-screen-image","--macos-target-arch","--macos-app-icon","--macos-signed-app-name","--macos-app-name",
        "--macos-app-mode","--macos-sign-identity","--macos-app-version","--macos-app-protected-resource","--linux-icon","--company-name",
        "--product-name","--file-version","--product-version","--file-description","--copyright","--trademarks","--enable-plugin","--disable-plugin",
        "--disable-plugin","--user-plugin","--noinclude-setuptools-mode","--noinclude-pytest-mode","--noinclude-unittest-mode","--noinclude-IPython-mode",
        "--noinclude-dask-mode","--noinclude-numba-mode","--noinclude-default-mode","--noinclude-custom-mode",
    ]
    mac_actions = [
        "--macos-target-arch",
        "--macos-create-app-bundle",
        "--macos-app-icon",
        "--macos-signed-app-name",
        "--macos-app-name",
        "--macos-app-mode",
        "--macos-sign-identity",
        "--macos-sign",
        "--macos-app-version",
        "--macos-app-protected-resource",
    ]
    options_values = [
        "--python-flag=FLAG",
        "--python-for-scons=PATH",
        "--include-package=PACKAGE",
        "--include-module=MODULE",
        "--include-plugin-directory=MODULE/PACKAGE",
        "--include-plugin-files=PATTERN",
        "--follow-import-to=MODULE/PACKAGE",
        "--nofollow-import-to=MODULE/PACKAGE",
        "--onefile-tempdir-spec=ONEFILE_TEMPDIR_SPEC",
        "--onefile-child-grace-time=GRACE_TIME_MS",
        "--include-package-data=PACKAGE",
        "--include-data-files=DESC",
        "--include-data-dir=DIRECTORY",
        "--noinclude-data-files=PATTERN",
        "--list-package-data=LIST_PACKAGE_DATA",
        "--noinclude-dlls=PATTERN",
        "--list-package-dlls=LIST_PACKAGE_DLLS",
        "--nowarn-mnemonic=MNEMONIC",
        "--user-package-configuration-file=YAML_FILENAME",
        "--file-reference-choice=MODE",
        "--module-name-choice=MODE",
        "--output-filename=FILENAME",
        "--output-dir=DIRECTORY",
        "--xml=XML_FILENAME  ",
        "--experimental=FLAG",
        "--create-environment-from-report=REPORT",
        "--msvc=MSVC_VERSION",
        "--jobs=N",
        "--lto=choice",
        "--static-libpython=choice",
        "--disable-cache=DISABLED_CACHES",
        "--clean-cache=CLEAN_CACHES",
        "--pgo-args=PGO_ARGS",
        "--pgo-executable=PGO_EXECUTABLE",
        "--report=REPORT_FILENAME",
        "--report-template=REPORT_DESC",
        "--show-modules-output=PATH",
        "--verbose-output=PATH",
        "--force-stdout-spec=FORCE_STDOUT_SPEC",
        "--force-stderr-spec=FORCE_STDERR_SPEC",
        "--windows-icon-from-ico=ICON_PATH",
        "--windows-icon-from-exe=ICON_EXE_PATH",
        "--onefile-windows-splash-screen-image=SPLASH_SCREEN_IMAGE",
        "--macos-target-arch=MACOS_TARGET_ARCH",
        "--macos-app-icon=ICON_PATH",
        "--macos-signed-app-name=MACOS_SIGNED_APP_NAME",
        "--macos-app-name=MACOS_APP_NAME",
        "--macos-app-mode=MODE",
        "--macos-sign-identity=MACOS_APP_VERSION",
        "--macos-app-version=MACOS_APP_VERSION",
        "--macos-app-protected-resource=RESOURCE_DESC",
        "--linux-icon=ICON_PATH",
        "--company-name=COMPANY_NAME",
        "--product-name=PRODUCT_NAME",
        "--file-version=FILE_VERSION",
        "--product-version=PRODUCT_VERSION",
        "--file-description=FILE_DESCRIPTION",
        "--copyright=COPYRIGHT_TEXT",
        "--trademarks=TRADEMARK_TEXT",
        "--enable-plugin=PLUGIN_NAME",
        "--disable-plugin=PLUGIN_NAME",
        "--user-plugin=PATH",
        "--noinclude-setuptools-mode=NOINCLUDE_SETUPTOOLS_MODE",
        "--noinclude-pytest-mode=NOINCLUDE_PYTEST_MODE",
        "--noinclude-unittest-mode=NOINCLUDE_UNITTEST_MODE",
        "--noinclude-IPython-mode=NOINCLUDE_IPYTHON_MODE",
        "--noinclude-dask-mode=NOINCLUDE_DASK_MODE",
        "--noinclude-numba-mode=NOINCLUDE_NUMBA_MODE",
        "--noinclude-default-mode=NOINCLUDE_DEFAULT_MODE",
        "--noinclude-custom-mode=CUSTOM_CHOICES",
    ]
    options = [x.split("=")[0] for x in options_values]
    linux_options = [x for x in options if x.startswith("--linux")]
    windows_options = [x for x in options if x.startswith("--windows")]
    action_map = {key: value for key, value in zip(all_actions, all_descriptions)}
    option_map = {key: value for key, value in zip(options, all_descriptions)}
    flag_map = {key: value for key, value in zip(flags, all_descriptions)}
    flag_map = {}
    option_map = {}
    