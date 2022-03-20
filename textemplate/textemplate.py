# SPDX-FileCopyrightText: 2022 Daniel Laidig <daniel@laidig.info>
#
# SPDX-License-Identifier: MIT
import os
import json
import sys

import yaml
import argparse
import jinja2
import copy
import latex
import latex.jinja2

from .filters import shuffled, shuffledAnswerLetters, precision, nodotzero, green2red, debug


def createEnv(path_or_loader=None, **kwargs):
    """
    Creates a jinja2 loader setup for LaTeX, mostly based on the latex package but with some additional filters.

    Basic usage:
    template = env.get_template(templateFilename)  # or
    template = env.from_string(templateString)
    template.render(**data)  # or use renderTemplate

    :param path_or_loader: a directory path to load templates from (as string), a jinja loader or None (default) to only
    support loading templates from string
    :return: a jinja2 Environment
    """
    if isinstance(path_or_loader, str):
        path_or_loader = jinja2.FileSystemLoader(path_or_loader)

    env = latex.jinja2.make_env(loader=path_or_loader, **kwargs)
    env.filters['precision'] = precision
    env.filters['nodotzero'] = nodotzero
    env.filters['shuffled'] = shuffled
    env.filters['shuffledAnswerLetters'] = shuffledAnswerLetters
    env.filters['green2red'] = green2red
    env.globals['debug'] = debug
    return env


def renderTemplate(template, data, outputFilename=None, inputDir=None, tex=True, pdf=True, output=True):
    """
    Renders the given template with the given data and optionally writes .tex and .pdf files.
    :param template: the jinja2 template obtained via env.get_template or env.from_string
    :param data: dictionary containing the data to pass to the template
    :param outputFilename: filename of the tex or pdf file to write to (optional, has to end with .tex or .pdf)
    :param inputDir: directory in which LaTeX looks for inputs/figures (obtained from outputFilename if None)
    :param tex: write a tex file with the rendered template
    :param pdf: write a pdf file with the compiled template
    :param output: print output about written files
    :return: rendered LaTeX code
    """

    if outputFilename is not None:
        outBasename, ext = os.path.splitext(outputFilename)
        assert ext in ('.pdf', '.tex'), 'outputFilename must end with .pdf or .tex'
        texFilename = outBasename + '.tex'
        pdfFilename = outBasename + '.pdf'
        if inputDir is None:
            inputDir = os.path.dirname(os.path.abspath(outputFilename))
    else:
        texFilename = None
        pdfFilename = None

    texData = template.render(**data)
    if tex:
        assert texFilename is not None
        with open(texFilename, 'w') as f:
            f.write(texData)
        if output:
            print('tex code written to', texFilename)

    if pdf:
        assert pdfFilename is not None
        assert inputDir is not None
        pdfData = latex.build_pdf(texData, texinputs=[os.path.abspath(inputDir), ''])
        pdfData.save_to(pdfFilename)
        print('pdf written to', pdfFilename)

    return texData


def run(templateFilename, dataFilenames, outputFilename, enableMultiOutput, verbose, createPdf):
    data = {}
    for dataFilename in dataFilenames:
        if '::' in dataFilename:
            prefix, dataFilename = dataFilename.split('::', maxsplit=1)
        else:
            prefix = None
        with open(dataFilename, 'r') as f:
            if dataFilename.endswith('.yaml') or dataFilename.endswith('.yml'):
                fileData = yaml.safe_load(f)
            else:
                fileData = json.load(f)
        if prefix is None:
            data.update(fileData)
        else:
            data[prefix] = fileData

    if isinstance(data, list):
        data = dict(data=data)

    if verbose:
        print('data:')
        import pprint
        pprint.pprint(data)

    env = createEnv('.')
    template = env.get_template(templateFilename)

    if enableMultiOutput and 'outputFiles' not in data:
        print('error: --multi-output was passed, but the data does not contain an outputFiles entry.', file=sys.stderr)
        exit(1)

    if 'outputFiles' in data and not enableMultiOutput:
        print('warning: data contains outputFiles entry but the --multi-output option was not was passed.',
              file=sys.stderr)

    outputBasename = os.path.splitext(dataFilenames[-1] if outputFilename is None else outputFilename)[0]
    if not enableMultiOutput and outputBasename + '.tex' == templateFilename:
        print('error: the template would be overwritten by the output. please rename the template file.',
              file=sys.stderr)
        exit(1)

    if enableMultiOutput:
        for fileData in data['outputFiles']:
            mergedData = copy.copy(data)
            mergedData.update(fileData)
            assert 'filename' in fileData, 'each entry in fileData must have a "filename" field'
            outputFilename = '{}_{}.tex'.format(outputBasename, fileData['filename'])
            renderTemplate(template, mergedData, outputFilename, pdf=createPdf)
    else:
        renderTemplate(template, data, '{}.tex'.format(outputBasename), pdf=createPdf)


def main():
    parser = argparse.ArgumentParser(description='LaTeX template renderer.')
    parser.add_argument('-p', '--pdf', action='store_true', help='create PDFs')
    parser.add_argument('-v', '--verbose', help='enable verbose mode (print parsed data)', action='store_true')
    parser.add_argument('--multi-output', action='store_true', help='generate multiple output files based on the '
                                                                    'outputFiles entry in the data')
    parser.add_argument('-o', '--out', help='output filename (default: derived from the last data filename)')
    parser.add_argument('template', help='name of the .tex template file')
    parser.add_argument('data', nargs='+', help='name of the .yaml/.json data files (use "variable::filename" to make '
                                                'the file data available in a specific variable)')
    args = parser.parse_args()
    run(args.template, args.data, args.out, args.multi_output, args.verbose, args.pdf)


if __name__ == '__main__':
    main()
