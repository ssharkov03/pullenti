# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class GeoTokenData:
    
    def __init__(self, t : 'Token') -> None:
        self.tok = None;
        self.npt = None;
        self.terr = None;
        self.cit = None;
        self.org_typ = None;
        self.org0_ = None;
        self.street = None;
        self.addr = None;
        self.no_geo = False
        self.tok = t
        t.tag = (self)
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print(str(self.tok), end="", file=tmp)
        if (self.npt is not None): 
            print(" \r\nNpt: {0}".format(str(self.npt)), end="", file=tmp, flush=True)
        if (self.terr is not None): 
            print(" \r\nTerr: {0}".format(str(self.terr)), end="", file=tmp, flush=True)
        if (self.cit is not None): 
            print(" \r\nCit: {0}".format(str(self.cit)), end="", file=tmp, flush=True)
        if (self.org0_ is not None): 
            print(" \r\nOrg: {0}".format(str(self.org0_)), end="", file=tmp, flush=True)
        if (self.org_typ is not None): 
            print(" \r\nOrgTyp: {0}".format(str(self.org_typ)), end="", file=tmp, flush=True)
        if (self.street is not None): 
            print(" \r\nStreet: {0}".format(str(self.street)), end="", file=tmp, flush=True)
        if (self.addr is not None): 
            print(" \r\nAddr: {0}".format(str(self.addr)), end="", file=tmp, flush=True)
        if (self.no_geo): 
            print(" \r\nNO GEO!!!", end="", file=tmp)
        return Utils.toStringStringIO(tmp)