# model.py

class Asset:
    def __init__(self, vendor, family, series, model):
        self._id = -1
        self.vendor = vendor
        self.family = family
        self.series = series
        self.model = model
        self._docu = self.__create_document()

    def __create_document(self):
        terms = [self.vendor, self.family, self.series, self.model]
        return " ".join(terms)
    
    def __repr__(self):
        return (
            f"Asset(\n"
            f"    Vendor: {self.vendor!r},\n"
            f"    Family {self.family!r},\n"
            f"    Series: {self.series!r}\n"
            f"    Model: {self.model!r}\n"
            f")"
        )
