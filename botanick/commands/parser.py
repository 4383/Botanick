# -*- coding: UTF-8 -*-

import argparse
import os
from const import BASE_PATH
from const import VERSION
from commands.subcommands.webservice import webservice

def version():
  print(VERSION)

class Parser():
    """
    Command line parser
    """
    __args = None
    __instance = None
    __command = None
    __binding = {'webservice': webservice, 'version': version}
    __parser = None
    __subparser = None
    __args = None
    
    def __new__(cls):
        """
        Singleton
        """
        if Parser.__instance is None:
            Parser.__instance = object.__new__(cls)
        return Parser.__instance
    
    def __init__(self):
        """
        Initialize command parser and subcommands
        """
        self.__parser = argparse.ArgumentParser(description="Python command line utilities {0}".format(VERSION))
        self.__subparser = self.__parser.add_subparsers(description='valid subcommands', help='the sub-command to use')
        self.__webservice()
        self.__version()
        self.__args = vars(self.__parser.parse_args())
        try:
            self.__command = self.__args['which']
        except KeyError:
            self.__parser.print_help()
            exit(1)
            
    def __webservice(self):
        """
        Launch webservice subcommand from command line application
        """
        webservice = self.__subparser.add_parser('webservice',
                description='Launch webservice subcommand from command line application')
        webservice.set_defaults(which='webservice')
        
    def __version(self):
        """
        Display current version
        """
        version = self.__subparser.add_parser('version', description='Display current version')
        version.set_defaults(which='version')
    
    def getCommand(self):
        """
        Return the selected sub-command
        """
        try:
            return self.__binding[self.__command]
        except KeyError:
            print('Unrecognized command !')
            self.__parser.print_help()
            exit(1)
            
    def getArgs(self):
        """
        Return the args of the selected sub-command
        """
        return {key: value for key, value in self.__args.items() if key != 'which'}
        
