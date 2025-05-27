# import_catalog.py

def import_raw(path, max_items = -1):
    assets = []
    with open(path, "r") as f:
        for n_line, line in enumerate(f):
            asset = line.strip().replace("_"," ")
            assets.append(asset)
            if max_items > 0 and n_line >= max_items:
                break
            
    return assets
