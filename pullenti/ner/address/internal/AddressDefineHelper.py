# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.geo.internal.GeoOwnerHelper import GeoOwnerHelper
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.Token import Token
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper

class AddressDefineHelper:
    
    @staticmethod
    def try_define(li : typing.List['AddressItemToken'], t : 'Token', ad : 'AnalyzerData') -> 'Token':
        if (li is None or len(li) == 0): 
            return None
        empty = True
        not_empty = False
        bad_org = False
        for v in li: 
            if (v.typ == AddressItemType.NUMBER or v.typ == AddressItemType.ZIP or v.typ == AddressItemType.DETAIL): 
                pass
            elif (v.typ == AddressItemType.HOUSE and v.is_doubt): 
                pass
            elif (v.typ != AddressItemType.STREET): 
                empty = False
                if (v.typ != AddressItemType.CITY and v.typ != AddressItemType.COUNTRY and v.typ != AddressItemType.REGION): 
                    not_empty = True
            elif (isinstance(v.referent, StreetReferent)): 
                s = Utils.asObjectOrNull(v.referent, StreetReferent)
                if (s.kind == StreetKind.RAILWAY and s.number is None): 
                    pass
                elif (s.kind == StreetKind.ORG): 
                    if (v.ref_token is not None and not v.ref_token_is_gsk): 
                        bad_org = True
                    if (bad_org): 
                        if (v == li[0]): 
                            return None
                        elif (li[0].typ == AddressItemType.PREFIX and v == li[1]): 
                            return None
                elif (s.kind == StreetKind.AREA): 
                    pass
                else: 
                    empty = False
                    not_empty = True
        if (empty): 
            return None
        if (not not_empty): 
            for v in li: 
                if (v != li[0] and v.is_newline_before): 
                    return None
            if (bad_org and not MiscLocationHelper.is_user_param_address(li[0])): 
                return None
            if (li[0].typ == AddressItemType.STREET and li[0].referent.kind == StreetKind.ORG): 
                return None
            if (len(li) == 1 and li[0].typ != AddressItemType.STREET and li[0].detail_meters == 0): 
                return None
        if ((len(li) > 3 and li[0].typ == AddressItemType.CITY and li[1].typ == AddressItemType.STREET) and li[2].typ == AddressItemType.CITY and li[3].typ == AddressItemType.STREET): 
            if (li[1].referent.kind == StreetKind.RAILWAY or li[1].referent.kind == StreetKind.ROAD): 
                geo = Utils.asObjectOrNull(li[2].referent, GeoReferent)
                if (geo is not None and geo.higher is None and GeoOwnerHelper.can_be_higher(Utils.asObjectOrNull(li[0].referent, GeoReferent), geo, None, None)): 
                    geo.higher = Utils.asObjectOrNull(li[0].referent, GeoReferent)
                    li[2] = li[2].clone()
                    li[2].begin_token = li[0].begin_token
                    del li[0:0+2]
        if (len(li) >= 2 and li[0].typ == AddressItemType.BLOCK and li[1].typ == AddressItemType.STREET): 
            return None
        if (len(li) >= 2 and li[0].typ == AddressItemType.CITY and li[1].typ == AddressItemType.BUILDING): 
            if (li[1].begin_token.is_value("СТР", None) and not MiscLocationHelper.is_user_param_address(li[1])): 
                return None
        if (li[0].typ == AddressItemType.STREET): 
            if (li[0].ref_token is not None): 
                if (not li[0].ref_token_is_gsk or li[0].referent.kind == StreetKind.AREA): 
                    return None
        addr = AddressReferent()
        streets = list()
        i = 0
        j = 0
        metro = None
        details = list()
        geos = None
        err = False
        cross = False
        i = 0
        while i < len(li): 
            if ((li[i].typ == AddressItemType.DETAIL and li[i].detail_type == AddressDetailType.CROSS and ((i + 2) < len(li))) and li[i + 1].typ == AddressItemType.STREET and li[i + 2].typ == AddressItemType.STREET): 
                cross = True
                streets.append(li[i + 1])
                streets.append(li[i + 2])
                li[i + 1].end_token = li[i + 2].end_token
                li[i].tag = (addr)
                li[i + 1].tag = (addr)
                del li[i + 2]
                break
            elif (li[i].typ == AddressItemType.STREET): 
                if (((li[i].ref_token is not None and not li[i].ref_token_is_gsk)) and len(streets) == 0): 
                    if (i > 0 and li[i].is_newline_before): 
                        err = True
                        del li[i:i+len(li) - i]
                        break
                    elif ((i + 1) == len(li)): 
                        err = len(details) == 0
                    elif (((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.NUMBER): 
                        err = True
                    if (err and geos is not None): 
                        for ii in range(i - 1, -1, -1):
                            if (li[ii].typ == AddressItemType.ZIP or li[ii].typ == AddressItemType.PREFIX): 
                                err = False
                    if (err and not MiscLocationHelper.is_user_param_address(li[i])): 
                        break
                li[i].tag = (addr)
                streets.append(li[i])
                if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.STREET): 
                    pass
                else: 
                    break
            elif (li[i].typ == AddressItemType.CITY or li[i].typ == AddressItemType.REGION): 
                if (geos is None): 
                    geos = list()
                geo = Utils.asObjectOrNull(li[i].referent, GeoReferent)
                if (li[i].detail_type != AddressDetailType.UNDEFINED): 
                    details.append(li[i])
                    if (len(geos) == 0): 
                        if (geo.higher is not None): 
                            geos.append(geo.higher)
                        else: 
                            geos.append(geo)
                else: 
                    geos.insert(0, geo)
                li[i].tag = (addr)
            elif (li[i].typ == AddressItemType.DETAIL): 
                details.append(li[i])
                li[i].tag = (addr)
            i += 1
        if ((i >= len(li) and metro is None and len(details) == 0) and not cross): 
            i = 0
            first_pass2744 = True
            while True:
                if first_pass2744: first_pass2744 = False
                else: i += 1
                if (not (i < len(li))): break
                cit = False
                if (li[i].typ == AddressItemType.CITY): 
                    cit = True
                elif (li[i].typ == AddressItemType.REGION): 
                    for s in li[i].referent.slots: 
                        if (s.type_name == GeoReferent.ATTR_TYPE): 
                            ss = Utils.asObjectOrNull(s.value, str)
                            if ("посел" in ss or "сельск" in ss or "почтовое отделение" in ss): 
                                cit = True
                if (cit): 
                    if (((i + 1) < len(li)) and (((((li[i + 1].typ == AddressItemType.HOUSE or li[i + 1].typ == AddressItemType.BLOCK or li[i + 1].typ == AddressItemType.PLOT) or li[i + 1].typ == AddressItemType.FIELD or li[i + 1].typ == AddressItemType.BUILDING) or li[i + 1].typ == AddressItemType.CORPUS or li[i + 1].typ == AddressItemType.POSTOFFICEBOX) or li[i + 1].typ == AddressItemType.CSP))): 
                        break
                    if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.NUMBER): 
                        if (li[i].end_token.next0_.is_comma): 
                            if ((isinstance(li[i].referent, GeoReferent)) and not li[i].referent.is_big_city and li[i].referent.is_city): 
                                li[i + 1].typ = AddressItemType.HOUSE
                                li[i + 1].is_doubt = True
                                break
                    if (li[0].typ == AddressItemType.ZIP or li[0].typ == AddressItemType.PREFIX): 
                        break
                    continue
                if (li[i].typ == AddressItemType.REGION): 
                    if ((isinstance(li[i].referent, GeoReferent)) and li[i].referent.higher is not None and li[i].referent.higher.is_city): 
                        if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.HOUSE): 
                            break
            if (i >= len(li)): 
                return None
        if (err and not MiscLocationHelper.is_user_param_address(li[0])): 
            return None
        i0 = i
        if (i > 0 and li[i - 1].typ == AddressItemType.HOUSE and li[i - 1].is_digit): 
            addr.add_slot(AddressReferent.ATTR_HOUSE, li[i - 1].value, False, 0).tag = li[i - 1]
            li[i - 1].tag = (addr)
        elif ((i > 0 and li[i - 1].typ == AddressItemType.KILOMETER and li[i - 1].is_digit) and (i < len(li)) and li[i].is_street_road): 
            addr.add_slot(AddressReferent.ATTR_KILOMETER, li[i - 1].value, False, 0).tag = li[i - 1]
            li[i - 1].tag = (addr)
        else: 
            if (i >= len(li)): 
                i = -1
            i = 0
            first_pass2745 = True
            while True:
                if first_pass2745: first_pass2745 = False
                else: i += 1
                if (not (i < len(li))): break
                if (li[i].tag is not None): 
                    continue
                if (li[i].typ == AddressItemType.HOUSE): 
                    if (addr.house is not None): 
                        break
                    if (li[i].value is not None): 
                        attr = AddressReferent.ATTR_HOUSE
                        if (li[i].is_doubt): 
                            attr = AddressReferent.ATTR_HOUSEORPLOT
                            if (((i + 1) < len(li)) and (((li[i + 1].typ == AddressItemType.FLAT or li[i + 1].typ == AddressItemType.POTCH or li[i + 1].typ == AddressItemType.FLOOR) or li[i + 1].typ == AddressItemType.NUMBER))): 
                                attr = AddressReferent.ATTR_HOUSE
                        addr.add_slot(attr, li[i].value, False, 0).tag = li[i]
                        if (li[i].house_type != AddressHouseType.UNDEFINED): 
                            addr.house_type = li[i].house_type
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.KILOMETER and li[i].is_digit and (((i0 < len(li)) and li[i0].is_street_road))): 
                    if (addr.kilometer is not None): 
                        break
                    s = addr.add_slot(AddressReferent.ATTR_KILOMETER, li[i].value, False, 0)
                    if (s is not None): 
                        s.tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.PLOT): 
                    if (addr.plot is not None): 
                        break
                    s = addr.add_slot(AddressReferent.ATTR_PLOT, li[i].value, False, 0)
                    if (s is not None): 
                        s.tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.FIELD): 
                    if (addr.field is not None): 
                        break
                    s = addr.add_slot(AddressReferent.ATTR_FIELD, li[i].value, False, 0)
                    if (s is not None): 
                        s.tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.BOX and li[i].is_digit): 
                    if (addr.box is not None): 
                        break
                    s = addr.add_slot(AddressReferent.ATTR_BOX, li[i].value, False, 0)
                    if (s is not None): 
                        s.tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.BLOCK and li[i].is_digit): 
                    if (addr.block is not None): 
                        break
                    s = addr.add_slot(AddressReferent.ATTR_BLOCK, li[i].value, False, 0)
                    if (s is not None): 
                        s.tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.CORPUS): 
                    if (addr.corpus is not None): 
                        break
                    if (li[i].value is not None): 
                        s = addr.add_slot(AddressReferent.ATTR_CORPUS, li[i].value, False, 0)
                        if (s is not None): 
                            s.tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.BUILDING): 
                    if (addr.building is not None): 
                        break
                    if (li[i].value is not None): 
                        s = addr.add_slot(AddressReferent.ATTR_BUILDING, li[i].value, False, 0)
                        if (s is not None): 
                            s.tag = li[i]
                        if (li[i].building_type != AddressBuildingType.UNDEFINED): 
                            addr.building_type = li[i].building_type
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.FLOOR and li[i].is_digit): 
                    if (addr.floor0_ is not None): 
                        break
                    s = addr.add_slot(AddressReferent.ATTR_FLOOR, li[i].value, False, 0)
                    if (s is not None): 
                        s.tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.POTCH and li[i].is_digit): 
                    if (addr.potch is not None): 
                        break
                    s = addr.add_slot(AddressReferent.ATTR_PORCH, li[i].value, False, 0)
                    if (s is not None): 
                        s.tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.FLAT): 
                    if (addr.flat is not None): 
                        break
                    if (li[i].value is not None): 
                        addr.add_slot(AddressReferent.ATTR_FLAT, li[i].value, False, 0).tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.PAVILION): 
                    if (addr.pavilion is not None): 
                        break
                    if (li[i].value is not None): 
                        addr.add_slot(AddressReferent.ATTR_PAVILION, li[i].value, False, 0).tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.OFFICE and li[i].is_digit): 
                    if (addr.office is not None): 
                        break
                    s = addr.add_slot(AddressReferent.ATTR_OFFICE, li[i].value, False, 0)
                    if (s is not None): 
                        s.tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.ROOM and li[i].is_digit): 
                    if (addr.room is not None): 
                        break
                    s = addr.add_slot(AddressReferent.ATTR_ROOM, li[i].value, False, 0)
                    if (s is not None): 
                        s.tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.CORPUSORFLAT and ((li[i].is_digit or li[i].value is None))): 
                    j = (i + 1)
                    while j < len(li): 
                        if (li[j].is_digit): 
                            if ((((li[j].typ == AddressItemType.FLAT or li[j].typ == AddressItemType.CORPUSORFLAT or li[j].typ == AddressItemType.OFFICE) or li[j].typ == AddressItemType.FLOOR or li[j].typ == AddressItemType.POTCH) or li[j].typ == AddressItemType.POSTOFFICEBOX or li[j].typ == AddressItemType.BUILDING) or li[j].typ == AddressItemType.PAVILION): 
                                break
                        j += 1
                    if (li[i].value is not None): 
                        if ((j < len(li)) and addr.corpus is None): 
                            addr.add_slot(AddressReferent.ATTR_CORPUS, li[i].value, False, 0).tag = li[i]
                        elif (addr.corpus is not None): 
                            addr.add_slot(AddressReferent.ATTR_FLAT, li[i].value, False, 0).tag = li[i]
                        else: 
                            addr.add_slot(AddressReferent.ATTR_CORPUSORFLAT, li[i].value, False, 0).tag = li[i]
                    li[i].tag = (addr)
                elif ((not li[i].is_newline_before and li[i].typ == AddressItemType.NUMBER and li[i].is_digit) and li[i - 1].typ == AddressItemType.STREET): 
                    v = 0
                    wrapv229 = RefOutArgWrapper(0)
                    inoutres230 = Utils.tryParseInt(li[i].value, wrapv229)
                    v = wrapv229.value
                    if (not inoutres230): 
                        wrapv223 = RefOutArgWrapper(0)
                        inoutres224 = Utils.tryParseInt(li[i].value[0:0+len(li[i].value) - 1], wrapv223)
                        v = wrapv223.value
                        if (not inoutres224): 
                            if (not "/" in li[i].value): 
                                break
                    if (v > 500 and not MiscLocationHelper.is_user_param_address(li[0])): 
                        break
                    attr = AddressReferent.ATTR_HOUSEORPLOT
                    if (((i + 1) < len(li)) and (((li[i + 1].typ == AddressItemType.FLAT or li[i + 1].typ == AddressItemType.POTCH or li[i + 1].typ == AddressItemType.FLOOR) or li[i + 1].typ == AddressItemType.NUMBER or ((li[i + 1].typ == AddressItemType.STREET and li[i + 1].ref_token_is_gsk))))): 
                        attr = AddressReferent.ATTR_HOUSE
                    addr.add_slot(attr, li[i].value, False, 0).tag = li[i]
                    li[i].tag = (addr)
                    if (((i + 1) < len(li)) and ((li[i + 1].typ == AddressItemType.NUMBER or li[i + 1].typ == AddressItemType.FLAT)) and not li[i + 1].is_newline_before): 
                        wrapv227 = RefOutArgWrapper(0)
                        inoutres228 = Utils.tryParseInt(li[i + 1].value, wrapv227)
                        v = wrapv227.value
                        if (inoutres228): 
                            if (v > 500 and not MiscLocationHelper.is_user_param_address(li[0])): 
                                break
                        i += 1
                        if ((((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.BUILDING and not li[i + 1].is_newline_before) and li[i + 1].building_type == AddressBuildingType.LITER): 
                            addr.add_slot(AddressReferent.ATTR_CORPUS, li[i].value, False, 0).tag = li[i]
                            li[i].tag = (addr)
                            continue
                        if ((li[i].typ == AddressItemType.NUMBER and li[i].end_token.next0_ is not None and li[i].end_token.next0_.is_comma) and li[i].begin_token.previous.is_comma): 
                            if (((i + 1) < len(li)) and ((li[i + 1].typ == AddressItemType.CORPUS or li[i + 1].typ == AddressItemType.CORPUSORFLAT))): 
                                addr.add_slot(AddressReferent.ATTR_BUILDING, li[i].value, False, 0).tag = li[i]
                                li[i].tag = (addr)
                                continue
                            else: 
                                addr.add_slot(AddressReferent.ATTR_CORPUS, li[i].value, False, 0).tag = li[i]
                                li[i].tag = (addr)
                                continue
                        if ((((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.NUMBER and not li[i + 1].is_newline_before) and (v < 5)): 
                            wrapv225 = RefOutArgWrapper(0)
                            inoutres226 = Utils.tryParseInt(li[i + 1].value, wrapv225)
                            v = wrapv225.value
                            if (inoutres226): 
                                if ((v < 500) or MiscLocationHelper.is_user_param_address(li[0])): 
                                    addr.add_slot(AddressReferent.ATTR_CORPUS, li[i].value, False, 0).tag = li[i]
                                    li[i].tag = (addr)
                                    i += 1
                        if (li[i].begin_token.previous.is_hiphen or addr.find_slot(AddressReferent.ATTR_CORPUS, None, True) is not None): 
                            addr.add_slot(AddressReferent.ATTR_FLAT, li[i].value, False, 0).tag = li[i]
                        else: 
                            addr.add_slot(AddressReferent.ATTR_CORPUSORFLAT, li[i].value, False, 0).tag = li[i]
                        li[i].tag = (addr)
                elif ((not li[i].is_newline_before and li[i].typ == AddressItemType.NUMBER and li[i].is_digit) and ((li[i - 1].typ == AddressItemType.NUMBER or li[i - 1].typ == AddressItemType.HOUSE))): 
                    if (addr.flat is not None): 
                        break
                    if (addr.house is None and addr.building is None and addr.corpus is None): 
                        break
                    addr.add_slot(AddressReferent.ATTR_FLAT, li[i].value, False, 0).tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.CITY): 
                    if (geos is None): 
                        geos = list()
                    if (li[i].is_newline_before): 
                        if (len(geos) > 0): 
                            if ((i > 0 and li[i - 1].typ != AddressItemType.CITY and li[i - 1].typ != AddressItemType.REGION) and li[i - 1].typ != AddressItemType.ZIP and li[i - 1].typ != AddressItemType.PREFIX): 
                                break
                        if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.STREET and i > i0): 
                            break
                    if (li[i].detail_type != AddressDetailType.UNDEFINED): 
                        details.append(li[i])
                        li[i].tag = (addr)
                        if (len(geos) > 0): 
                            continue
                    ii = 0
                    ii = 0
                    while ii < len(geos): 
                        if (geos[ii].is_city): 
                            break
                        ii += 1
                    if (ii >= len(geos)): 
                        geos.append(Utils.asObjectOrNull(li[i].referent, GeoReferent))
                    elif (i > 0 and li[i].is_newline_before and i > i0): 
                        jj = 0
                        jj = 0
                        while jj < i: 
                            if ((li[jj].typ != AddressItemType.PREFIX and li[jj].typ != AddressItemType.ZIP and li[jj].typ != AddressItemType.REGION) and li[jj].typ != AddressItemType.COUNTRY and li[jj].typ != AddressItemType.CITY): 
                                break
                            jj += 1
                        if (jj < i): 
                            break
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.POSTOFFICEBOX): 
                    if (addr.post_office_box is not None): 
                        break
                    addr.add_slot(AddressReferent.ATTR_POSTOFFICEBOX, Utils.ifNotNull(li[i].value, ""), False, 0).tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.CSP): 
                    if (addr.csp is not None): 
                        break
                    addr.add_slot(AddressReferent.ATTR_CSP, li[i].value, False, 0).tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.STREET): 
                    if (len(streets) > 1): 
                        break
                    if (len(streets) > 0): 
                        if (li[i].is_newline_before): 
                            break
                        if (MiscHelper.can_be_start_of_sentence(li[i].begin_token)): 
                            break
                    if (li[i].ref_token is None and i > 0 and li[i - 1].typ != AddressItemType.STREET): 
                        break
                    if (len(streets) > 0): 
                        ss = Utils.asObjectOrNull(li[i].referent, StreetReferent)
                        if (ss.kind == StreetKind.ORG and streets[len(streets) - 1].referent.kind == StreetKind.UNDEFINED): 
                            details.append(li[i])
                            li[i].tag = (addr)
                            continue
                    streets.append(li[i])
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.DETAIL): 
                    if ((i + 1) == len(li) and li[i].detail_type == AddressDetailType.NEAR): 
                        break
                    if (li[i].detail_type == AddressDetailType.NEAR and ((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.CITY): 
                        details.append(li[i])
                        li[i].tag = (addr)
                        i += 1
                    details.append(li[i])
                    li[i].tag = (addr)
                elif (i > i0): 
                    break
        if (len(streets) == 1 and streets[0].orto_terr is not None): 
            streets.insert(0, streets[0].orto_terr)
        typs = list()
        for s in addr.slots: 
            if (not s.type_name in typs): 
                typs.append(s.type_name)
        if (len(streets) == 1 and not streets[0].is_doubt and streets[0].ref_token is None): 
            pass
        elif (len(li) > 2 and li[0].typ == AddressItemType.ZIP and ((li[1].typ == AddressItemType.COUNTRY or li[1].typ == AddressItemType.REGION))): 
            pass
        elif ((len(typs) + len(streets)) < 2): 
            if (len(typs) > 0): 
                if (((((typs[0] != AddressReferent.ATTR_STREET and typs[0] != AddressReferent.ATTR_POSTOFFICEBOX and metro is None) and typs[0] != AddressReferent.ATTR_HOUSE and typs[0] != AddressReferent.ATTR_HOUSEORPLOT) and typs[0] != AddressReferent.ATTR_CORPUS and typs[0] != AddressReferent.ATTR_BUILDING) and typs[0] != AddressReferent.ATTR_PLOT and typs[0] != AddressReferent.ATTR_DETAIL) and len(details) == 0 and not cross): 
                    return None
            elif (len(streets) == 0 and len(details) == 0 and not cross): 
                if (li[i - 1].typ == AddressItemType.CITY and i > 2 and li[i - 2].typ == AddressItemType.ZIP): 
                    pass
                else: 
                    return None
            elif ((i == len(li) and len(streets) == 1 and (isinstance(streets[0].referent, StreetReferent))) and streets[0].referent.find_slot(StreetReferent.ATTR_TYPE, "квартал", True) is not None): 
                return None
            if (geos is None): 
                has_geo = False
                tt = li[0].begin_token.previous
                first_pass2746 = True
                while True:
                    if first_pass2746: first_pass2746 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.morph.class0_.is_preposition or tt.is_comma): 
                        continue
                    r = tt.get_referent()
                    if (r is None): 
                        break
                    if (r.type_name == "DATE" or r.type_name == "DATERANGE"): 
                        continue
                    if (isinstance(r, GeoReferent)): 
                        if (not r.is_state): 
                            if (geos is None): 
                                geos = list()
                            geos.append(Utils.asObjectOrNull(r, GeoReferent))
                            has_geo = True
                    break
                if (not has_geo): 
                    if (len(streets) > 0 and streets[0].ref_token_is_gsk and streets[0].ref_token is not None): 
                        pass
                    else: 
                        return None
        i = 0
        while i < len(li): 
            if (li[i].typ == AddressItemType.PREFIX): 
                li[i].tag = (addr)
            elif (li[i].tag is None): 
                if (li[i].is_newline_before and i > i0): 
                    stop = False
                    j = (i + 1)
                    while j < len(li): 
                        if (li[j].typ == AddressItemType.STREET): 
                            stop = True
                            break
                        j += 1
                    if (stop): 
                        break
                if (li[i].typ == AddressItemType.COUNTRY or li[i].typ == AddressItemType.REGION or li[i].typ == AddressItemType.CITY): 
                    if (geos is None): 
                        geos = list()
                    if (not Utils.asObjectOrNull(li[i].referent, GeoReferent) in geos): 
                        geos.append(Utils.asObjectOrNull(li[i].referent, GeoReferent))
                    if (li[i].typ != AddressItemType.COUNTRY): 
                        if (li[i].detail_type != AddressDetailType.UNDEFINED and addr.detail == AddressDetailType.UNDEFINED): 
                            addr.add_slot(AddressReferent.ATTR_DETAIL, Utils.enumToString(li[i].detail_type).upper(), False, 0).tag = li[i]
                            if (li[i].detail_meters > 0): 
                                addr.add_slot(AddressReferent.ATTR_DETAILPARAM, "{0}м".format(li[i].detail_meters), False, 0)
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.ZIP): 
                    if (addr.zip0_ is not None): 
                        break
                    addr.add_slot(AddressReferent.ATTR_ZIP, li[i].value, False, 0).tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.POSTOFFICEBOX): 
                    if (addr.post_office_box is not None): 
                        break
                    addr.add_slot(AddressReferent.ATTR_POSTOFFICEBOX, li[i].value, False, 0).tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.CSP): 
                    if (addr.csp is not None): 
                        break
                    addr.add_slot(AddressReferent.ATTR_CSP, li[i].value, False, 0).tag = li[i]
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.NUMBER and li[i].is_digit and len(li[i].value) == 6): 
                    if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.CITY): 
                        if (addr.zip0_ is not None): 
                            break
                        addr.add_slot(AddressReferent.ATTR_ZIP, li[i].value, False, 0).tag = li[i]
                        li[i].tag = (addr)
                else: 
                    break
            i += 1
        t0 = None
        t1 = None
        i = 0
        while i < len(li): 
            if (li[i].tag is not None): 
                t0 = li[i].begin_token
                break
            i += 1
        for i in range(len(li) - 1, -1, -1):
            if (li[i].tag is not None): 
                t1 = li[i].end_token
                break
        else: i = -1
        if (t0 is None or t1 is None): 
            return None
        if (len(addr.slots) == 0): 
            pure_streets = 0
            gsks = 0
            for s in streets: 
                if (s.ref_token is not None and s.ref_token_is_gsk): 
                    gsks += 1
                elif (s.ref_token is None): 
                    pure_streets += 1
            if ((pure_streets + gsks) == 0 and len(streets) > 0): 
                if (((len(details) > 0 or cross)) and geos is not None): 
                    pass
                else: 
                    addr = (None)
            elif (len(streets) < 2): 
                if ((len(streets) == 1 and geos is not None and len(geos) > 0) and ((streets[0].ref_token is None or streets[0].ref_token_is_gsk))): 
                    pass
                elif (len(details) > 0 and geos is not None and len(streets) == 0): 
                    pass
                else: 
                    addr = (None)
        if (addr is not None): 
            if (cross): 
                addr.detail = AddressDetailType.CROSS
            elif (len(details) > 0): 
                ty = AddressDetailType.UNDEFINED
                par = None
                for v in details: 
                    if ((isinstance(v.referent, StreetReferent)) and v.referent.kind == StreetKind.ORG): 
                        org0_ = Utils.asObjectOrNull(v.referent.get_slot_value(StreetReferent.ATTR_REF), Referent)
                        if (org0_ is not None and org0_.type_name == "ORGANIZATION"): 
                            addr.add_slot(AddressReferent.ATTR_DETAILREF, org0_, False, 0)
                            v.referent.move_ext_referent(addr, org0_)
                    elif (v.referent is not None): 
                        addr.add_slot(AddressReferent.ATTR_DETAILREF, v.referent, False, 0)
                        if (v.ref_token is not None): 
                            addr.add_ext_referent(v.ref_token)
                        gg = Utils.asObjectOrNull(v.referent, GeoReferent)
                        if (gg is not None and gg.higher is None and geos is not None): 
                            if (len(geos) > 0 and GeoOwnerHelper.can_be_higher(geos[0], gg, None, None)): 
                                gg.higher = geos[0]
                    if (ty == AddressDetailType.UNDEFINED or v.detail_meters > 0): 
                        if (v.detail_meters > 0): 
                            par = "{0}м".format(v.detail_meters)
                        ty = v.detail_type
                if (ty != AddressDetailType.UNDEFINED): 
                    addr.detail = ty
                if (par is not None): 
                    addr.add_slot(AddressReferent.ATTR_DETAILPARAM, par, False, 0)
                else: 
                    for v in li: 
                        if (v.tag is not None and v.detail_meters > 0): 
                            addr.add_slot(AddressReferent.ATTR_DETAILPARAM, "{0}м".format(v.detail_meters), False, 0)
                            break
        if (geos is None and len(streets) > 0 and not streets[0].is_street_road): 
            cou = 0
            tt = t0.previous
            while tt is not None and (cou < 200): 
                if (tt.is_newline_after): 
                    cou += 10
                r = tt.get_referent()
                if ((isinstance(r, GeoReferent)) and not r.is_state): 
                    geos = list()
                    geos.append(Utils.asObjectOrNull(r, GeoReferent))
                    break
                if (isinstance(r, StreetReferent)): 
                    ggg = r.geos
                    if (len(ggg) > 0): 
                        geos = list(ggg)
                        break
                if (isinstance(r, AddressReferent)): 
                    ggg = r.geos
                    if (len(ggg) > 0): 
                        geos = list(ggg)
                        break
                tt = tt.previous; cou += 1
        rt = None
        sr0 = None
        ii = 0
        while ii < len(streets): 
            s = streets[ii]
            sr = Utils.asObjectOrNull(s.referent, StreetReferent)
            if (geos is not None and sr is not None and len(sr.geos) == 0): 
                for gr in geos: 
                    if (gr.is_city or ((gr.higher is not None and gr.higher.is_city)) or ((gr.is_region and sr.kind != StreetKind.UNDEFINED))): 
                        sr.add_slot(StreetReferent.ATTR_GEO, gr, True, 0)
                        if (li[0].referent == gr): 
                            streets[0].begin_token = li[0].begin_token
                        jj = ii + 1
                        while jj < len(streets): 
                            if (isinstance(streets[jj].referent, StreetReferent)): 
                                streets[jj].referent.add_slot(StreetReferent.ATTR_GEO, gr, False, 0)
                            jj += 1
                        geos.remove(gr)
                        break
                    elif (gr.is_region): 
                        ok = False
                        if ((sr.kind == StreetKind.RAILWAY or sr.kind == StreetKind.ROAD or sr.kind == StreetKind.AREA) or sr.kind == StreetKind.SPEC): 
                            ok = True
                        else: 
                            for v in gr.typs: 
                                if (v == "муниципальный округ" or v == "городской округ"): 
                                    ok = True
                        if (ok): 
                            if (li[0].referent == gr): 
                                streets[0].begin_token = li[0].begin_token
                            sr.add_slot(StreetReferent.ATTR_GEO, gr, True, 0)
                            geos.remove(gr)
                            break
            is_reverce = False
            if (sr is not None and len(sr.geos) == 0): 
                if (sr0 is not None): 
                    for g in sr0.geos: 
                        sr.add_slot(StreetReferent.ATTR_GEO, g, False, 0)
                sr0 = sr
            if (s.referent is not None and s.referent.find_slot(StreetReferent.ATTR_NAME, "НЕТ", True) is not None): 
                for ss in s.referent.slots: 
                    if (ss.type_name == StreetReferent.ATTR_GEO): 
                        addr.add_referent(Utils.asObjectOrNull(ss.value, Referent))
            else: 
                if (sr is not None and ii > 0 and (isinstance(streets[ii - 1].referent, StreetReferent))): 
                    ki = streets[ii - 1].referent.kind
                    ok2 = False
                    if (ki != sr.kind or ki == StreetKind.AREA or ki == StreetKind.ORG): 
                        if ((sr.kind == StreetKind.AREA or ki == StreetKind.AREA or ki == StreetKind.RAILWAY) or ki == StreetKind.ROAD or ((ki == StreetKind.ORG and sr.kind == StreetKind.UNDEFINED))): 
                            ok2 = True
                    if (ki == StreetKind.ORG and streets[ii - 1].ref_token_is_massive): 
                        ok2 = True
                    if (ok2): 
                        if (sr.kind == StreetKind.AREA): 
                            if (ki == StreetKind.UNDEFINED): 
                                is_reverce = True
                            elif (ki == StreetKind.ORG and ((streets[ii].ref_token_is_massive or sr.find_slot(StreetReferent.ATTR_TYPE, "массив", True) is not None))): 
                                is_reverce = True
                        if (is_reverce): 
                            streets[ii - 1].end_token = streets[ii].end_token
                            streets[ii - 1].referent.higher = sr
                            streets[ii - 1].referent.add_slot(StreetReferent.ATTR_GEO, None, True, 0)
                        else: 
                            sr.higher = Utils.asObjectOrNull(streets[ii - 1].referent, StreetReferent)
                            sr.add_slot(StreetReferent.ATTR_GEO, None, True, 0)
                            if (addr is not None): 
                                slo = addr.find_slot(AddressReferent.ATTR_STREET, None, True)
                                if (slo is not None): 
                                    addr.slots.remove(slo)
                            s.begin_token = t0
                if (addr is not None): 
                    addr.move_ext_referent(s.referent, None)
                s.referent = ad.register_referent(s.referent)
                if (addr is not None and not is_reverce): 
                    addr.add_referent(s.referent)
                tt = s.begin_token.previous
                first_pass2747 = True
                while True:
                    if first_pass2747: first_pass2747 = False
                    else: tt = tt.previous
                    if (not (tt is not None and tt.begin_char >= t0.begin_char)): break
                    g = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                    if (g is None or sr is None): 
                        continue
                    for gg in sr.geos: 
                        if (gg.top_higher == g.top_higher): 
                            s.begin_token = tt
                rt = ReferentToken(s.referent, s.begin_token, s.end_token)
                t = (rt)
                t.kit.embed_token(rt)
                if (is_reverce and (isinstance(t.previous, ReferentToken))): 
                    rt = ReferentToken(t.previous.get_referent(), t.previous, t)
                    t.kit.embed_token(rt)
                    t = (rt)
                if (s.begin_char == t0.begin_char): 
                    t0 = (rt)
                if (s.end_char == t1.end_char): 
                    t1 = (rt)
            ii += 1
        if (addr is not None): 
            ok = False
            for s in addr.slots: 
                if (s.type_name != AddressReferent.ATTR_DETAIL): 
                    ok = True
            if (not ok): 
                addr = (None)
        if (addr is None): 
            return t
        if (geos is not None and len(geos) > 0): 
            if ((len(geos) == 1 and geos[0].is_region and len(streets) == 1) and streets[0].ref_token is not None): 
                pass
            if (len(streets) == 1 and streets[0].referent is not None): 
                for s in streets[0].referent.slots: 
                    if (s.type_name == StreetReferent.ATTR_GEO and (isinstance(s.value, GeoReferent))): 
                        k = 0
                        gg = Utils.asObjectOrNull(s.value, GeoReferent)
                        while gg is not None and (k < 5): 
                            for ii in range(len(geos) - 1, -1, -1):
                                if (geos[ii] == gg): 
                                    del geos[ii]
                                    break
                            gg = (Utils.asObjectOrNull(gg.parent_referent, GeoReferent)); k += 1
            while len(geos) >= 2:
                if (geos[1].higher is None and GeoOwnerHelper.can_be_higher(geos[0], geos[1], None, None)): 
                    geos[1].higher = geos[0]
                    del geos[0]
                elif (geos[0].higher is None and GeoOwnerHelper.can_be_higher(geos[1], geos[0], None, None)): 
                    geos[0].higher = geos[1]
                    del geos[1]
                elif (geos[1].higher is not None and geos[1].higher.higher is None and GeoOwnerHelper.can_be_higher(geos[0], geos[1].higher, None, None)): 
                    geos[1].higher.higher = geos[0]
                    del geos[0]
                elif (geos[0].higher is not None and geos[0].higher.higher is None and GeoOwnerHelper.can_be_higher(geos[1], geos[0].higher, None, None)): 
                    geos[0].higher.higher = geos[1]
                    del geos[1]
                else: 
                    break
            for g in geos: 
                addr.add_referent(g)
        ok1 = False
        for s in addr.slots: 
            if (s.type_name != AddressReferent.ATTR_STREET): 
                ok1 = True
                break
        if (not ok1): 
            return t
        if (addr.house is not None and addr.corpus is None and addr.find_slot(AddressReferent.ATTR_STREET, None, True) is None): 
            if (geos is not None and len(geos) > 0 and geos[0].find_slot(GeoReferent.ATTR_NAME, "ЗЕЛЕНОГРАД", True) is not None): 
                addr.corpus = addr.house
                addr.house = None
        rt = ReferentToken(ad.register_referent(addr), t0, t1)
        t.kit.embed_token(rt)
        t = (rt)
        if ((t.next0_ is not None and ((t.next0_.is_comma or t.next0_.is_char(';'))) and (t.next0_.whitespaces_after_count < 2)) and (isinstance(t.next0_.next0_, NumberToken))): 
            last = None
            for ll in li: 
                if (ll.tag is not None): 
                    last = ll
            attr_name = None
            if (last is None): 
                return t
            if (last.typ == AddressItemType.HOUSE): 
                attr_name = AddressReferent.ATTR_HOUSE
            elif (last.typ == AddressItemType.CORPUS): 
                attr_name = AddressReferent.ATTR_CORPUS
            elif (last.typ == AddressItemType.BUILDING): 
                attr_name = AddressReferent.ATTR_BUILDING
            elif (last.typ == AddressItemType.FLAT): 
                attr_name = AddressReferent.ATTR_FLAT
            elif (last.typ == AddressItemType.PAVILION): 
                attr_name = AddressReferent.ATTR_PAVILION
            elif (last.typ == AddressItemType.PLOT): 
                attr_name = AddressReferent.ATTR_PLOT
            elif (last.typ == AddressItemType.FIELD): 
                attr_name = AddressReferent.ATTR_FIELD
            elif (last.typ == AddressItemType.BOX): 
                attr_name = AddressReferent.ATTR_BOX
            elif (last.typ == AddressItemType.POTCH): 
                attr_name = AddressReferent.ATTR_PORCH
            elif (last.typ == AddressItemType.BLOCK): 
                attr_name = AddressReferent.ATTR_BLOCK
            elif (last.typ == AddressItemType.OFFICE): 
                attr_name = AddressReferent.ATTR_OFFICE
            elif (last.typ == AddressItemType.ROOM): 
                attr_name = AddressReferent.ATTR_ROOM
            if (attr_name is not None): 
                t = t.next0_.next0_
                while t is not None: 
                    if (not (isinstance(t, NumberToken))): 
                        break
                    addr1 = Utils.asObjectOrNull(addr.clone(), AddressReferent)
                    addr1.occurrence.clear()
                    addr1.add_slot(attr_name, str(t.value), True, 0)
                    rt = ReferentToken(ad.register_referent(addr1), t, t)
                    t.kit.embed_token(rt)
                    t = (rt)
                    if ((t.next0_ is not None and ((t.next0_.is_comma or t.next0_.is_char(';'))) and (t.next0_.whitespaces_after_count < 2)) and (isinstance(t.next0_.next0_, NumberToken))): 
                        pass
                    else: 
                        break
                    t = t.next0_
        return t