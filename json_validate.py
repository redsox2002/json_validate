#!/usr/bin/env python3.6
# vim: sw=2 ts=2

import click
import json

CTX_SILENT_MODE = 'silent'
CTX_DEBUG_MODE = 'debug'
CONTEXT_SETTINGS = dict(token_normalize_func=lambda x: x.lower())

def is_silent(ctx):
    return ctx.obj[CTX_SILENT_MODE]


def is_debug(ctx):
    return ctx.obj[CTX_DEBUG_MODE]

@click.group()
@click.option('--silent', is_flag=True, default=False, help='Accept all prompts')
@click.option('--debug', is_flag=True, default=False, help='Verbose output')
@click.pass_context
def cli(ctx, silent, debug):
    ctx.obj[CTX_SILENT_MODE] = silent
    ctx.obj[CTX_DEBUG_MODE] = debug
    click.echo('Silent mode is %s' % (is_silent(ctx) and 'on' or 'off'))
    click.echo('Debug mode is %s' % (is_silent(ctx) and 'on' or 'off'))

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.argument('filename', type=click.Path(exists=True))
def validate(ctx, filename):

    silent = is_silent(ctx)
    filename = click.format_filename(filename)

    if silent:
        click.echo('Validate {0}'.format(filename))
    elif not click.confirm('Validate {0}?'.format(filename)):
        sys.exit(1)

    with open(filename) as json_data:
        try:
            click.echo(click.style('\nJSON File: {0} is valid!'.format(filename), fg='green'))
            return json.load(json_data)
        except ValueError as e:
            click.echo(click.style('\ninvalid json: %s' % e, fg='red'))
            return None

if __name__ == '__main__':
    cli(obj={})
