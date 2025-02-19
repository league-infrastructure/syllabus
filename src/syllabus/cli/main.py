import click
from pathlib import Path
from syllabus.models import  Course
from dataclasses import dataclass
import yaml

import logging

logger = logging.getLogger(__name__)    

def setup_logging(verbose):
    
    if verbose == 1:
        log_level = logging.INFO
    elif verbose > 1:
        log_level = logging.DEBUG
    else:
        log_level = logging.ERROR


    logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')   
    logger.setLevel(log_level)

@dataclass
class Context:
    file: Path = None
    verbose: bool = False
    exceptions: bool = False
    syllabus: Course = None
    workspace: Path = None

@click.group()
@click.option('-v', '--verbose', count=True, help="Increase verbosity level.")
@click.option('-e', '--exceptions', is_flag=True, help="Raise exceptions on errors.")
@click.option('-f', '--file', type=click.Path(), help="Specify the syllabus file.", default=Path("syllabus.yaml"))
@click.option('-w', '--workspace', type=click.Path(), help="User's working directory.", default=Path('./workspace'))
@click.pass_context
def cli(ctx, verbose, exceptions, file, workspace):
    setup_logging(verbose)
    
    ctx.obj = Context()
    
    file_path = Path(file)
    if not file_path.exists():
        logger.error(f"Error: Thecd ../ file {file} does not exist.")
        exit(1)
    else:
        ctx.obj.file = file_path
        
    if not ctx.obj.file.exists():
        logger.error(f"Error: The syllabus file {ctx.obj.file} does not exist.")
        exit(1)

    workspace = Path(workspace)
    if not workspace.exists():
        logger.error(f"Error: The workspace '{workspace}' does not exist.  )")
        exit(1)
    else:
        ctx.obj.workspace = workspace

    ctx.obj.syllabus = Course.from_yaml(ctx.obj.file)


@click.command()
@click.pass_context
def inspect(ctx):
    """Inspect and report on the environment"""
    
    print(ctx.obj.syllabus.to_yaml())

cli.add_command(inspect)

@click.command()
def build():
    """Build the syllabus."""
    pass

cli.add_command(build)

@click.command()
def renumber():
    """Renumber the syllabus sections."""
    pass

cli.add_command(renumber)

@click.command()
@click.option('-e', '--exists', is_flag=True, help="Check that referenced files exist.")
@click.option('-c', '--create', is_flag=True, help="Create files that are referenced but don't exist.")
def check(exists, create):
    """Check the syllabus for errors."""
    if exists:
        logger.info("Checking that referenced files exist...")
        # Add logic to check file existence

    if create:
        logger.info("Creating files that are referenced but don't exist...")
        # Add logic to create files if they don't exist

cli.add_command(check)


@click.command()
@click.argument('module_dir', type=click.Path(exists=True))
@click.option('-p', '--print', 'print_only', is_flag=True, help="Print the module rather than add to the syllabus.")
@click.option('-ng', '--no-group', 'nogroup', is_flag=True, help="Group lessons with the same basename. ")
@click.pass_context
def import_module(ctx, module_dir, print_only, nogroup):
    """Import a module from the specified directory."""
    
    from syllabus.sync import read_module
    
    module_path = Path(module_dir)
    if not module_path.is_dir():
        logger.info(f"Error: The directory {module_dir} does not exist or is not a directory.")
        exit(1)
    
    # Add logic to import the module
    logger.info(f"Importing module from {module_dir}...")
    module = read_module(module_path, group=not nogroup)
    
    if print_only:
        print(module.to_yaml())
    else:
        s = ctx.obj.syllabus
        s.modules.append(module)
        
        ctx.obj.file.write_text(s.to_yaml())
        
        print(f"Updated syllabus to {ctx.obj.file}")

cli.add_command(import_module, name='import')

def run():
    cli()

if __name__ == "__main__":
    run()