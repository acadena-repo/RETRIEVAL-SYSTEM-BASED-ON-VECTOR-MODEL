from pathlib import Path
from data.import_catalog import import_raw
from repository.catalog import Catalog
from repository.model import Asset
from ishell.cli import IShell, create_parsers

def insert_asset(database, asset_info):
    vendor, family, series, model, *xx= asset_info
    asset = Asset(vendor, family, series, model)
    database.insert(asset)

def is_database_exist(folder_path, file_name, file_ext):
    folder = Path(folder_path)

    if not folder.is_dir():
        raise FileNotFoundError(f"The path {folder_path} is not a valid directory.")

    # Complete path to database file
    check_db = folder / f"{file_name}.{file_ext}"

    if check_db.exists() and check_db.is_file():
        return True
    else:
        return False

def main():
    LOAD_ASSETS = 4000

    if not is_database_exist("./repository", "assets_catalog", "pkl"):
        raw_catalog = import_raw("./data/catalog.txt", LOAD_ASSETS)
        database = Catalog()
        for x in range(LOAD_ASSETS):
            info = raw_catalog[x].split(",")
            insert_asset(database, info)

        database._create_vspace()
    else:
        database = Catalog.load("./repository/assets_catalog.pkl")

    parser_search, parser_select = create_parsers()

    # Run interactive shell
    IShell(database, parser_search, parser_select).cmdloop()

if __name__ == '__main__':
    main()