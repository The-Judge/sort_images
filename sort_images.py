#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyexifinfo
import os
import sys
import argparse
import shutil
import magic
import daiquiri, logging

class myparser(argparse.ArgumentParser):
    """
    Define a sub class for argparse.ArgumentParser, which print_help() in error.
    """
    def error(self, message):
        args = {'prog': self.prog, 'message': message}
        print('%(prog)s: error: %(message)s\n' % args)
        self.print_help()
        sys.exit(1)

def parseArgs():
    parser = myparser(description='This script searches for image files in a secified source folder and moves those '
                                  'found to a defined destination folder. Inside that destination folder, it '
                                  'automatically generates subfolders for the year (and optionally the month) the '
                                  'found picture was taken.')
    parser.add_argument('-n', '--dry-run', action='store_true',
                        help='Do not take any actions for real, just print what would be done. This ensures no data is '
                             'changed or directories created. Even logging is disabled.')
    parser.add_argument('-l', '--logfile', metavar='/path/to/logfile',
                        help='Specify the filename to which to write the log to\n (Default: /tmp/sort_images.log)',
                        default='/tmp/sort_images.log')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Be verbose during execution.')
    parser.add_argument('-m', '--monthly', action='store_true',
                        help='If set, files are not only moved to a subfolder, representing their year of creation, '
                             'but to another subfolder, representing the month (like "2017/02/" instead of just '
                             '"2017/".')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-d', '--destination', metavar='/path/to/destination',
                        help='Specify the base destination directory where the time based subdirectories should be '
                             'created in.', required=True)
    requiredNamed.add_argument('-s', '--source', metavar='/path/to/unsorted-files',
                        help='Specify the directory, where the to-be-sorted files are in (files are searched '
                             'recursively).',
                        required=True)
    return parser.parse_args()

def setupLogging(logfile, dryrun=False, verbose=False):
    """
    This generates a daiquiri logging object.
    :param logfile: a str object, naming the destination of a logfile
    :param dryrun: bool which switches dryrun on or off
    :param verbose: bool which switches verbosity on or off
    :return:
    """
    stream_level = logging.DEBUG
    if dryrun:
        daiquiri.setup(level=logging.DEBUG, outputs=(
            daiquiri.output.Stream(level=stream_level, stream=sys.stdout),
        ))
    else:
        if not verbose:
            stream_level = logging.WARN
        daiquiri.setup(level=logging.DEBUG, outputs=(
            daiquiri.output.File(level=logging.DEBUG,
                                 directory='{}'.format(os.path.dirname(logfile)),
                                 filename='{}'.format(os.path.basename(logfile))),
            daiquiri.output.Stream(level=stream_level)
        ))
    return daiquiri.getLogger()

def get_image_files(path, formats=('gif', 'jp2', 'jpeg', 'pcx', 'png', 'tiff', 'x-ms-bmp', 'x-portable-pixmap',
                                   'x-xbitmap')):
    """
    Check path recursively for files. If any compatible file is found, it is yielded with it's full path.
    :param formats: An iterable listing all mime formats (skipping the class part like 'images/') to include
    :param path:
    :return: yield absolute path
    """
    def is_image(file_name):
        # List mime types fully supported by Pillow
        try:
            if magic.from_file(file_name, mime=True).rsplit('/', 1)[1] in formats:
                return True
            else:
                return False
        except IndexError:
            return False

    path = os.path.abspath(path)
    if os.path.isfile(path):
        yield path
    else:
        for root, files in os.walk(path)[0:3:2]:
            for file in files:
                if is_image(os.path.join(root, file)):
                    yield os.path.join(root, file)

def main():
    args = parseArgs()
    logger = setupLogging(logfile=os.path.abspath(os.path.expanduser(args.logfile)), dryrun=args.dry_run,
                          verbose=args.verbose)
    srcdir = str(os.path.abspath(os.path.expanduser(args.source))).strip()
    dstdir = str(os.path.abspath(os.path.expanduser(args.destination))).strip()

    # Get a list of files
    logger.debug('Starting search for supported files in {}'.format(srcdir))
    source_files = get_image_files(srcdir, ('gif', 'jp2', 'jpeg', 'pcx', 'png', 'tiff', 'x-ms-bmp', 'x-portable-pixmap',
                                            'x-xbitmap', 'x-canon-cr2', 'mp4', 'x-msvideo', 'quicktime'))
    for source_file in source_files:
        # List of metadata field names, sorted by preference
        meta_preference_list = [ 'EXIF:CreateDate', 'PNG:exifDateTime', 'QuickTime:CreateDate', 'XMP:DateCreated',
                                 'File:FileModifyDate' ]
        source_file_meta = pyexifinfo.information(source_file)
        fieldname = None
        for fieldname in meta_preference_list:
            if fieldname in source_file_meta.keys():
                # At least 'File:FileModifyDate' will always be found, so: no fallback here
                break

        logger.debug('Trying to extract EXIF data from {}'.format(source_file))
        try:
            source_date = source_file_meta.get(fieldname)
        except KeyError:
            # No Exif data found
            logger.info('Could not extract EXIF data. Will not process file {}'.format(source_file))
            continue
        if isinstance(source_date, bytes):
            source_date = source_date.decode('utf-8')
        logger.debug('Found creation time: {} (in {})'.format(source_date, fieldname))

        # Determining destination dir and file
        destination_base = '{}/{}'.format(dstdir, source_date.split(':', 1)[0])
        if args.monthly:
            destination_base = '{}/{}'.format(destination_base, source_date.split(':', 2)[1])
        # Skip file if source_file already is beneath destination_file (like: "2017/Birthday/file.jpg")
        if destination_base in source_file:
            logger.info("Skipping file {} since it already is beneath it's destination".format(source_file))
            continue
        # Remove args.source from source_file to respect subfolders in the destination
        #   eg.: "/my/shiny/src/vacation/pic.jpg" becomes moved to "/whatever/dest/YYYY/vacation/pic.jpg" instead of
        #        "/whatever/dest/YYYY/pic.jpg" when args.source was "/my/shiny/src"
        sub_part = str(source_file).replace(srcdir, '', 1)
        if len(sub_part) == 0:
            sub_part = os.path.basename(source_file)
        destination_file = os.path.normpath('{}/{}'.format(destination_base, sub_part))
        destination_dir = os.path.dirname(destination_file)
        logger.info('Using {} as destination for file {}'.format(destination_dir, source_file))

        # Create destination folder if not exist
        if not os.path.isdir(destination_dir):
            if args.dry_run:
                logger.info('DRY-RUN: Would now create directory {}'.format(destination_dir))
            else:
                logger.info('Destination directory {} does not exist yet; will create it'.format(destination_dir))
                os.makedirs(destination_dir)
        else:
            logger.debug('Destination directory {} does already exist'.format(destination_dir))

        # Move file to destination
        if os.path.isfile(destination_file):
            logger.warn("WARN: Destination {} already exists; won't move source file {}.".format(destination_file,
                                                                                                 source_file))
            continue
        if args.dry_run:
            logger.info('DRY-RUN: Would now move {} to {}'.format(source_file, destination_file))
        else:
            logger.info('Moving {} to {}'.format(source_file, destination_file))
            shutil.move(source_file, destination_file)

if __name__ == "__main__":
    main()
