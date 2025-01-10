import os


def create_nsis_installer_file(build_folder_path, build_version):
    """Create NSIS installer file for windows"""

    build_version = build_version.replace('.', '')
    build_folder_path = os.path.join(build_folder_path)
    file_object_install = open(os.path.join(build_folder_path, 'install.nsi'), 'w+')

    # Use unicode
    file_object_install.write('Unicode True\n')

    # define installer header name
    file_object_install.write('Name "DeepISLES"\n')

    # define installer exe name
    # file_object_install.write('CompanyName "Medical Image Analysis Group ARTORG Unibe"\n')
    file_object_install.write(f'OutFile "DeepISLES_100_64bit.exe"\n')

    # set install directory
    file_object_install.write('InstallDir "$PROGRAMFILES64\DeepISLES"\n')

    # set icon path
    file_object_install.write(fr'Icon "{build_folder_path}\bin\deepISLES.ico"')

    # default section start
    file_object_install.write('\nSection\n')

    # For all users
    file_object_install.write('SetShellVarContext all\n')

    # clean data from previous installation
    file_object_install.write('RMDir /r $INSTDIR\n')

    # set user data directory
    file_object_install.write('SetOutPath "$LocalAppdata\DeepISLES"\n')

    # Set path to write files
    file_object_install.write('SetOutPath $INSTDIR\n')

    # Copy first the icon file
    file_object_install.write(r'File bin\deepISLES.ico')
    file_object_install.write('\n')

    # All files
    file_object_install.write(f'File /r "{build_folder_path}\*.*"\n')

    # create shortcuts, desktop and startmenu
    file_object_install.write(r'CreateShortCut "$DESKTOP\DeepISLES.lnk" "$INSTDIR\bin\DeepISLES.exe" "" "$INSTDIR\deepISLES.ico"')
    file_object_install.write('\n')
    file_object_install.write(r'CreateShortcut "$SMPROGRAMS\DeepISLES.lnk" "$INSTDIR\bin\DeepISLES.exe" "" "$INSTDIR\deepISLES.ico"')
    file_object_install.write('\n')

    # define and create uninstaller
    file_object_install.writelines(r'WriteUninstaller $INSTDIR\uninstaller.exe')
    file_object_install.write('\n')

    # create shortcut startmenu
    file_object_install.write(r'CreateShortcut "$SMPROGRAMS\DeepISLES Uninstaller.lnk" "$INSTDIR\uninstaller.exe" "" "$INSTDIR\deepISLES.ico"')
    file_object_install.write('\n')

    # default section end
    file_object_install.write('SectionEnd\n')

    # create a section to define what the uninstaller does.
    # the section will always be named "Uninstall"
    file_object_install.write('Section "Uninstall"\n')

    # For all users
    file_object_install.write('SetShellVarContext all\n')

    # Always delete uninstaller first
    file_object_install.write(r'Delete $INSTDIR\uninstaller.exe')
    file_object_install.write('\n')

    # delete all files recursively
    file_object_install.write('RMDir /r $INSTDIR\n')
    file_object_install.write('RMDir /r "$LocalAppdata\DeepISLES"\n')

    # if not possible to delete, the files will be deleted during reboot
    file_object_install.write('RMDir /r /REBOOTOK $INSTDIR\n')
    file_object_install.write('RMDir /r /REBOOTOK "$LocalAppdata\DeepISLES"\n')

    # delete shortcuts, desktop and start menu
    file_object_install.write('Delete "$SMPROGRAMS\DeepISLES.lnk"\n')
    file_object_install.write('Delete "$DESKTOP\DeepISLES.lnk"\n')
    file_object_install.write('Delete "$SMPROGRAMS\DeepISLES Uninstaller.lnk"\n')

    # Delete the directory
    file_object_install.write('RMDir $INSTDIR\n')
    file_object_install.write('RMDir "$LocalAppdata\DeepISLES"\n')
    file_object_install.write('SectionEnd\n')
