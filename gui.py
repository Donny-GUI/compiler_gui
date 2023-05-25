from font import Font
from outputtextbox import OutputTextBox
from asset import Asset
from gif import AnimatedGif
from lib import Nuikta, Pyinstaller
from error import ErrorString

import os
from typing import Tuple
import customtkinter as ctk
from tkinter import END as TEXTEND
import sys
import tkinter as tk
import subprocess
from threading import Thread


    
class CompilerGui(ctk.CTk):
    tabs_ = ("Pyinstaller", "Nuikta", "Compiler", "Decompiler", "Numba", "Settings")
    platform = sys.platform
    Installers = ["Pyinstaller", "Nukita"]
    setting_keys = ["hide infobox", "hide logo"]
    platform_flag = str(sys.platform)[0]
    fonts = Font.get_font_list()
    NUITKA_COMMAND = "python -m nuitka"
    selector_positions = [
        ("top_frame", {"row":0, "column":3, "padx":0, "pady":5, "sticky":'e'}),
        ("flag_button_frame", {"row":0, "column":0, "sticky":'E', "padx":(5,0), "pady":(5,0)}),
        ("bottom_frame", {"row":4, "column":1, "sticky":'we'})
    ]
        
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.pyinstaller_output_textbox_x = 0
        self.wm_attributes("-transparentcolor", "white")
        ## VARIABLES
        self.pyinstaller_current_installer = None
        self.image = None
        self.pyinstaller_path = "<path>"
        self.imagetk = None
        self.icon_path_command = ""
        self.pyinstaller_current_installer = ""
        self.current_feedback = ""
        self.last_feedback = ""
        self.commpiler_info = "123"
        ## FLAGS
        self.hidden_info_box = False
        self.flags_disabled = False
        self.pyinstaller_command = [self.pyinstaller_current_installer, self.pyinstaller_path, self.icon_path_command, "--noconfirm", "--log-level=DEBUG"]
        self.settings = {"hide infobox": 0, "hide logo": 0, "label font":"Trebuchet MS", "label font size":16, "label font style":"bold"}
        self.tabs = {}
        self.tab_frames = {}
        self.object_map = {}
        self.pyinstaller_flag_to_button = {}
        self.pyinstaller_option_to_button = {}
        self.tabview = None
        self.settings_frame = None
        self.threads = []
        self.description_location = None
        #================================================================
        #   SETUP
        #================================================================
        self.setup_tabs()
        self.setup_description_box()
        self.setup_nuikta_tab()
        self.setup_pyinstaller_tab()
        self.setup_compiler_tab()
        self.setup_decompiler_tab()
        self.mainloop()
    
    #////////////////////////////////////////////////////////////////
    #   TAB Setups
    #////////////////////////////////////////////////////////////////
    
    def setup_decompiler_tab(self):
        pass
    
    def setup_tabs(self, *args):
        """ Creates all the necessary tabs for the application
        """
        # create tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="NEW")
        
        for t in self.tabs_:
            self.tabview.add(t)
            tab = self.tabs[t] = self.tabview.tab(t)
            self.tabs[t].bind("<Button-1>", self.tabview_event)
            tab_frame = self.tab_frames[t] = ctk.CTkFrame(tab, width=740, height=750, border_width=0)
            tab_frame.grid(row=1, column=0, sticky='NWE')
            
    def setup_pyinstaller_tab(self):
        self.pyinstaller_top_frame = ctk.CTkFrame(self.tab_frames['Pyinstaller'], border_width=1)
        self.pyinstaller_top_frame.grid(   row=0, column=0, sticky='NWE', padx=5, pady=5)
        
        self.pyinstaller_flag_button_frame = ctk.CTkFrame(self.pyinstaller_top_frame, border_width=2)
        self.pyinstaller_flag_button_frame.grid(row=3, column=0, sticky="WE", columnspan=3, padx=(5,5), pady=(5,5), ipadx=3, ipady=3)
        
        self.pyinstaller_bottom_frame = ctk.CTkFrame(self.tab_frames['Pyinstaller'], border_width=1)
        self.pyinstaller_bottom_frame.grid(row=1, column=0, sticky='WE', padx=5, pady=5)
        
        self.pyinstaller_option_frame = ctk.CTkFrame(self.pyinstaller_top_frame, border_width=1)
        self.pyinstaller_option_frame.grid(row=4, column=0, sticky="WE", columnspan=3, padx=(5,5), pady=(5,5))
        # SElectors
        self.pyinstaller_selector_browse = AnimatedGif(self.pyinstaller_top_frame, Asset.spinpy20, width=20, height=20)
        self.pyinstaller_selector_flags = AnimatedGif(self.pyinstaller_flag_button_frame, Asset.spinpy20, width=20, height=20)
        self.pyinstaller_selector_compile = AnimatedGif(self.pyinstaller_bottom_frame, Asset.spinpy20, width=20, height=20)
        self.pyinstaller_selector_browse.extract_frames()
        self.pyinstaller_selector_flags.extract_frames()
        self.pyinstaller_selector_compile.extract_frames()
        self.pyinstaller_selector_browse.start_animation()
        self.pyinstaller_selector_compile.start_animation()
        self.py_installer_selectors = {"browse":self.pyinstaller_selector_browse, "flags":self.pyinstaller_selector_flags, "compile":self.pyinstaller_selector_compile}
        #=================================================
        #
        # Browse and filepath widgets
        #
        #=================================================
        self.pyinstaller_label_python_script = ctk.CTkLabel(self.pyinstaller_top_frame, text="Python Script: ", font=("Trebuchet MS", 16, 'bold'))
        self.pyinstaller_label_python_script.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        # browse button for python path
        self.pyinstaller_browse_python_script = ctk.CTkButton(self.pyinstaller_top_frame, text="browse")
        self.pyinstaller_browse_python_script.grid(row=0,column=2, padx=(5, 0), pady=5)
        self.pyinstaller_browse_python_script.bind("<Button-1>", lambda event: self.pyinstaller_browse_python_file())
        self.pyinstaller_selector_browse.grid(row=0, column=3, padx=0, pady=5, sticky='e')
        # entry box for pyth path
        self.pyinstaller_entry_python_script = ctk.CTkEntry(self.pyinstaller_top_frame, placeholder_text="Browse to get a file", width=400)
        self.pyinstaller_entry_python_script.grid(row=0, column=1, padx=5, pady=5)
        # browse button for icon file
        self.pyinstaller_browse_icon = ctk.CTkButton(self.pyinstaller_top_frame, text="browse")
        self.pyinstaller_browse_icon.grid(row=1, column=2, padx=5, pady=5)
        self.pyinstaller_browse_icon.bind("<Button-1>", lambda ico_event: self.pyinstaller_browse_icon_file())
        # icon path entry box
        self.pyinstaller_entry_icon  = ctk.CTkEntry(self.pyinstaller_top_frame, placeholder_text="Browse to get a icon file", width=400)
        self.pyinstaller_entry_icon.grid(row=1, column=1, padx=5, pady=5)
        #label for icon file path
        self.pyinstaller_label_icon  = ctk.CTkLabel(self.pyinstaller_top_frame, text="Icon File: ", font=("Trebuchet MS", 16, 'bold'))
        self.pyinstaller_label_icon.grid(row=1, column=0, padx=5, pady=5, sticky='W')
        # combo for installer type 
        self.pyinstaller_current_installer = self.Installers[0]
        #=================================================
        #
        # Command widgets
        #
        #=================================================
        self.pyinstaller_command_label = ctk.CTkLabel(self.pyinstaller_bottom_frame, text="Command", font=("Trebuchet MS", 16, 'bold'))
        self.pyinstaller_command_label.grid(row=0, column=0, sticky='W', padx=(5,5), pady=(5,0))

        self.pyinstaller_command_textbox = ctk.CTkTextbox(self.pyinstaller_bottom_frame, height=50, width=800, border_width=2, bg_color='black', font=("Trebuchet MS", 16, 'bold'))
        self.pyinstaller_command_textbox.grid(row=1, column=0, sticky='WE', padx=5, pady=(1,5))        
        #=================================================
        #
        # Output widgets
        #
        #=================================================
        self.pyinstaller_output_label = ctk.CTkLabel(self.pyinstaller_bottom_frame, text="Output", font=("Trebuchet MS", 16, 'bold'))
        self.pyinstaller_output_label.grid(row=2, column=0, sticky='W', padx=(5,5), pady=(5,0))
        
        self.pyinstaller_output_textbox = OutputTextBox( self.pyinstaller_bottom_frame, height=200, width=725, border_width=2)
        self.pyinstaller_output_textbox.grid( row=3, column=0, sticky='WE', padx=5, pady=(1,5))
        #=================================================
        #
        # argument button widgets
        #
        #=================================================
        self.pyinstaller_arguments_label = ctk.CTkLabel(self.pyinstaller_flag_button_frame, text="Arguments: ", font=("Trebuchet MS", 16, 'bold'))
        self.pyinstaller_arguments_label.grid(row=3, column=0, padx=(2,2), pady=(2,2), sticky='W')
    
        self.pyinstaller_onedir_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--onedir', width=185, state='disabled')
        self.pyinstaller_onedir_button.grid(row=3, column=1, padx=(2,2), pady=(2,2))
        #self.pyinstaller_onedir_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--onedir", self.pyinstaller_onedir_button))
        self.pyinstaller_onedir_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--onedir"))
        
        self.pyinstaller_onefile_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--onefile', width=185, state='disabled')
        self.pyinstaller_onefile_button.grid(row=3, column=2, padx=(2,2), pady=(2,2))
        #self.pyinstaller_onefile_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--onefile", self.pyinstaller_onefile_button))
        self.pyinstaller_onefile_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--onefile"))
        
        self.pyinstaller_clean_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--clean', width=185, state='disabled')
        self.pyinstaller_clean_button.grid(row=3, column=3, padx=(2,2), pady=(2,2))
        #self.pyinstaller_clean_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--clean", self.pyinstaller_clean_button))
        self.pyinstaller_clean_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--clean"))
        
        self.pyinstaller_strip_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--strip', width=185, state='disabled')
        self.pyinstaller_strip_button.grid(row=3, column=4, padx=(2,2), pady=(2,2))
        #self.pyinstaller_strip_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--strip", self.pyinstaller_strip_button))
        self.pyinstaller_strip_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--strip"))
        
        self.pyinstaller_noupx_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--noupx', width=185, state='disabled')
        self.pyinstaller_noupx_button.grid(row=3, column=1, padx=(2,2), pady=(2,2))
        #self.pyinstaller_noupx_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--noupx", self.pyinstaller_noupx_button))
        self.pyinstaller_noupx_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--noupx"))
        
        self.pyinstaller_console_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--console', width=185, state='disabled')
        self.pyinstaller_console_button.grid(row=3, column=1, padx=(2,2), pady=(2,2))
        #self.pyinstaller_console_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--console", self.pyinstaller_console_button))
        self.pyinstaller_console_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--console"))
        
        self.pyinstaller_windowed_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--windowed', width=185, state='disabled')
        self.pyinstaller_windowed_button.grid(row=4, column=2, padx=(2,2), pady=(2,2))
        #self.pyinstaller_windowed_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--windowed", self.pyinstaller_windowed_button))
        self.pyinstaller_windowed_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--windowed"))
        
        self.disablewindowedtraceback_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--disable-windowed-traceback', width=185, state='disabled')
        self.disablewindowedtraceback_button.grid(row=4, column=3, padx=(2,2), pady=(2,2))
        #self.disablewindowedtraceback_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--disable-windowed-traceback", self.disablewindowedtraceback_button))
        self.disablewindowedtraceback_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--disable-windowed-traceback"))
        
        self.noembeddedmanifest_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--no-embedded-manifest', width=185, state='disabled')
        self.noembeddedmanifest_button.grid(row=4, column=4, padx=(2,2), pady=(2,2))
        #self.noembeddedmanifest_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--no-embedded-manifest", self.noembeddedmanifest_button))
        self.noembeddedmanifest_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--no-embedded-manifest"))
        
        self.uacadmin_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--uac-admin', width=185, state='disabled')
        self.uacadmin_button.grid(row=5, column=1, padx=(2,2), pady=(2,2))
        #self.uacadmin_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--uac-admin", self.uacadmin_button))
        self.uacadmin_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--uac-admin"))
        
        self.uacuiaccess_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--uac-uiaccess', width=185, state='disabled')
        self.uacuiaccess_button.grid(row=4, column=1, padx=(2,2), pady=(2,2))
        #self.uacuiaccess_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--uac-uiaccess", self.uacuiaccess_button))
        self.uacuiaccess_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--uac-uiaccess"))
        
        self.winprivateassemblies_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--win-private-assemblies', width=185, state='disabled')
        self.winprivateassemblies_button.grid(row=5, column=2, padx=(2,2), pady=(2,2))
        #self.winprivateassemblies_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--win-private-assemblies", self.winprivateassemblies_button))
        self.winprivateassemblies_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--win-private-assemblies"))
        
        self.winnopreferredirects_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--win-no-prefer-redirects', width=185, state='disabled')
        self.winnopreferredirects_button.grid(row=5, column=3, padx=(2,2), pady=(2,2))
        #self.winnopreferredirects_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--win-no-prefer-redirects", self.winnopreferredirects_button))
        self.winnopreferredirects_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--win-no-prefer-redirects"))
        
        self.bootloaderignoresignals_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text='--bootloader-ignore-signals', width=185, state='disabled')
        self.bootloaderignoresignals_button.grid(row=5, column=4, padx=(2,2), pady=(2,2))
        #self.bootloaderignoresignals_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--bootloader-ignore-signals", self.bootloaderignoresignals_button))
        self.bootloaderignoresignals_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--bootloader-ignore-signals"))
        
        self.argvemulation_button = ctk.CTkButton(self.pyinstaller_flag_button_frame, text="--argv-emulation", state='disabled', width=185)
        self.argvemulation_button.grid(row=6, column=1, padx=(2,2), pady=(2,2))
        #self.argvemulation_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--argv-emulation", self.argvemulation_button))
        self.argvemulation_button.bind("<Enter>", lambda event2:  self.pyinstaller_set_description_box("--argv-emulation"))

        self.pyinstaller_compile_button = ctk.CTkButton(self.pyinstaller_bottom_frame, text='Compile', width=725, state='disabled')
        self.pyinstaller_compile_button.grid(row=4, column=0, sticky='we')
        #=================================================
        #
        # option flag widgets
        #
        #=================================================
        self.pyinstaller_options_label = ctk.CTkLabel(self.pyinstaller_option_frame, text='Options:      ',font=("Trebuchet MS", 16, "bold"))
        self.pyinstaller_options_label.grid(row=0, column=0, sticky='w', padx=(2,2), pady=(2,2), )
    
        self.pyinstaller_name_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--name', width=185)
        self.pyinstaller_name_button.grid(row=2, column=4, padx=(2,2), pady=(2,2))
        #self.pyinstaller_name_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--name', self.pyinstaller_name_button))
        self.pyinstaller_name_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--name'))
    
        self.addbinary_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--add-binary', width=185)
        self.addbinary_button.grid(row=0, column=1, padx=(2,2), pady=(2,2))
        #self.addbinary_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--add-binary', self.addbinary_button))
        self.addbinary_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--add-binary'))
    
        self.pyinstaller_paths_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--paths', width=185)
        self.pyinstaller_paths_button.grid(row=0, column=2, padx=(2,2), pady=(2,2))
        #self.pyinstaller_paths_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--paths', self.pyinstaller_paths_button))
        self.pyinstaller_paths_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--paths'))
    
        self.hiddenimport_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--hidden-import', width=185)
        self.hiddenimport_button.grid(row=0, column=3, padx=(2,2), pady=(2,2))
        #self.hiddenimport_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--hidden-import', self.hiddenimport_button))
        self.hiddenimport_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--hidden-import'))
    
        self.collectsubmodules_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--collect-submodules', width=185)
        self.collectsubmodules_button.grid(row=0, column=4, padx=(2,2), pady=(2,2))
        #self.collectsubmodules_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--collect-submodules', self.collectsubmodules_button))
        self.collectsubmodules_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--collect-submodules'))
        
        self.collectdata_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--collect-data', width=185)
        self.collectdata_button.grid(row=3, column=4, padx=(2,2), pady=(2,2))
        #self.collectdata_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--collect-data', self.collectdata_button))
        self.collectdata_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--collect-data'))
    
        self.collectbinaries_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--collect-binaries', width=185)
        self.collectbinaries_button.grid(row=3, column=2, padx=(2,2), pady=(2,2))
        #self.collectbinaries_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--collect-binaries', self.collectbinaries_button))
        self.collectbinaries_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--collect-binaries'))
    
        self.collectall_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--collect-all', width=185)
        self.collectall_button.grid(row=1, column=1, padx=(2,2), pady=(2,2))
        #self.collectall_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--collect-all', self.collectall_button))
        self.collectall_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--collect-all'))
    
        self.specpath_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--specpath', width=185)
        self.specpath_button.grid(row=1, column=2, padx=(2,2), pady=(2,2))
        #self.specpath_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--specpath', self.specpath_button))
        self.specpath_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--specpath'))
    
        self.adddata_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--add-data', width=185)
        self.adddata_button.grid(row=1, column=3, padx=(2,2), pady=(2,2))
        #self.adddata_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--add-data', self.adddata_button))
        self.adddata_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--add-data'))
    
        self.copymetadata_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--copy-metadata', width=185)
        self.copymetadata_button.grid(row=1, column=4, padx=(2,2), pady=(2,2))
        #self.copymetadata_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--copy-metadata', self.copymetadata_button))
        self.copymetadata_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--copy-metadata'))
    
        self.recursivecopymetadata_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--recursive-copy-metadata', width=185)
        self.recursivecopymetadata_button.grid(row=3, column=1, padx=(2,2), pady=(2,2))
        #self.recursivecopymetadata_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--recursive-copy-metadata', self.recursivecopymetadata_button))
        self.recursivecopymetadata_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--recursive-copy-metadata'))
    
        self.additionalhooksdir_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--additional-hooks-dir', width=185)
        self.additionalhooksdir_button.grid(row=3, column=3, padx=(2,2), pady=(2,2))
        #self.additionalhooksdir_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--additional-hooks-dir', self.additionalhooksdir_button))
        self.additionalhooksdir_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--additional-hooks-dir'))
    
        self.runtimehook_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--runtime-hook', width=185)
        self.runtimehook_button.grid(row=2, column=1, padx=(2,2), pady=(2,2))
        #self.runtimehook_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--runtime-hook', self.runtimehook_button))
        self.runtimehook_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--runtime-hook'))
    
        self.excludemodule_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--exclude-module', width=185)
        self.excludemodule_button.grid(row=2, column=2, padx=(2,2), pady=(2,2))
        #self.excludemodule_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--exclude-module', self.excludemodule_button))
        self.excludemodule_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--exclude-module'))
    
        self.splash_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--splash', width=185)
        self.splash_button.grid(row=2, column=3, padx=(2,2), pady=(2,2))
        #self.splash_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--splash', self.splash_button))
        self.splash_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--splash'))
    
        self.osxbundleidentifier_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--osx-bundle-identifier', width=185, state="disabled")
        self.osxbundleidentifier_button.grid(row=4, column=1, padx=(2,2), pady=(2,2))
        #self.osxbundleidentifier_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--osx-bundle-identifier', self.splash_button))
        self.osxbundleidentifier_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--osx-bundle-identifier'))
    
        self.targetarchitecture_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--target-architecture', width=185, state="disabled")
        self.targetarchitecture_button.grid(row=4, column=2, padx=(2,2), pady=(2,2))
        #self.targetarchitecture_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--target-architecture', self.splash_button))
        self.targetarchitecture_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--target-architecture'))
    
        self.codesignidentity_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--codesign-identity', width=185, state="disabled")
        self.codesignidentity_button.grid(row=4, column=3, padx=(2,2), pady=(2,2))
        #self.codesignidentity_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--codesign-identity', self.splash_button))
        self.codesignidentity_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--codesign-identity'))
    
        self.osxentitlementsfile_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--osx-entitlements-file', width=185, state="disabled")
        self.osxentitlementsfile_button.grid(row=4, column=4, padx=(2,2), pady=(2,2))
        #self.osxentitlementsfile_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--osx-entitlements-file', self.splash_button))
        self.osxentitlementsfile_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--osx-entitlements-file'))
    
        self.runtimetmpdir_button = ctk.CTkButton(self.pyinstaller_option_frame, text='--runtime-tmpdir', width=185, state="disabled")
        self.runtimetmpdir_button.grid(row=5, column=1, padx=(2,2), pady=(2,2))
        #self.runtimetmpdir_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--runtime-tmpdir', self.splash_button))
        self.runtimetmpdir_button.bind("<Enter>", lambda descoevent: self.pyinstaller_set_description_box_option('--runtime-tmpdir'))
        
        self.pyinstaller_exit_compile_button = ctk.CTkButton(self.pyinstaller_bottom_frame, text="Exit Build", width=186, height= 70)
        self.pyinstaller_exit_compile_button.bind("<Enter>", lambda exitevent: self.pyinstaller_exit_compile_event())
        self.pyinstaller_finished_button = ctk.CTkButton(self.pyinstaller_bottom_frame, text="Finished!", width=120, height=70, fg_color='green')
        
        self.pyinstaller_flag_buttons = [
            self.pyinstaller_onedir_button, self.pyinstaller_onefile_button, self.pyinstaller_clean_button, self.pyinstaller_strip_button, self.pyinstaller_noupx_button, self.pyinstaller_console_button, self.pyinstaller_windowed_button, 
            self.disablewindowedtraceback_button, self.noembeddedmanifest_button, self.uacadmin_button, self.uacuiaccess_button, self.winprivateassemblies_button, 
            self.winnopreferredirects_button, self.bootloaderignoresignals_button, 
        ]
        self.pyinstaller_option_buttons = [
            self.pyinstaller_name_button, self.addbinary_button, self.pyinstaller_paths_button, self.hiddenimport_button, self.collectsubmodules_button, 
            self.collectdata_button, self.collectbinaries_button, self.collectall_button, self.specpath_button, self.adddata_button, 
            self.copymetadata_button, self.recursivecopymetadata_button, self.additionalhooksdir_button, 
            self.runtimehook_button, self.excludemodule_button, self.splash_button, self.runtimetmpdir_button      
        ]
        self.pyinstaller_commandtext = ""
        self.pyinstaller_flag_to_button = {
            "--onedir":self.pyinstaller_onedir_button, "--onefile":self.pyinstaller_onefile_button, "--clean":self.pyinstaller_clean_button, "--strip":self.pyinstaller_strip_button, 
            "--noupx":self.pyinstaller_noupx_button, "--console":self.pyinstaller_console_button, "--windowed":self.pyinstaller_windowed_button, "--disable-windowed-traceback":self.disablewindowedtraceback_button,
            "--no-embedded-manifest":self.noembeddedmanifest_button, "--uac-admin": self.uacadmin_button, "--win-private-assemblies":self.winprivateassemblies_button,
            '--win-no-prefer-redirects':self.winnopreferredirects_button, "--bootloader-ignore-signals":self.bootloaderignoresignals_button, "--argv-emulation":self.argvemulation_button
            }
        self.pyinstaller_option_to_button = {
            "--name":self.pyinstaller_name_button, "--add-binary":self.addbinary_button, "--paths":self.pyinstaller_paths_button, "--hidden-import":self.hiddenimport_button, "--collect-submodules":self.collectsubmodules_button,
            "--collect-data":self.collectdata_button, "--collect-binaries":self.collectbinaries_button, "--collect-all":self.collectall_button, "--specpath":self.specpath_button, "--add-data":self.adddata_button,
            "--copy-metadata":self.copymetadata_button, "--recursive-copy-metadata":self.recursivecopymetadata_button, "--additional-hooks-dir":self.additionalhooksdir_button,
            "--runtime-hook":self.runtimehook_button, "--exclude-module":self.excludemodule_button, "--splash":self.splash_button,
            "--osx-bundle-identifier":self.osxbundleidentifier_button, "--target-architecture":self.targetarchitecture_button, "--codesign-identity":self.codesignidentity_button,
            "--osx-entitlements-file":self.osxentitlementsfile_button, "--runtime-tmpdir":self.runtimetmpdir_button
        }
        self.pyinstaller_label_fontables = (

            self.pyinstaller_label_python_script,
            self.pyinstaller_label_icon,
            self.pyinstaller_arguments_label,
            self.pyinstaller_command_label,
            self.pyinstaller_output_label,
            self.pyinstaller_command_textbox,
        )

        self.pyinstaller_button_fontables = (
            self.pyinstaller_onedir_button,self.pyinstaller_onefile_button,self.pyinstaller_clean_button,self.pyinstaller_strip_button,self.pyinstaller_noupx_button,self.pyinstaller_console_button,self.pyinstaller_windowed_button,
            self.disablewindowedtraceback_button,self.noembeddedmanifest_button,self.uacadmin_button,self.uacuiaccess_button,self.winprivateassemblies_button,
            self.winnopreferredirects_button,self.bootloaderignoresignals_button,self.argvemulation_button,self.pyinstaller_compile_button,self.pyinstaller_name_button,self.addbinary_button,
            self.pyinstaller_paths_button,self.hiddenimport_button,self.collectsubmodules_button,self.collectdata_button,self.collectbinaries_button,self.collectall_button,
            self.specpath_button,self.adddata_button,self.copymetadata_button,self.recursivecopymetadata_button,self.additionalhooksdir_button,self.runtimehook_button,
            self.excludemodule_button,self.splash_button,self.osxbundleidentifier_button,self.targetarchitecture_button,self.codesignidentity_button,
            self.osxentitlementsfile_button,self.runtimetmpdir_button
        )
        self.pyinstaller_flag_button_frame.grid(row=3, column=0, sticky="WE", columnspan=3, padx=(5,5), pady=(5,5), ipadx=3, ipady=3)
        self.pyinstaller_option_frame.grid(row=4, column=0, sticky="WE", columnspan=3, padx=(5,5), pady=(5,5))
        self.pyinstaller_output_textbox.grid( row=3, column=0, sticky='WE', padx=5, pady=(1,5))
        
        self.pyinstaller_disable_all_flag_buttons()
        self.pyinstaller_disable_all_option_buttons()
        self.pyinstaller_reset_command()
        self.pyinstaller_command_to_box()
    
    def setup_nuikta_tab(self):    
        self.nuikta_output_textbox_x = 0
        self.nuikta_current_installer = None
        self.nuikta_path = "<path>"
        self.nuikta_current_installer = ""
        self.nuikta_current_feedback = ""
        self.nuikta_last_feedback = ""
        self.nuikta_commpiler_info = "123"
        self.nuikta_commandtext = ""
        self.nuikta_flag_to_button = {}
        self.nuikta_option_to_button = {}
        self.nuikta_command = [self.nuikta_current_installer, self.nuikta_path, "--no-progressbar" ]
        self.nuikta_top_frame = ctk.CTkFrame(self.tab_frames["Nuikta"], width=740, height=300, border_width=1)
        self.nuikta_top_frame.grid(row=0, column=0, pady=(5,5), padx=(5,5), sticky='NWE')
        self.nuikta_bottom_frame = ctk.CTkFrame(self.tab_frames["Nuikta"], width=740, height=350, border_width=1)
        self.nuikta_flag_button_frame = ctk.CTkScrollableFrame(self.nuikta_bottom_frame, border_width=2, width = 700)
        self.nuikta_option_frame = ctk.CTkScrollableFrame(self.nuikta_top_frame, border_width=1, width= 800)
        self.nuikta_filepath_label = ctk.CTkLabel(self.nuikta_top_frame, text="Python Script Path:", font=("Trebuchet MS", 16, 'bold'))
        self.nuikta_filepath_label.grid(row=0, column=0, pady=(1,1), padx=(1,1), sticky='W')
        self.nuikta_filepath_entry = ctk.CTkEntry(self.nuikta_top_frame,  width=400)
        self.nuikta_filepath_entry.grid(row=0, column=1, pady=(1,1), padx=(1,1), sticky='W')
        self.nuikta_filepath_browse_button = ctk.CTkButton(self.nuikta_top_frame, text='browse')
        self.nuikta_filepath_browse_button.bind("<Button-1>", self.browse_filepath_nuikta)
        self.nuikta_filepath_browse_button.grid(row=0, column=2, pady=(1,1), padx=(1,1), sticky='W')
        self.nuikta_label_icon  = ctk.CTkLabel(self.nuikta_top_frame, text="Icon File: ", font=("Trebuchet MS", 16, 'bold'))
        self.nuikta_label_icon.grid(row=1, column=0, padx=1, pady=1, sticky='W')
        self.nuikta_entry_icon  = ctk.CTkEntry(self.nuikta_top_frame, placeholder_text="Browse to get a icon file", width=400)
        self.nuikta_entry_icon.grid(row=1, column=1, padx=1, pady=1, sticky='W')
        self.nuikta_browse_icon = ctk.CTkButton(self.nuikta_top_frame, text="browse")
        self.nuikta_browse_icon.grid(row=1, column=2, padx=1, pady=1, sticky='W')
        #self.nuikta_browse_icon.bind("<Button-1>", self.browse_icon_nuikta)
        # SElectors
        self.nuikta_selector_browse = AnimatedGif(self.nuikta_top_frame, Asset.spinpy20, width=20, height=20)
        self.nuikta_selector_browse.grid(row=0, column=3, padx=0, pady=0)
        self.nuikta_selector_flags = AnimatedGif(self.nuikta_bottom_frame, Asset.spinpy20, width=20, height=20)

        self.nuikta_selector_browse.extract_frames()
        self.nuikta_selector_browse.start_animation()
        self.nuikta_selector_flags.extract_frames()
        self.nuikta_selector_flags.start_animation()
        self.nuikta_action_buttons = {}
        self.nukes = []
        rind = 3
        cind = 0
        if self.platform_flag == 'd':
            self.dont_tags = ["--win", '--linux']
        elif self.platform_flag == 'w':
            self.dont_tags = ["--macos-", '--linux']
        elif self.platform_flag == 'l':
            self.dont_tags = ["--macos-", '--win']
        for index, item in enumerate(Nuikta.all_actions):
            if item.startswith("--disable-"):
                self.nuikta_command.append(item)
                continue
            for t in self.dont_tags:
                if item.startswith(t):
                    continue 
            self.nuikta_action_buttons[item] = ctk.CTkButton(self.nuikta_option_frame, text=item, width=185, state='normal')
            self.nuikta_action_buttons[item].grid(row=rind, column=cind, padx=(1,1), pady=(2,2), sticky='NWE')
            self.nuikta_action_buttons[item].bind('<Button-1>', lambda oevent: self.nuikta_add_option(item, self.nuikta_action_buttons[item]))
            self.nuikta_action_buttons[item].bind("<Enter>", lambda descoevent: self.nuikta_set_description_box_option(item))
            
            cind+=1
            if cind == 5:
                cind = 0
                rind+=1
        
        self.nuikta_command_label = ctk.CTkLabel(self.nuikta_bottom_frame, text="Command", font=("Trebuchet MS", 16, 'bold'))
        self.nuikta_command_textbox = ctk.CTkTextbox(self.nuikta_bottom_frame, height=50, width=800, border_width=2, bg_color='black', font=("Trebuchet MS", 16, 'bold'))
        self.nuikta_output_label = ctk.CTkLabel(self.nuikta_bottom_frame, text="Output", font=("Trebuchet MS", 16, 'bold'))
        self.nuikta_output_textbox = OutputTextBox( self.nuikta_bottom_frame, height=200, width=725, border_width=2)
        self.nuikta_compile_button = ctk.CTkButton(self.nuikta_bottom_frame, text='Compile', width=725, state='disabled')
        self.nuikta_exit_compile_button = ctk.CTkButton(self.nuikta_bottom_frame, text='EXIT', width=200, height=100, fg_color='red')
        self.nuikta_finished_button = ctk.CTkButton(self.nuikta_bottom_frame, text="Finished!", width=500, height=100)
        self.nuikta_commandtext = ""
        self.nuikta_flag_to_button = {}
        self.nuikta_option_to_button = {}
        self.nuikta_button_fontables = ()
        self.nuikta_command = ["nuikta", "<path>"]
        
        self.nuikta_flag_button_frame.grid(row=3, column=0, sticky="WE", columnspan=3, padx=(5,5), pady=(5,5), ipadx=3, ipady=3)
        self.nuikta_option_frame.grid(row=4, column=0, sticky="WE", columnspan=3, padx=(5,5), pady=(5,5))
        self.nuikta_bottom_frame.grid(row=1, column=0, pady=(5,5), padx=(5,5), sticky='NWE')
        
        self.nuikta_command_textbox.grid(row=1, column=0, sticky='WE', padx=5, pady=(1,5))  
        self.nuikta_command_label.grid(row=0, column=0, sticky='W', padx=(5,5), pady=(5,0))
        self.nuikta_flag_button_frame.grid(row=3, column=0, sticky="WE", columnspan=3, padx=(5,5), pady=(5,5), ipadx=3, ipady=3)
        self.nuikta_compile_button.grid(row=4, column=0, padx=5, pady=(5,5), sticky='NW')
            
        #self.nuikta_output_label.grid(row=2, column=0, sticky='W', padx=(5,5), pady=(5,0))
        self.nuikta_output_textbox.grid( row=3, column=0, sticky='WE', padx=5, pady=(1,5))
        
        self.nuikta_command_to_box()
        
    def setup_compiler_tab(self):
        self.compiler_path = ""
        self.compiler_dirpath = ""
        self.python_cmd = "python" if sys.platform.startswith("w") else "python3"
        self.compiler_command = [f"{self.python_cmd} -m py_compile", ""]
        self.compiler_filepath_label = ctk.CTkLabel(self.tab_frames["Compiler"], text="Compiling File: ", font=("Trebuchet MS", 16, 'bold'))
        self.compiler_filepath_label.grid(row=0, column=0, padx=(2,2), pady=(2,2), sticky="NW")
        self.compiler_filepath_entry = ctk.CTkEntry(self.tab_frames["Compiler"], font=("Trebuchet MS", 12, 'bold'), width=450)
        self.compiler_filepath_entry.grid(row=0, column=1, padx=(2,2), pady=(2,2), sticky="NW")
        self.compiler_filepath_browse = ctk.CTkButton(self.tab_frames["Compiler"], font=("Trebuchet MS", 14, 'bold'), text='browse')
        self.compiler_filepath_browse.grid(row=0, column=2, padx=(2,2), pady=(2,2), sticky="NW")
        self.compiler_filepath_browse.bind("<Button-1>", self.compiler_filepath_browse_event)
        self.compiler_compile_button = ctk.CTkButton(self.tab_frames["Compiler"], text="compile", font=("Trebuchet MS", 14, 'bold'))
        self.compiler_compile_button.grid(column=1, row=2, padx=(2,2), pady=(2,2), sticky="NW")
        
        self.compiler_dirpath_label = ctk.CTkLabel(self.tab_frames["Compiler"], text="Compiling Directory: ", font=("Trebuchet MS", 16, 'bold'))
        self.compiler_dirpath_label.grid(row=1, column=0, padx=(2,2), pady=(2,2), sticky="NW")
        self.compiler_dirpath_entry = ctk.CTkEntry(self.tab_frames["Compiler"], font=("Trebuchet MS", 12, 'bold'), width=450)
        self.compiler_dirpath_entry.grid(row=1, column=1, padx=(2,2), pady=(2,2), sticky="NW")
        self.compiler_dirpath_browse = ctk.CTkButton(self.tab_frames["Compiler"], font=("Trebuchet MS", 14, 'bold'), text='browse')
        self.compiler_dirpath_browse.grid(row=1, column=2, padx=(2,2), pady=(2,2), sticky="NW")
        self.compiler_dirpath_browse.bind("<Button-1>", self.compiler_dirpath_browse_event)
        
        self.compiler_output_textbox = OutputTextBox(self.tab_frames["Compiler"], width=725, height=300, font=("Trebuchet MS", 14, 'italic'))
        self.compiler_output_textbox.grid(row=3, column=1, padx=(2,2), pady=(2,2), sticky='NW')
    
    def compiler_set_output_box(self, text, obj):
        self.compiler_output_textbox.new_text(obj, text)
    
    def compiler_checker_thread(self, *args):
        self.process.wait()

    def compiler_compile_thread(self, *args):
        while True:  # While the subprocess is running
            self.last_feedback = self.current_feedback
            if self.process.stderr != None:
                self.error_feedback = self.process.stderr.readline().decode().strip()
                self.compiler_set_output_box(self.error_feedback, "ERROR")
            if self.process.stdout != None:
                self.current_feedback = self.process.stdout.readline().decode().strip()
                if self.current_feedback != self.last_feedback:
                    self.compiler_set_output_box(f"All .py files compiled to bytecode in {self.compiler_dirpath}", "Compiler")
            self.return_code = self.process.returncode
            self.process.returncode
            if self.return_code == 0:
                break
            elif self.return_code == 1:
                break
        return

    def compiler_compile_event(self, *args):
        cmdstring = " ".join(self.compiler_command)
        self.process = subprocess.Popen(cmdstring, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        self.current_feedback = ""
        self.last_feedback = ""
        self.commpiler_info = "123"
        self.return_code = self.process.returncode
        self.compiler_compile_threader = Thread(target=self.compiler_compile_thread, args=(None, ))
        self.check_thread = Thread(target=self.compiler_checker_thread, args=(None,))
        self.compiler_compile_threader.start()
        self.check_thread.start()
    
    def compiler_dirpath_browse_event(self, *args):
        self.compiler_command = [f"{self.python_cmd} -m py_compile", ""]
        self.compiler_dirpath = ctk.filedialog.askdirectory()
        print(self.compiler_dirpath)
        try:
            self.compiler_dirpath = self.compiler_dirpath
        except AttributeError:
            return
        if os.path.exists(self.compiler_dirpath):
            self.compiler_dirpath_entry.delete(0, "end")
            self.compiler_dirpath_entry.insert(0, self.compiler_dirpath)
            files = [x for x in os.listdir() if os.path.isfile(x)]
            pyfiles = [x for x in files if x.split(".")[1] == "py"]
            paths = [os.path.join(self.compiler_dirpath, file) for file in pyfiles]
            pathstring = " ".join(paths)
            self.compiler_command[1] = pathstring
            print(self.compiler_command)
            self.compiler_compile_button.bind("<Button-1>", self.compiler_compile_event)
    
    def compiler_filepath_browse_event(self, *args):
        self.compiler_command = [f"{self.python_cmd} -m py_compile", ""]
        self.compiler_path = ctk.filedialog.askopenfile()
        try:
            self.compiler_path = self.compiler_path.name
        except AttributeError:
            return
        if self.pyinstaller_path is not None:
            if not self.compiler_path.endswith(".py"):
                return
            if self.compiler_path.endswith(".py"):
                self.compiler_filepath_entry.delete(0, "end")
                self.compiler_filepath_entry.insert(0, self.compiler_path)
                self.compiler_command[1] = self.compiler_path
                self.compiler_compile_button.bind("<Button-1>", self.compiler_compile_event)
                   
    def setup_description_box(self):
        self.right_info_box_frame = ctk.CTkFrame(self, border_width=2)
        self.right_info_box_frame.grid(row=0, column=1, pady=(400, 1), padx=5)
        
        self.description_box = ctk.CTkTextbox(self.right_info_box_frame, width=350, height=200, font=("Trebuchet MS", 18, "italic"), fg_color="black")
        self.description_box.grid(row=0, column=0, sticky='NWE', padx=5, pady=(5,5))
    
        self.description_title = ctk.CTkLabel(self.right_info_box_frame, text="             ", font=("Consolas", 18, "bold"), anchor='w')
        self.description_title.grid(row=1, column=0, padx=(5, 5), pady=(5,5), sticky='NWE', )
    
        self.type_title = ctk.CTkLabel(self.right_info_box_frame, text="             ", font=("Consolas", 18, "bold"), anchor='w')
        self.type_title.grid(row=2, column=0, padx=(5, 5), pady=(5,5), sticky='NWE', )
    
        self.status_title = ctk.CTkLabel(self.right_info_box_frame, text="         ", font=("Consolas", 18, "bold"), anchor='w')
        self.status_title.grid(row=3, column=0, padx=(5, 5), pady=(5,5), sticky='NWE', )
    
        self.value_title = ctk.CTkLabel(self.right_info_box_frame, text="         ", font=("Consolas", 18, "bold"), anchor='w')
        self.value_title.grid(row=4, column=0, padx=(5, 5), pady=(5,5), sticky='NWE')

    #////////////////////////////////////////////////////////////////
    #   Pyinstaller Compile Events
    #////////////////////////////////////////////////////////////////

    def pyinstaller_exit_compile_event(self):
        self.pyinstaller_restore_view()
          
    def pyinstaller_compile_thread(self, *args):
        """ Thread that is called when the compile button is clicked """        
        while True:  # While the subprocess is running
            self.last_feedback = self.current_feedback
            if self.process.stderr != None:
                self.error_feedback = self.process.stderr.readline().decode().strip()
                self.pyinstaller_set_output_box(self.error_feedback, "ERROR", )
            if self.process.stdout != None:
                self.current_feedback = self.process.stdout.readline().decode().strip()
                if self.current_feedback != self.last_feedback:
                    self.pyinstaller_set_output_box(self.current_feedback, "Compiler")
            self.return_code = self.process.returncode
            self.process.returncode
            if self.return_code == 0:
                break
            elif self.return_code == 1:
                break
        return
    
    def pyinstaller_restore_view(self, *args):
        """Restore the original view from before the compiler took over
        """
        self.pyinstaller_exit_compile_button.grid_forget()
        self.pyinstaller_finished_button.grid_forget()
        self.pyinstaller_compile_button.configure(state='normal')
        self.pyinstaller_compile_button.grid(row=4, column=0, sticky='we')
        self.pyinstaller_top_frame.grid(   row=0, column=0, sticky='WE', padx=5, pady=5)
        self.pyinstaller_output_textbox.configure(height=200, width=725, border_width=2)
        self.pyinstaller_command_textbox.grid(row=1, column=0, sticky='WE', padx=5, pady=(1,5))
        self.pyinstaller_finished_button.grid_forget()
        

        self.process.terminate()
    
    def pyinstaller_checker_thread(self, *args):
        """waits for the compile thread to finish and then fixes the buttons
        """
        self.process.wait()
        self.pyinstaller_finished_button = ctk.CTkButton(self.pyinstaller_bottom_frame, text="Finished!", width=120, height=70, fg_color='green')
        self.pyinstaller_finished_button.grid(column=0,row=0)
        self.pyinstaller_finished_button.bind("<Button-1>", self.pyinstaller_restore_view)  
        
    def pyinstaller_compile_event(self, *args):
        """ Called When the compile button is clicked
        """
        self.pyinstaller_output_textbox.delete("0.0", "end")
        self.pyinstaller_set_output_box(f"Compiling {self.pyinstaller_entry_python_script.get()}...", "Compiler")
        cmdstring = " ".join(self.pyinstaller_command)
        self.process = subprocess.Popen(cmdstring, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        self.pyinstaller_exit_compile_button.grid(column=0, row=0)
        self.current_feedback = ""
        self.last_feedback = ""
        self.commpiler_info = "123"
        self.return_code = self.process.returncode
        self.pyinstaller_compile_threader = Thread(target=self.pyinstaller_compile_thread, args=(None, ))
        self.check_thread = Thread(target=self.pyinstaller_checker_thread, args=(None,))
        self.pyinstaller_compile_threader.start()
        self.check_thread.start()
        
    #////////////////////////////////////////////////////////////////
    #   PYINSTALLER FONT ADJUST
    #////////////////////////////////////////////////////////////////
    def pyinstaller_adjust_button_fonts(self, *args):
        """Called when one of the comboboxes regarding font size is selected
        """
        if args[0] in self.fonts:
            font = args[0]
        else:
            font = self.button_font_combobox.get()
        size = int(self.button_font_size_combobox.get())
        style = self.button_font_style_combobox.get()
        weight = 'bold' if style == 'bold' else 'normal'
        slant = "italic" if style == 'italic' else "roman"
        
        ff = ctk.CTkFont(family=font, size=size, weight=weight, slant=slant)
        for button in self.pyinstaller_button_fontables:
            button.configure(font=ff)
         
    def pyinstaller_adjust_label_fonts(self, *args):
        """ Called when the font is changed for the labels in the settings panel
        """
        if args[0] in self.fonts:
            font = args[0]
        else:
            font = self.label_font_combobox.get()
        size = int(self.label_font_size_combobox.get())
        style = self.label_font_style_combobox.get()
        weight = 'bold' if style == 'bold' else 'normal'
        slant = "italic" if style == 'italic' else "roman"
        
        ff = ctk.CTkFont(family=font, size=size, weight=weight, slant=slant)
        for label in self.pyinstaller_label_fontables:
            label.configure(font=ff)
    
    #////////////////////////////////////////////////////////////////
    #   SETTING EVENTS
    #////////////////////////////////////////////////////////////////
    def check_settings(self, *args):
        """ called when a setting is changed
        """
        print(args)
        self.settings[args[1]] = args[0]
        self.apply_settings()
    
    def apply_settings(self):
        """ Called after the settings have been checked to apply the new settings
        """
        for setting in self.settings.items():
            if setting[0] == 'hide infobox':
                if setting[1] == True:
                    self.right_info_box_frame.destroy()
                    self.description_box.destroy()
                    self.description_title.destroy()
                    self.type_title.destroy()
                    self.status_title.destroy()
                    self.value_title.destroy()
                    self.hidden_info_box = True
                else:
                    self.right_info_box_frame = ctk.CTkFrame(self, border_width=2, width=600)
                    self.right_info_box_frame.grid(row=0, column=1, pady=(480, 1), padx=1, sticky='WE')
                    self.description_box = ctk.CTkTextbox(self.right_info_box_frame, width=350, height=200, font=("Trebuchet MS", 18, "italic"), fg_color="black")
                    self.description_box.grid(row=0, column=0, sticky='NWE', padx=5, pady=(5,5))
                    self.description_title = ctk.CTkLabel(self.right_info_box_frame, text="             ", font=("Consolas", 18, "bold"), anchor='w')
                    self.description_title.grid(row=1, column=0, padx=(5, 5), pady=(5,5), sticky='NWE', )
                    self.type_title = ctk.CTkLabel(self.right_info_box_frame, text="             ", font=("Consolas", 18, "bold"), anchor='w')
                    self.type_title.grid(row=2, column=0, padx=(5, 5), pady=(5,5), sticky='NWE', )
                    self.status_title = ctk.CTkLabel(self.right_info_box_frame, text="         ", font=("Consolas", 18, "bold"), anchor='w')
                    self.status_title.grid(row=3, column=0, padx=(5, 5), pady=(5,5), sticky='NWE', )
                    self.value_title = ctk.CTkLabel(self.right_info_box_frame, text="         ", font=("Consolas", 18, "bold"), anchor='w')
                    self.value_title.grid(row=4, column=0, padx=(5, 5), pady=(5,5), sticky='NWE')
                    self.hidden_info_box = False
                        
            elif setting[1] == 'hide logo':
                if setting[1] == True:
                    self.logo_canvas.destroy()
                else:
                    self.logo_canvas = tk.Canvas(self, width=269, height=326, background='gray', borderwidth=0, border=0)
                    self.logo_canvas.grid(row=0, column=1, sticky='WN')
    
    #////////////////////////////////////////////////////////////////
    #   PYINSTALLER FLAG ENABLE/DISABLE
    #////////////////////////////////////////////////////////////////
    
    def pyinstaller_disable_os_specific_flags(self):
        """ Disables flags that can not be used on your operating system
        """
        if self.platform.startswith("w"):
            for flag in Pyinstaller.mac_flags:
                widget = self.pyinstaller_flag_to_button[flag]
                widget.configure(state="disabled")
            for option in Pyinstaller.mac_options:
                widget = self.pyinstaller_option_to_button[option]
                widget.configure(state="disabled")
        else:
            for flag in Pyinstaller.windows_flags:
                widget = self.pyinstaller_flag_to_button[flag]
                widget.configure(state="disabled")
            for option in Pyinstaller.windows_options:
                widget = self.pyinstaller_option_to_button[option]
                widget.configure(state="disabled")
            
    def pyinstaller_disable_all_flag_buttons(self):
        """ Disables all the buttons related to flags
        """
        for button in self.pyinstaller_flag_buttons:
            button.configure(state="disabled")
    
    def pyinstaller_disable_all_option_buttons(self):
        """ Disables all buttons relate to options
        """
        for button in self.pyinstaller_option_buttons:
            button.configure(state="disabled")
    
    def pyinstaller_enable_all_flag_buttons(self):
        """ Enables all buttons related to flags
        """
        for button in self.pyinstaller_flag_buttons:
            button.configure(state="normal")
    
    def pyinstaller_enable_all_option_buttons(self):
        """ Enables all buttons related to options
        """
        for button in self.pyinstaller_option_buttons:
            button.configure(state="normal")
    
    def pyinstaller_reset_command(self):
        """ Resets the command list incase lambda functions are accidently called or need to be reset
        """
        self.pyinstaller_command = [self.pyinstaller_current_installer, self.pyinstaller_path, self.icon_path_command, "--noconfirm",]
    
    #////////////////////////////////////////////////////////////////
    #   PYINSTALLER BROWSE EVENTS
    #////////////////////////////////////////////////////////////////
    def pyinstaller_browse_python_file(self):
        """ Called when the browse button for the python file is clicked
        """

        self.pyinstaller_path = ctk.filedialog.askopenfile()
        try:
            self.pyinstaller_path = self.pyinstaller_path.name
        except AttributeError:
            return
        if self.pyinstaller_path is not None:
            if not self.pyinstaller_path.endswith(".py"):
                self.pyinstaller_set_text_command_box(ErrorString.pyfile)
                self.description_box.delete("0.0", "end")
                self.description_box.insert("0.0", ErrorString.pyfile)
                self.pyinstaller_set_output_box(ErrorString.pyfile, "ERROR")
                self.pyinstaller_path = "<path>"
            if self.pyinstaller_path.endswith(".py"):
                self.pyinstaller_entry_python_script.delete(0, "end")
                self.pyinstaller_entry_python_script.insert(0, self.pyinstaller_path)
                self.pyinstaller_command[1] = self.pyinstaller_path
                self.pyinstaller_command[0] = self.pyinstaller_current_installer
                self.pyinstaller_command_to_box()
                self.pyinstaller_enable_all_flag_buttons()
                self.pyinstaller_enable_all_option_buttons()
                self.pyinstaller_disable_os_specific_flags()
                self.pyinstaller_compile_button.configure(state='normal')
                self.pyinstaller_compile_button.bind("<Button-1>", self.pyinstaller_compile_event)
                self.pyinstaller_selector_browse.grid_forget()
                self.pyinstaller_selector_compile.grid(row=4, column=3)
                self.pyinstaller_bind_option_buttons()
                self.pyinstaller_bind_flag_buttons()
    
    def pyinstaller_bind_option_buttons(self):
        self.pyinstaller_onedir_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--onedir", self.pyinstaller_onedir_button))
        self.pyinstaller_onefile_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--onefile", self.pyinstaller_onefile_button))
        self.pyinstaller_clean_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--clean", self.pyinstaller_clean_button))
        self.pyinstaller_strip_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--strip", self.pyinstaller_strip_button))
        self.pyinstaller_noupx_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--noupx", self.pyinstaller_noupx_button))
        self.pyinstaller_console_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--console", self.pyinstaller_console_button))
        self.pyinstaller_windowed_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--windowed", self.pyinstaller_windowed_button))
        self.disablewindowedtraceback_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--disable-windowed-traceback", self.disablewindowedtraceback_button))
        self.noembeddedmanifest_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--no-embedded-manifest", self.noembeddedmanifest_button))
        self.bootloaderignoresignals_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--bootloader-ignore-signals", self.bootloaderignoresignals_button))
        if sys.platform.startswith('w'):
            self.uacadmin_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--uac-admin", self.uacadmin_button))
            self.uacuiaccess_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--uac-uiaccess", self.uacuiaccess_button))
            self.winprivateassemblies_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--win-private-assemblies", self.winprivateassemblies_button))
            self.winnopreferredirects_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--win-no-prefer-redirects", self.winnopreferredirects_button))
        elif sys.platform.startswith('d'):
            self.argvemulation_button.bind("<Button-1>", lambda event: self.pyinstaller_add_flag("--argv-emulation", self.argvemulation_button))
    
    def pyinstaller_bind_flag_buttons(self):
        self.pyinstaller_name_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--name', self.pyinstaller_name_button))
        self.addbinary_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--add-binary', self.addbinary_button))
        self.pyinstaller_paths_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--paths', self.pyinstaller_paths_button))
        self.hiddenimport_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--hidden-import', self.hiddenimport_button))
        self.collectsubmodules_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--collect-submodules', self.collectsubmodules_button))
        self.collectdata_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--collect-data', self.collectdata_button))
        self.collectbinaries_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--collect-binaries', self.collectbinaries_button))
        self.collectall_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--collect-all', self.collectall_button))
        self.specpath_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--specpath', self.specpath_button))
        self.adddata_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--add-data', self.adddata_button))
        self.copymetadata_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--copy-metadata', self.copymetadata_button))
        self.recursivecopymetadata_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--recursive-copy-metadata', self.recursivecopymetadata_button))
        self.additionalhooksdir_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--additional-hooks-dir', self.additionalhooksdir_button))
        self.runtimehook_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--runtime-hook', self.runtimehook_button))
        self.excludemodule_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--exclude-module', self.excludemodule_button))
        self.splash_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--splash', self.splash_button))
        self.runtimetmpdir_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--runtime-tmpdir', self.splash_button))
        if sys.platform.startswith('d'):
            self.osxbundleidentifier_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--osx-bundle-identifier', self.splash_button))
            self.targetarchitecture_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--target-architecture', self.splash_button))
            self.codesignidentity_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--codesign-identity', self.splash_button))
            self.osxentitlementsfile_button.bind('<Button-1>', lambda oevent: self.pyinstaller_add_option('--osx-entitlements-file', self.splash_button))
        
    def pyinstaller_browse_icon_file(self):
        """ Called when the browse button is clicked for the icon file
        """
        path = ctk.filedialog.askopenfile().name
        if path is not None and path.endswith(".ico"):
            self.icon_path_command = f"--icon={path}"
            self.pyinstaller_entry_icon.delete(0)
            for index, char in enumerate(path):
                self.pyinstaller_entry_icon.insert(index, char)
            cmdset = False
            for index, option in enumerate(self.pyinstaller_command):
                if option.startswith('--icon='):
                    self.pyinstaller_command[index] = f"--icon={path}"
                    cmdset = not cmdset
                    break 
            if not cmdset:
                self.pyinstaller_command.append(f"--icon={path}")
        elif not path.endswith(".ico"):
            msg = "[ ! ] Sorry Icon has to be .ico file [ ! ]"
            self.pyinstaller_command_textbox.delete("0.0", "end")
            self.pyinstaller_set_text_command_box(msg)
            self.description_box.delete("0.0", "end")
            self.description_box.insert("0.0", msg)
            self.description_title.configure(text="Selection Error")
            self.type_title.configure(text="Only Ico files Allowed")
            self.status_title.configure(text="Status: Massive Failure")
    
    #////////////////////////////////////////////////////////////////
    #   PYINSTALLER BUTTON EVENTS
    #////////////////////////////////////////////////////////////////
    def pyinstaller_add_flag(self, *args):
        """ Called when a flag button is pressed
        """
        print(args)
        flag = args[0]
        incommand = False 
        for index, f in enumerate(self.pyinstaller_command):
            if f == flag:
                incommand = True
                self.pyinstaller_command.pop(index)
                args[1].configure(border_width=0)
                break
        if incommand == False:
            self.pyinstaller_command.append(flag)
            args[1].configure(border_width=1, border_color="yellow")
              
        self.pyinstaller_command_to_box()

    def pyinstaller_add_option(self, *args):
        """ called when an option button is clicked
        """
        print(args)
        option = args[0]
        incommand = False
        if args[1].cget('border_width') != 1:
            dialog = ctk.CTkInputDialog(text=f"Enter Value for {option}:", title="Key Value Enter")
            value = dialog.get_input()
            value = "$CANCEL$" if value == '' else value
        else:
            value = ""
        option_value = option + f"={value}"
        for index, f in enumerate(self.pyinstaller_command):
           if f.startswith(option):
                incommand = True
                self.pyinstaller_command.pop(index)
                args[1].configure(border_width=0, text=option)
                break
        if incommand == False:
            if value != "$CANCEL$":
                self.pyinstaller_command.append(option_value)
                args[1].configure(border_width=1, border_color="yellow", text=option_value)
        self.pyinstaller_command_to_box()
        
    def pyinstaller_command_to_box(self):
        """ creates the command string and sends it to the command box
        """
        cmdstr = " ".join(self.pyinstaller_command)    
        self.pyinstaller_set_text_command_box(cmdstr)
        
    def pyinstaller_set_text_command_box(self, text: str):
        """ sets the command box to <text>

        Args:
            text (str): New text to be displayed
        """
        self.pyinstaller_command_textbox.delete("0.0", "end")
        self.pyinstaller_command_textbox.insert("0.0", text)
        
    def pyinstaller_set_description_box(self, *args) -> None:
        """Sets the black description box when a button is highlighted
        """
        if self.hidden_info_box:
            return
        item = str(args[0])
        name = "Name:   " + item.replace("-", " ").strip(" ")
        tt = f"Type:   " + "Flag"
        status = "Status:  " + "Deactivated"
        val = "Value:   " +  "None"
        desc = Pyinstaller.flag_map[item]
        self.description_box.delete("0.0", "end")
        self.description_box.insert("0.0", desc)
        self.description_title.configure(text=name)
        self.type_title.configure(text=tt)
        for index, x in enumerate(self.pyinstaller_command):
            if x == item:
                status = "Status:  " + "Activated"
                val = "Value:   None"
                break
        self.status_title.configure(text=status)
        self.value_title.configure(text=val)
        
    def pyinstaller_set_description_box_option(self, *args) -> None:
        """Sets the description box when an option button is highlighted
        """
        if self.hidden_info_box:
            return
        item = str(args[0])
        name = "Name:   " + item.replace("-", " ").strip(" ")
        tt = f"Type:   " + "Option"
        status = "Status:  " + "Deactivated"
        val = f"Value:   None"
        desc = Pyinstaller.option_map[item]
        self.description_box.delete("0.0", "end")
        self.description_box.insert("0.0", desc)
        self.description_title.configure(text=name)
        self.type_title.configure(text=tt)
        for index, x in enumerate(self.pyinstaller_command):
            if x.startswith(item):
                val = x.split("=")[1]
                status = "Status:  " + f"Activated"
                val = f"Value:    {val}"
                break
        self.status_title.configure(text=status)
        self.value_title.configure(text=val)

    def pyinstaller_set_output_box(self, *args):
        """ Sets text into the output box
        """
        name = args[0]
        reference = args[1]
        msg = str(name)
        self.pyinstaller_output_textbox.new_text(text=msg, reference=reference)

    #////////////////////////////////////////////////////////////////
    #   TAB EVENTS
    #////////////////////////////////////////////////////////////////
    def tabview_event(self, *args):
        self.current_tab = self.tabview.get()
        if self.current_tab == 'Nuikta' and self.description_location != 'Nuikta':
            self.description_box.grid_forget()
            self.description_box.configure(master=self.nuikta_bottom_frame)
            self.description_location = self.current_tab
        else:
            if self.current_tab != self.description_location:
                self.description_box.grid_forget()
                self.description_box.configure(master=self.tab_frames[self.current_tab])
                self.description_location = self.current_tab
         
         
    #////////////////////////////////////////////////////////////////
    #   NUIKTA BROWSE EVENTS
    #////////////////////////////////////////////////////////////////
    def browse_filepath_nuikta(self, *args):
        try:
            self.nuikta_path = str(ctk.filedialog.askopenfile().name)
        except AttributeError:
            return
        print(self.nuikta_path)
        if self.nuikta_path.endswith(".py") == False:
            self.nuikta_set_text_command_box("[ ! ]         Please Only Use Python '.py' files          [ ! ]")
            self.description_box.delete("0.0", "end")
            self.description_box.insert("0.0", "[ ! ]         Please Only Use Python '.py' files          [ ! ]")
            self.nuikta_path = "<path>"
        elif self.nuikta_path.endswith(".py"):
            self.nuikta_bottom_frame.grid(row=1, column=0, pady=(5,5), padx=(5,5), sticky='NWE')
            self.nuikta_option_frame.grid(row=4, column=0, sticky="NW", columnspan=3, padx=(1,1), pady=(1,1))
            self.nuikta_flag_button_frame.grid(row=0, column=0, sticky="WE", columnspan=8, padx=(1,1), pady=(1,1), ipadx=1, ipady=1)
            self.nuikta_filepath_entry.delete(0, "end")
            self.nuikta_filepath_entry.insert(0, self.nuikta_path)
            self.nuikta_command[1] = self.nuikta_path
            self.nuikta_command[0] = "nuikta"
            self.nuikta_command_to_box()
            self.nuikta_compile_button.bind("<Button-1>", self.nuikta_compile_event)
            self.nuikta_compile_button.configure(state='normal')
            self.nuikta_selector_browse.grid_forget()
            self.nuikta_selector_flags.grid(row=4, column=1, sticky='NW')
            
    def nuikta_browse_icon_file(self):
        """ Called when the browse button is clicked for the icon file
        """
        path = ctk.filedialog.askopenfile().name
        if path is not None and path.endswith(".ico"):
            self.icon_path_command = f"--icon={path}"
            self.nuikta_entry_icon.delete(0)
            for index, char in enumerate(path):
                self.nuikta_entry_icon.insert(index, char)
            cmdset = False
            for index, option in enumerate(self.nuikta_command):
                if option.startswith('--icon='):
                    self.nuikta_command[index] = f"--icon={path}"
                    cmdset = not cmdset
                    break 
            if not cmdset:
                self.nuikta_command.append(f"--icon={path}")
        elif not path.endswith(".ico"):
            msg = "[ ! ] Sorry Icon has to be .ico file [ ! ]"
            self.nuikta_command_textbox.delete("0.0", "end")
            self.nuikta_set_text_command_box(msg)
            self.description_box.delete("0.0", "end")
            self.description_box.insert("0.0", msg)
            self.description_title.configure(text="Selection Error")
            self.type_title.configure(text="Only Ico files Allowed")
            self.status_title.configure(text="Status: Massive Failure")
    
    #////////////////////////////////////////////////////////////////
    #   NUIKTA FLAG DISABLE/ENABLE EVENTS
    #////////////////////////////////////////////////////////////////
    def nuikta_disable_os_specific_flags(self):
        """ Disables flags that can not be used on your operating system
        """
        if self.platform.startswith("w"):
            for flag in Nuikta.mac_flags:
                widget = self.nuikta_flag_to_button[flag]
                widget.configure(state="disabled")
            for option in Nuikta.mac_options:
                widget = self.nuikta_option_to_button[option]
                widget.configure(state="disabled")
        else:
            for flag in Nuikta.windows_flags:
                widget = self.nuikta_flag_to_button[flag]
                widget.configure(state="disabled")
            for option in Nuikta.windows_options:
                widget = self.nuikta_option_to_button[option]
                widget.configure(state="disabled")
            
    def nuikta_reset_command(self):
        """ Resets the command list incase lambda functions are accidently called or need to be reset
        """
        self.nuikta_command = ["nuikta", self.nuikta_path, self.icon_path_command, "--noconfirm"]
  
    #////////////////////////////////////////////////////////////////
    #   NUIKTA BUTTON EVENTS
    #////////////////////////////////////////////////////////////////
    def nuikta_add_flag(self, *args):
        """ Called when a flag button is pressed
        """
        print(args)
        flag = args[0]
        incommand = False 
        for index, f in enumerate(self.nuikta_command):
            if f == flag:
                incommand = True
                self.nuikta_command.pop(index)
                args[1].configure(border_width=0)
                break
        if incommand == False:
            self.nuikta_command.append(flag)
            args[1].configure(border_width=1, border_color="yellow")
              
        self.nuikta_command_to_box()

    def nuikta_add_option(self, *args):
        """ called when an option button is clicked
        """
        print(args)
        option = args[0]
        incommand = False
        if args[1].cget('border_width') != 1:
            dialog = ctk.CTkInputDialog(text=f"Enter Value for {option}:", title="Key Value Enter")
            value = dialog.get_input()
            value = "$CANCEL$" if value == '' else value
        else:
            value = ""
        option_value = option + f"={value}"
        for index, f in enumerate(self.nuikta_command):
           if f.startswith(option):
                incommand = True
                self.nuikta_command.pop(index)
                args[1].configure(border_width=0, text=option)
                break
        if incommand == False:
            if value != "$CANCEL$":
                self.nuikta_command.append(option_value)
                args[1].configure(border_width=1, border_color="yellow", text=option_value)
        self.nuikta_command_to_box()
        
    def nuikta_command_to_box(self):
        """ creates the command string and sends it to the command box
        """
        cmdstr = " ".join(self.nuikta_command)    
        self.nuikta_set_text_command_box(cmdstr)
        
    def nuikta_set_text_command_box(self, text: str):
        """ sets the command box to <text>

        Args:
            text (str): New text to be displayed
        """
        self.nuikta_command_textbox.delete("0.0", "end")
        self.nuikta_command_textbox.insert("0.0", text)
        
    def nuikta_set_description_box(self, *args) -> None:
        """Sets the black description box when a button is highlighted
        """
        if self.hidden_info_box:
            return
        item = str(args[0])
        name = "Name:   " + item.replace("-", " ").strip(" ")
        tt = f"Type:   " + "Flag"
        status = "Status:  " + "Deactivated"
        val = "Value:   " +  "None"
        desc = Pyinstaller.flag_map[item]
        self.description_box.delete("0.0", "end")
        self.description_box.insert("0.0", desc)
        self.description_title.configure(text=name)
        self.type_title.configure(text=tt)
        for index, x in enumerate(self.nuikta_command):
            if x == item:
                status = "Status:  " + "Activated"
                val = "Value:   None"
                break
        self.status_title.configure(text=status)
        self.value_title.configure(text=val)
        
    def nuikta_set_description_box_option(self, *args) -> None:
        """Sets the description box when an option button is highlighted
        """
        if self.hidden_info_box:
            return
        item = str(args[0])
        name = "Name:   " + item.replace("-", " ").strip(" ")
        tt = f"Type:   " + "Option"
        status = "Status:  " + "Deactivated"
        val = f"Value:   None"
        desc = Nuikta.action_map[item]
        self.description_box.delete("0.0", "end")
        self.description_box.insert("0.0", desc)
        self.description_title.configure(text=name)
        self.type_title.configure(text=tt)
        for index, x in enumerate(self.nuikta_command):
            if x.startswith(item):
                val = x.split("=")[1]
                status = "Status:  " + f"Activated"
                val = f"Value:    {val}"
                break
        self.status_title.configure(text=status)
        self.value_title.configure(text=val)
    
    def nuikta_set_output_box(self, *args):
        """ Sets text into the output box
        """
        name = args[0]
        reference = args[1]
        msg = str(name)
        self.nuikta_output_textbox.new_text(text=msg, reference=reference) 
  
    #////////////////////////////////////////////////////////////////
    #   NUIKTA COMPILE EVENTS
    #////////////////////////////////////////////////////////////////
    def nuikta_compile_event(self):
        pass
    
    
if __name__ == '__main__':
    cg = CompilerGui()
    
