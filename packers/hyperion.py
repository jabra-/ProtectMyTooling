#!/usr/bin/python3
# -*- coding: utf-8 -*-

from IPacker import IPacker
from lib.utils import *

class PackerHyperion(IPacker):
    default_hyperion_args = '-s 4 -k 6' # gives: 5^6 ~ 262k brute-forces to undertake during launch
    hyperion_cmdline_template = '<command> <options> <infile> <outfile>'

    def __init__(self, logger, options):
        self.hyperion_args = PackerHyperion.default_hyperion_args
        self.logger = logger
        self.options = options

    @staticmethod
    def get_name():
        return 'Hyperion'

    @staticmethod
    def get_desc():
        return 'Robust PE EXE runtime AES encrypter for x86/x64 with own-key brute-forcing logic.'

    def help(self, parser):
        if parser != None:
            parser.add_argument('--hyperion-path', metavar='PATH', dest='hyperion_path',
                help = '(required) Path to hyperion binary capable of compressing x86/x64 executables.')

            parser.add_argument('--hyperion-args', metavar='ARGS', dest='hyperion_args',
                help = 'Optional hyperion-specific arguments to pass during compression.')

        else:
            if not self.options['config']:
                self.logger.fatal('Config file not specified!')

            self.options['hyperion_path'] = configPath(self.options['config'], self.options['hyperion_path'])

            if not os.path.isfile(self.options['hyperion_path']):
                self.logger.fatal('--hyperion-path option must be specified!')

            if 'hyperion_args' in self.options.keys() and self.options['hyperion_args'] != None \
                and len(self.options['hyperion_args']) > 0: 
                self.hyperion_args += ' ' + self.options['hyperion_args']


    def process(self, arch, infile, outfile):
        ver = shell(self.logger, self.options['hyperion_path'] + ' --version')
        ver = ' '.join(ver.split('\r\n')[0:2]).strip().replace('Version ', '')

        self.logger.info(f'Working with {ver}')

        try:
            cwd = os.getcwd()
            base = os.path.dirname(self.options['hyperion_path'])

            self.logger.dbg('changed working directory to "{}"'.format(base))
            os.chdir(base)

            out = shell(self.logger, IPacker.build_cmdline(
                PackerHyperion.hyperion_cmdline_template,
                os.path.basename(self.options['hyperion_path']),
                self.hyperion_args,
                infile,
                outfile
            ))

        except Exception as e:
            raise

        finally:
            self.logger.dbg('reverted to original working directory "{}"'.format(cwd))
            os.chdir(cwd)

        return os.path.isfile(outfile)