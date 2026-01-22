"""
Main CLI entry point
"""
import typer
from .commands import list, add, delete, show, update
from .utils import connect_host

app = typer.Typer(
    name="divein",
    help="DiveIn - SSH Connection Manager",
    add_completion=False,
    no_args_is_help=False
)

app.command(name="list", help="List all saved hosts")(list.list_hosts)
app.command(name="show", help="Show host details")(show.show_hosts)
app.command(name="add", help="Add a new host")(add.add_host)
app.command(name="update", help="Update an existing host")(update.update_host)
app.command(name="delete", help="Delete a host")(delete.delete_host)
app.command(name="rm", help="Alias for delete")(delete.delete_host)
@app.command(name="connect", help="Connect to a host", hidden=True)
def connect_trigger(identifier: str):
    connect_host(identifier)

@app.callback(invoke_without_command=True)
def cli_root(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Show the version and exit", is_eager=True)
):
    """
    DiveIn - Simple SSH Connection Manager.
    
    run 'divein <id>' or 'divein <nickname>' to connect.
    """
    # If version flag is set, print version and exit
    if version:
        print("divein 1.0.9")
        return

    # If no subcommand and no injected connect, show help
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())

def main():
    """Entry point for console_scripts"""
    import sys
    
    # Support `divein <id>` shortcut via sys.argv patching
    # If the first argument is not a known command, assume it's a host identifier for 'connect'
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        known_commands = ["add", "list", "delete", "rm", "show", "connect", "help", "--help", "-h", "--install-completion", "--show-completion"]
        
        # If it's not a flag and not a known command, treat it as `connect <arg>`
        if not cmd.startswith("-") and cmd not in known_commands:
            sys.argv.insert(1, "connect")
            
    app()

if __name__ == "__main__":
    main()