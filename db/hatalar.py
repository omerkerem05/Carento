class YanlisKullanici(Exception):
    pass

class GecersizTarihHatasi(Exception):
    pass

class BosStringHatasi(Exception):
    pass

class GecersizUcretHatasi(Exception):
    pass

class CakismaHatasi(Exception):
    pass

class YanlisTipHatasi(Exception):
    pass

class NoneDegerHatasi(Exception):
    pass

def reraise_sqlite_err(err):
    match err.sqlite_errorcode:
            case 1299:
                raise NoneDegerHatasi from None
            case 2067:
                raise CakismaHatasi from None
    
    raise err 

