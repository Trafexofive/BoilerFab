"""
Main CLI entry point for {{PROJECT_NAME}}
"""

import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from .commands import hello, info, process
from .utils.config import Config
from .utils.helpers import setup_logging

console = Console()


@click.group()
@click.version_option(version="1.0.0")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--config", "-c", help="Configuration file path")
@click.pass_context
def main(ctx, verbose, config):
    """
    {{PROJECT_NAME}} - {{#if description}}{{description}}{{else}}A powerful Python CLI application{{/if}}
    
    Use --help with any command for more information.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Setup logging
    setup_logging(verbose)
    
    # Load configuration
    ctx.obj['config'] = Config(config_path=config)
    ctx.obj['verbose'] = verbose
    ctx.obj['console'] = console


@main.command()
@click.argument('name', required=False, default='World')
@click.option('--greeting', '-g', default='Hello', help='Greeting to use')
@click.option('--count', '-c', default=1, help='Number of times to greet', type=int)
@click.pass_context
def hello(ctx, name, greeting, count):
    """
    Say hello to someone (example command)
    
    NAME: The name to greet (default: World)
    """
    console = ctx.obj['console']
    
    for i in range(count):
        if ctx.obj['verbose']:
            console.print(f"[bold green]{greeting} {name}![/bold green] (iteration {i+1})")
        else:
            console.print(f"[bold green]{greeting} {name}![/bold green]")


@main.command()
@click.pass_context  
def info(ctx):
    """
    Show application information
    """
    console = ctx.obj['console']
    config = ctx.obj['config']
    
    table = Table(title="{{PROJECT_NAME}} Information")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    table.add_row("Application", "{{PROJECT_NAME}}")
    table.add_row("Version", "1.0.0")
    table.add_row("Author", "{{author_name}}")
    table.add_row("Config File", str(config.config_path) if config.config_path else "Not specified")
    table.add_row("Verbose Mode", "Enabled" if ctx.obj['verbose'] else "Disabled")
    
    console.print(table)


@main.command()
@click.argument('input_file', type=click.File('r'))
@click.option('--output', '-o', type=click.File('w'), default='-', help='Output file (default: stdout)')
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'txt']), default='txt', help='Output format')
@click.pass_context
def process(ctx, input_file, output, format):
    """
    Process a file (example command)
    
    INPUT_FILE: Path to the input file to process
    """
    console = ctx.obj['console']
    
    try:
        # Read input file
        content = input_file.read()
        lines = content.strip().split('\n')
        
        if ctx.obj['verbose']:
            console.print(f"[blue]Processing {len(lines)} lines...[/blue]")
        
        # Simple processing: count words per line
        results = []
        for i, line in enumerate(lines, 1):
            word_count = len(line.split())
            results.append({
                'line_number': i,
                'content': line.strip(),
                'word_count': word_count
            })
        
        # Output results based on format
        if format == 'json':
            import json
            json.dump(results, output, indent=2)
        elif format == 'csv':
            import csv
            writer = csv.DictWriter(output, fieldnames=['line_number', 'content', 'word_count'])
            writer.writeheader()
            writer.writerows(results)
        else:  # txt format
            for result in results:
                output.write(f"Line {result['line_number']}: {result['word_count']} words - {result['content']}\n")
        
        console.print(f"[green]✅ Successfully processed {len(lines)} lines[/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error processing file: {e}[/red]")
        raise click.Abort()


if __name__ == "__main__":
    main()