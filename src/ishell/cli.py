# cli.py
import argparse
import cmd
import shlex

def create_parsers():
    p_search = argparse.ArgumentParser(prog='search', add_help=False)
    p_search.add_argument(
        '--query',
        required=True,
        help='Search terms separated by spaces to retrieve assets'
    )
    p_search.add_argument(
    '--top_matches',
    type=int,
    choices=range(1, 11),
    default=5,
    help='Number of top matches assets to return (1–10, default=5)'
    )

    p_select = argparse.ArgumentParser(prog='select', add_help=False)
    p_select.add_argument(
    '--idx',
    type=int,
    help='Catalog index to select an specific asset (0-4000)'
    )

    return p_search, p_select

class IShell(cmd.Cmd):
    intro = ("Retrieves the top similar assets according with query terms.\n"
             "Type `help` or `?` to list commands and `exit` to exit.\n")
    prompt = '(ReS): '

    def __init__(self, catalog, p_search, p_select, **kwargs):
        super().__init__(**kwargs)
        self._search = p_search
        self._select = p_select
        self._db = catalog

    def do_search(self, line):
        args = shlex.split(line)
        try:
            ns = self._search.parse_args(args)
            terms = ns.query
            top = ns.top_matches
            
            matches = self._db.search(terms, top)

            for item in matches:
                print(f"Query: {terms}")
                print("".center(50, "-"))
                print(f"Confidence: {item[0]:.4f} | Document: {item[1]}")
                print(item[2])
                print("".center(50, "="))
            
        except SystemExit:
            pass
    
    def do_select(self, line):
        args = shlex.split(line)
        try:
            ns = self._select.parse_args(args)
            asset_id = ns.idx
            
            asset = self._db.get_asset(asset_id)

            print(asset)
            print("".center(50, "="))
            
        except SystemExit:
            pass

    def do_exit(self, line):
        print("Exiting Interactive Shell...")
        return True

    def do_help(self, arg):
        """Shows help for commands"""
        if arg:
            if arg in ('search', 'select'):
                {'search': self._search, 'select': self._select}[arg].print_help()
            else:
                print(f"There is no help for: {arg!r}")
        else:
            print("Available Commands:")
            print("  search --query 'term1 term2 ...'")
            print("  select --idx N, where N = [0, 3999]")
            print("  exit   Close interactive shell")