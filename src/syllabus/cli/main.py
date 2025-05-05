"""Main command line interface for the syllabus package."""

# pylint: disable=C0116, C0115, W0613, E1120, W0107, W0622

import logging
import os
from dataclasses import dataclass
from pathlib import Path

import click

from syllabus.models import Course
from syllabus.sync import read_module, sync_syllabus, renumber_lessons, regroup_lessons, check_structure
from syllabus import __version__  # Import the package version


logger = logging.getLogger(__name__)


def setup_logging(verbose):

    if verbose == 1:
        log_level = logging.INFO
    elif verbose > 1:
        log_level = logging.DEBUG
    else:
        log_level = logging.ERROR

    logging.basicConfig(level=logging.ERROR,
                        format='%(levelname)s: %(message)s')
    logger.setLevel(log_level)


@dataclass
class Context:
    file: Path = None
    verbose: bool = False
    exceptions: bool = False
    syllabus: Course = None
    workspace: Path = None


@click.pass_context
def syllabus(ctx):

    if ctx.obj.syllabus is not None:
        return ctx.obj.syllabus

    if not ctx.obj.file.exists():
        logger.error("Error: The file %s does not exist.", ctx.obj.file)
        exit(1)

    ctx.obj.syllabus = Course.from_yaml(ctx.obj.file)

    return ctx.obj.syllabus


@click.group()
@click.option('-v', '--verbose', count=True, help="Increase verbosity level.")
@click.option('-e', '--exceptions', is_flag=True, help="Raise exceptions on errors.")
@click.option('-f', '--file', type=click.Path(), help="Specify the syllabus file.", default=Path("syllabus.yaml"))
@click.option('-w', '--workspace', type=click.Path(), help="User's working directory.", default=Path('./workspace'))
@click.option('-d', '--dir', type=click.Path(), help="Set the working directory.", default=Path('.'))
@click.pass_context
def cli(ctx, verbose, exceptions, file, workspace, dir):
    setup_logging(verbose)

    ctx.obj = Context()

    if dir:
        if not Path(dir).exists():
            logger.error(
                "Error: The working directory %s does not exist.", dir)
            exit(1)
        os.chdir(dir)

    ctx.obj.file = Path(file)

    workspace = Path(workspace)
    ctx.obj.workspace = workspace


@click.command()
def version():
    """Show the version and exit."""
    print(f"Syllabus CLI version {__version__}")


cli.add_command(version)


@click.command()
@click.option('-n', '--name', type=str, required=True, help="Name of the course.")
@click.option('-d', '--description', type=str, help="Description of the description.")
@click.pass_context
def new(ctx, name, description):
    """Create a new syllabus file."""

    new_syllabus = Course(name=name, description=description)
    ctx.obj.file.write_text(new_syllabus.to_yaml())

    print(f"Created new syllabus file at {ctx.obj.file}")


cli.add_command(new)



@click.command()
@click.argument('lesson_dir', type=click.Path(exists=True))
@click.pass_context
def check(ctx, lesson_dir):
    """Validate the structure of the lesson directory."""
    

    try:
        check_structure(Path(lesson_dir))
    except Exception as e:
        logger.error("Error: %s", e)
        exit(1)
        


cli.add_command(check)


@click.command()
@click.argument('module_dir', type=click.Path(exists=True))
@click.option('-p', '--print', 'print_only', is_flag=True, help="Print the module rather than add to the syllabus.")
@click.option('-ng', '--no-group', 'nogroup', is_flag=True, help="Group lessons with the same basename. ")
@click.option('-r', '--recursive', is_flag=True, help="Import all modules in the directory recursively.")
@click.pass_context
def import_module(ctx, module_dir, print_only, nogroup, recursive=False):
    """Import a module from the specified directory."""

    module_path = Path(module_dir)

    if recursive:
        for subdir in sorted(module_path.iterdir()):
            if subdir.stem.lower() == 'readme':
                continue
            if not subdir.is_dir():
                continue
            if subdir.is_dir():
                ctx.invoke(import_module, module_dir=subdir,
                           print_only=print_only, nogroup=nogroup, recursive=False)
        return

    if not module_path.is_dir():
        logger.info(
            "Error: The directory %s does not exist or is not a directory.", module_dir)
        exit(1)

    # Add logic to import the module
    logger.info("Importing module from %s...", module_dir)
    module = read_module(module_path, group=not nogroup)

    if print_only:
        print(module.to_yaml())
    else:
        s = syllabus()
        if not s.modules:
            s.modules = []
        s.modules.append(module)

        ctx.obj.file.write_text(s.to_yaml())

        print(f"Updated syllabus to {ctx.obj.file}")


cli.add_command(import_module, name='import')


@click.command()
@click.argument('lesson_dir', type=click.Path(exists=True))
@click.pass_context
def sync(ctx, lesson_dir):
    """Import a module from the specified directory."""
    sync_syllabus(
        lesson_dir=Path(lesson_dir),
        syllabus=syllabus())

cli.add_command(sync, name='sync')


@click.command()
@click.argument('lesson_dir', type=click.Path(exists=True))
@click.option('-d', '--dryrun', is_flag=True, help="Perform a dry run without renaming files.")
@click.option('-i', '--increment', type=int, default=1, help="Increment the lesson numbers by this amount.")
@click.pass_context
def renumber(ctx, lesson_dir, dryrun, increment):
    """Import a module from the specified directory."""
    renumber_lessons(lesson_dir=Path(lesson_dir),
                     increment=increment, dryrun=dryrun)


cli.add_command(renumber, name='renumber')


@click.command()
@click.argument('lesson_dir', type=click.Path(exists=True))
@click.option('-d', '--dryrun', is_flag=True, help="Perform a dry run without renaming files.")
@click.pass_context
def regroup(ctx, lesson_dir, dryrun):
    """Import a module from the specified directory."""
    regroup_lessons(lesson_dir=Path(lesson_dir), dryrun=dryrun)


cli.add_command(regroup, name='regroup')


def run():
    cli()


if __name__ == "__main__":
    run()
