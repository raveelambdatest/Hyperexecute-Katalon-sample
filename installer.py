"""
This module writes various values to various registers. Read
certificates from remote server or from the laptop/desktop,
certificate files are zipped and contents of the zip file 
extracted to current working directory.Adds various certificates
to ROOT store and also pfx files to NOROOT store.
"""

import ctypes
import sys
import glob
import subprocess
import requests
from winreg import *
from zipfile import ZipFile
from os import path, getcwd, remove


def regWrite(registry, keyValue, valueName, type, value):
    """
    In this function we attempt to open the key,  If the open 
    fails, it’s usually because the key doesn’t exist, so we 
    try to create the key in our exception handler. Then we 
    use SetValueEx to actually set the value and clean up when 
    we’re done and close the key. 
    Args:   
        registry : Windows Registry name.
        keyValue : Key this method opens or creates
        valueName: Names the subkey with which the value is 
                   associated
        type     : Type of key to write
        value    : The value to write
    Returns:
       None
    """
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    key = None
    try:
        key = OpenKey(registry, keyValue, 0, access = KEY_WRITE | KEY_WOW64_32KEY)
    except Exception as Error:
        key = CreateKey(registry, keyValue)
    SetValueEx(key, valueName, 0, type, value)
    for i in range(1024):                                           
        try:
            n,v,t = EnumValue(key, i)
            print ("i=",i, " n=",n, " v=",v, " t=",t)
        except Exception as Error:                                               
            print ("You have",i," tasks starting at logon...")
            break  
    CloseKey(key)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


def writeToRegistery():
    """
    This function writes various registry values to registry keys, 
    like HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE for Internet settings,
    policies and chrome.
    Args:
        None
    Returns:
        None
    """
    regWrite(HKEY_CURRENT_USER, 
             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Domains", 
             "pwcinternal.com", 
             REG_SZ, 
             "")
    regWrite(HKEY_CURRENT_USER, 
             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Domains\pwcinternal.com", 
             "*", 
             REG_DWORD, 
             2)
    regWrite(HKEY_CURRENT_USER, 
             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Domains", 
             "pwc.com", 
             REG_SZ, 
             "")
    regWrite(HKEY_CURRENT_USER, 
             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Domains\pwc.com", 
             "*", 
             REG_DWORD, 
             2)

    regWrite(HKEY_LOCAL_MACHINE, 
             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Domains", 
             "pwcinternal.com", 
             REG_SZ, 
             "")
    regWrite(HKEY_LOCAL_MACHINE, 
             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Domains\pwcinternal.com", 
             "*", 
             REG_DWORD, 
             2)
    regWrite(HKEY_LOCAL_MACHINE, 
             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Domains", 
             "pwc.com", 
             REG_SZ, 
             "")
    regWrite(HKEY_LOCAL_MACHINE, 
             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Domains\pwc.com", 
             "*", 
             REG_DWORD, 
             2)

    regWrite(HKEY_LOCAL_MACHINE, 
             r"SOFTWARE\Policies\Microsoft\Cryptography", 
             "ForceKeyProtection", 
             REG_DWORD, 
             2)

    regWrite(HKEY_LOCAL_MACHINE, 
             r"SOFTWARE\Policies\Google\Chrome\AutoSelectCertificateForUrls", 
             "1", 
             REG_SZ, 
             '{"pattern":"https://login-stg.pwcinternal.com","filter":{"ISSUER":{"CN":"PwC Test Issuing-1"}}}')


def disable64FsRedirection():
    """
    This function is useful for 32-bit applications that want to 
    gain access to the native system32 directory. By default, 
    WOW64 file system redirection is enabled.
    Args:
        None
    Returns:
        None
    """
    k32 = ctypes.windll.kernel32
    wow64 = ctypes.c_long()
    k32.Wow64DisableWow64FsRedirection(ctypes.byref(wow64))


def getCertificates():
    """
    Incase of remote server HTTP requests using Windows HTTP native
    API are sent to remote server, read all the certificates, write
    it to a zip file and then un zip all the files to current working
    directory else read certificates zip file from laptop/desktop 
    and then un zip all the files to current working directory.Based 
    on URL environment variable we will decide whether it is an url 
    to remote webserver or just path of zip files on laptop/desktop.
    Args:
        None
    Returns:
        None
    """

    pass  # secret code


def loadCertificates():
    """
    This function adds certificates to ROOT store.
    Args:
        None
    Returns:
        None
    """
    #Load certificate files
    #executeCommand("PwC Policy-1.cer")
    executeCommand("Test.pfx")
    #executeCommand("PwC Test Issuing-1_2022.cer")
    #executeCommand("PwC SSL Issuing - 1_2022.cer")
    #executeCommand("PwC Root-3_2044.crt")


def getCurrentDir() -> str:
    from os import path
    return path.dirname(__file__)


def getPath(file: str):
    from os import path
    return path.join(getCurrentDir(), file)


def executeCommand(certFile):
    """
    This function spanws subprocess for loading given certificate
    as ROOT user
    Args:
        None
    Returns:
        None
    """
    print(getPath(certFile))
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    cmd = "certutil -f -p abc123 -importpfx Test.pfx"
    print(cmd)
    proc = subprocess.Popen(cmd, shell=True)
    proc.communicate()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


def loadPfxFile(certFile: str, password: str):
    """
    This function spanws subprocess for loading PFX file with
    the given password
    Args:
        None
    Returns:
        None
    """
    #Load the PFX file
    print(getPath(certFile))
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    password = password or '{{PASSWORD}}'
    cmd = f'c:\\windows\\system32\\certutil.exe -user -f ' \
          f'-p abc123 -importpfx Test.pfx NOROOT'
    print(cmd)
    proc = subprocess.Popen(cmd, shell=True)
    proc.communicate()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


def cleanUp():
    """
    This function will cleanup the zip and certificate files
    Args:
        None
    Returns:
        None
    """
    print("Cleanup: Deleting certificate zip and extracted certificate files")
    try:
        for filename in glob.glob('P*.cer'):
            remove(filename)
        for filename in glob.glob('*.crt'):
            remove(filename)
        for filename in glob.glob('*.zip'):
            remove(filename)
        for filename in glob.glob('*.pfx'):
            remove(filename)
    except Exception as Error:
        print("Exception occurred in cleanUp :", Error)
        sys.exit()


def get_pfx_files() -> list:
    return [path.basename(file)
            for file in glob.glob(getPath('*.pfx'))]


if __name__ == '__main__':

    # creating the argument parser instance
    from argparse import ArgumentParser, SUPPRESS, OPTIONAL
    parser = ArgumentParser()

    # declaring all arguments
    parser.add_argument(
        '--list', '-l', required=False, action='store_true',
        help='Display all certificates zipped in the file and available to unpack')
    # parser.add_argument(
    #     '--auto-upload', '-a', '--get-certificates',
    #     type=bool, const=True, default=False,
    #     nargs='?', required=False)
    parser.add_argument(
        '--no-registry', '-R', required=False, action='store_false',
        help='Avoid registry updates. Certificate will not be applied automatically')
    parser.add_argument(
        '--no-fs-redirection', '-D', required=False, action='store_false',
        help='Disables automatic redirection of 32-bit processes. '
             'Use this option when you’re using a 32-bit process')
    parser.add_argument(
        '--cert', '-c', type=str, nargs='+', required=False,
        help='The list of certificates to install. Each of these certificates '
             'should be already packed to the installer')
    parser.add_argument(
        '--password', '-p', type=str, nargs=1, required=False,
        help='The password for the certificate[s] installation')

    # getting all passed arguments
    arguments = parser.parse_args()

    # printing the available certs
    if arguments.list:
        print('Available certificates:')
        for cert_file in get_pfx_files():
            print(' - ' + cert_file)

    # installing all certificates
    if arguments.cert or not arguments.list:

        # updating the registry
        if not arguments.no_registry:
            writeToRegistery()

        # upload all certificates from the pwc servers
        # if arguments.auto_upload:
        #     getCertificates()

        # disabling fs redirection
        if arguments.no_fs_redirection:
            disable64FsRedirection()

        # loading root certificates
        loadCertificates()

        # loading/installing pfx certificate files
        for certificate in arguments.cert or get_pfx_files():
            loadPfxFile(certificate, arguments.password)

    # cleaning after the execution
    cleanUp()