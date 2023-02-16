# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import Stopwatch

from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.geo.internal.GeoOwnerHelper import GeoOwnerHelper
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.address.internal.MetaAddress import MetaAddress
from pullenti.ner.address.internal.MetaStreet import MetaStreet
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.geo.internal.MetaGeo import MetaGeo
from pullenti.ner.geo.internal.GeoAnalyzerData import GeoAnalyzerData
from pullenti.ner.core.internal.PullentiNerCoreInternalResourceHelper import PullentiNerCoreInternalResourceHelper
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.ner.Token import Token
from pullenti.ner.TextToken import TextToken
from pullenti.ner.Referent import Referent
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken

class GeoAnalyzer(Analyzer):
    """ Анализатор географических объектов (стран, регионов, населённых пунктов) """
    
    ANALYZER_NAME = "GEO"
    """ Имя анализатора ("GEO") """
    
    @property
    def name(self) -> str:
        return GeoAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Страны, регионы, города"
    
    def clone(self) -> 'Analyzer':
        return GeoAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaGeo._global_meta]
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["PHONE"]
    
    @staticmethod
    def _get_data(t : 'Token') -> 'GeoAnalyzerData':
        if (t is None): 
            return None
        return Utils.asObjectOrNull(t.kit.get_analyzer_data_by_analyzer_name(GeoAnalyzer.ANALYZER_NAME), GeoAnalyzerData)
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaGeo.COUNTRY_CITY_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("countrycity.png")
        res[MetaGeo.COUNTRY_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("country.png")
        res[MetaGeo.CITY_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("city.png")
        res[MetaGeo.DISTRICT_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("district.png")
        res[MetaGeo.REGION_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("region.png")
        res[MetaGeo.UNION_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("union.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == GeoReferent.OBJ_TYPENAME): 
            return GeoReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 15
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        return GeoAnalyzerData()
    
    def process(self, kit : 'AnalysisKit') -> None:
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        from pullenti.ner.geo.internal.CityAttachHelper import CityAttachHelper
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        from pullenti.ner.geo.internal.OrgTypToken import OrgTypToken
        from pullenti.ner.geo.internal.TerrDefineHelper import TerrDefineHelper
        ad = Utils.asObjectOrNull(kit.get_analyzer_data(self), GeoAnalyzerData)
        t = kit.first_token
        while t is not None: 
            t.inner_bool = False
            t = t.next0_
        sw = Stopwatch()
        sw.reset()
        sw.start()
        MiscLocationHelper._prepare_all_data(kit.first_token)
        sw.stop()
        kit.msgs.append("Npt: {0}ms".format(sw.elapsedMilliseconds))
        if (not self._on_progress(10, 100, kit)): 
            return
        sw.reset()
        sw.start()
        AddressItemToken.SPEED_REGIME = True
        AddressItemToken._prepare_all_data(kit.first_token)
        sw.stop()
        kit.msgs.append("AddressItemToken: {0}ms".format(sw.elapsedMilliseconds))
        if (not self._on_progress(20, 100, kit)): 
            return
        sw.reset()
        sw.start()
        OrgTypToken.SPEED_REGIME = True
        OrgTypToken._prepare_all_data(kit.first_token)
        sw.stop()
        kit.msgs.append("OrgTypToken: {0}ms".format(sw.elapsedMilliseconds))
        if (not self._on_progress(30, 100, kit)): 
            return
        sw.reset()
        sw.start()
        OrgItemToken.SPEED_REGIME = True
        OrgItemToken._prepare_all_data(kit.first_token)
        sw.stop()
        kit.msgs.append("OrgItemToken: {0}ms".format(sw.elapsedMilliseconds))
        if (not self._on_progress(40, 100, kit)): 
            return
        sw.reset()
        sw.start()
        StreetItemToken.SPEED_REGIME = True
        StreetItemToken._prepare_all_data(kit.first_token)
        sw.stop()
        kit.msgs.append("StreetItemToken: {0}ms".format(sw.elapsedMilliseconds))
        if (not self._on_progress(60, 100, kit)): 
            return
        sw.reset()
        sw.start()
        TerrItemToken.SPEED_REGIME = True
        TerrItemToken._prepare_all_data(kit.first_token)
        sw.stop()
        kit.msgs.append("TerrItemToken: {0}ms".format(sw.elapsedMilliseconds))
        if (not self._on_progress(65, 100, kit)): 
            return
        sw.reset()
        sw.start()
        CityItemToken.SPEED_REGIME = True
        CityItemToken._prepare_all_data(kit.first_token)
        sw.stop()
        kit.msgs.append("CityItemToken: {0}ms".format(sw.elapsedMilliseconds))
        if (not self._on_progress(85, 100, kit)): 
            return
        sw.reset()
        sw.start()
        non_registered = list()
        for step in range(2):
            ad.step = step
            t = kit.first_token
            first_pass2894 = True
            while True:
                if first_pass2894: first_pass2894 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_ignored): 
                    continue
                if (len(ad.referents) >= 2000): 
                    break
                if (step > 0 and (isinstance(t, ReferentToken))): 
                    geo_ = Utils.asObjectOrNull(t.get_referent(), GeoReferent)
                    if (((geo_ is not None and t.next0_ is not None and t.next0_.is_char('(')) and t.next0_.next0_ is not None and geo_.can_be_equals(t.next0_.next0_.get_referent(), ReferentsEqualType.WITHINONETEXT)) and t.next0_.next0_.next0_ is not None and t.next0_.next0_.next0_.is_char(')')): 
                        rt0 = ReferentToken._new956(geo_, t, t.next0_.next0_.next0_, t.morph)
                        kit.embed_token(rt0)
                        t = (rt0)
                        continue
                    if ((geo_ is not None and t.next0_ is not None and t.next0_.is_hiphen) and t.next0_.next0_ is not None and geo_.can_be_equals(t.next0_.next0_.get_referent(), ReferentsEqualType.WITHINONETEXT)): 
                        rt0 = ReferentToken._new956(geo_, t, t.next0_.next0_, t.morph)
                        kit.embed_token(rt0)
                        t = (rt0)
                        continue
                ok = False
                if (step == 0 or t.inner_bool): 
                    ok = True
                elif ((isinstance(t, TextToken)) and t.chars.is_letter and not t.chars.is_all_lower): 
                    ok = True
                cli = None
                if (ok): 
                    cli = TerrItemToken.try_parse_list(t, 5, ad)
                if (cli is None): 
                    continue
                t.inner_bool = True
                rt = TerrDefineHelper.try_define(cli, ad, False, None, non_registered)
                if ((rt is None and len(cli) == 1 and cli[0].is_adjective) and cli[0].onto_item is not None): 
                    tt = cli[0].end_token.next0_
                    if (tt is not None): 
                        if (tt.is_char(',')): 
                            tt = tt.next0_
                        elif (tt.morph.class0_.is_conjunction): 
                            tt = tt.next0_
                            if (tt is not None and tt.morph.class0_.is_conjunction): 
                                tt = tt.next0_
                        cli1 = TerrItemToken.try_parse_list(tt, 2, None)
                        if (cli1 is not None and cli1[0].onto_item is not None): 
                            g0 = Utils.asObjectOrNull(cli[0].onto_item.referent, GeoReferent)
                            g1 = Utils.asObjectOrNull(cli1[0].onto_item.referent, GeoReferent)
                            if ((g0 is not None and g1 is not None and g0.is_region) and g1.is_region): 
                                if (g0.is_city == g1.is_city or g0.is_region == g1.is_region or g0.is_state == g1.is_state): 
                                    rt = TerrDefineHelper.try_define(cli, ad, True, None, None)
                        if (rt is None and cli[0].onto_item.referent.is_state): 
                            if ((rt is None and tt is not None and (isinstance(tt.get_referent(), GeoReferent))) and tt.whitespaces_before_count == 1): 
                                geo2 = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                                if (GeoOwnerHelper.can_be_higher(Utils.asObjectOrNull(cli[0].onto_item.referent, GeoReferent), geo2, None, None)): 
                                    cl = cli[0].onto_item.referent.clone()
                                    cl.occurrence.clear()
                                    rt = ReferentToken._new956(cl, cli[0].begin_token, cli[0].end_token, cli[0].morph)
                            if (rt is None and step == 0): 
                                npt = MiscLocationHelper._try_parse_npt(cli[0].begin_token)
                                if (npt is not None and npt.end_char >= tt.begin_char): 
                                    cits = CityItemToken.try_parse_list(tt, 5, ad)
                                    rt1 = (None if cits is None else CityAttachHelper.try_define(cits, ad, False))
                                    if (rt1 is not None): 
                                        rt1.referent = ad.register_referent(rt1.referent)
                                        kit.embed_token(rt1)
                                        cl = cli[0].onto_item.referent.clone()
                                        cl.occurrence.clear()
                                        rt = ReferentToken._new956(cl, cli[0].begin_token, cli[0].end_token, cli[0].morph)
                if (rt is None): 
                    cits = self.__try_parse_city_list_back(t.previous)
                    if (cits is not None): 
                        rt = TerrDefineHelper.try_define(cli, ad, False, cits, None)
                if (rt is None and len(cli) == 2): 
                    te = cli[len(cli) - 1].end_token.next0_
                    if (te is not None): 
                        if (te.morph.class0_.is_preposition or te.is_char(',')): 
                            te = te.next0_
                    li = AddressItemToken.try_parse_list(te, 2)
                    if (li is not None and len(li) > 0): 
                        if (li[0].typ == AddressItemType.STREET or li[0].typ == AddressItemType.KILOMETER or li[0].typ == AddressItemType.HOUSE): 
                            ad0 = StreetItemToken.try_parse(cli[0].begin_token.previous, None, False, None)
                            if (ad0 is not None and ad0.typ == StreetItemType.NOUN): 
                                pass
                            elif (not cli[0].is_adjective): 
                                rt = TerrDefineHelper.try_define(cli, ad, True, None, None)
                            else: 
                                aaa = AddressItemToken.try_parse(cli[0].begin_token, False, None, None)
                                if (aaa is not None and aaa.typ == AddressItemType.STREET): 
                                    pass
                                else: 
                                    rt = TerrDefineHelper.try_define(cli, ad, True, None, None)
                if ((rt is None and len(cli) > 2 and cli[0].termin_item is None) and cli[1].termin_item is None and cli[2].termin_item is not None): 
                    cit = CityItemToken.try_parse_back(cli[0].begin_token.previous, False)
                    if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN): 
                        if (((len(cli) > 4 and cli[1].termin_item is None and cli[2].termin_item is not None) and cli[3].termin_item is None and cli[4].termin_item is not None) and cli[2].termin_item.canonic_text.endswith(cli[4].termin_item.canonic_text)): 
                            pass
                        else: 
                            del cli[0]
                            rt = TerrDefineHelper.try_define(cli, ad, True, None, None)
                if (rt is not None): 
                    if (MiscLocationHelper.check_territory(rt.begin_token.previous) is not None): 
                        if (not rt.begin_token.previous.is_value("ГРАНИЦА", None)): 
                            rt.begin_token = rt.begin_token.previous
                    geo_ = Utils.asObjectOrNull(rt.referent, GeoReferent)
                    if (not geo_.is_city and not geo_.is_state and geo_.find_slot(GeoReferent.ATTR_TYPE, "республика", True) is None): 
                        non_registered.append(geo_)
                    else: 
                        rt.referent = ad.register_referent(geo_)
                    kit.embed_token(rt)
                    t = (rt)
                    if (step == 0): 
                        tt = t
                        while True:
                            rr = self.__try_attach_territory_before_city(tt, ad)
                            if (rr is None): 
                                break
                            geo_ = (Utils.asObjectOrNull(rr.referent, GeoReferent))
                            if (not geo_.is_city and not geo_.is_state): 
                                non_registered.append(geo_)
                            else: 
                                rr.referent = ad.register_referent(geo_)
                            kit.embed_token(rr)
                            tt = (rr)
                        if (t.next0_ is not None and ((t.next0_.is_comma or t.next0_.is_char('(')))): 
                            rt1 = TerrDefineHelper.try_attach_stateusaterritory(t.next0_.next0_)
                            if (rt1 is not None): 
                                rt1.referent = ad.register_referent(rt1.referent)
                                kit.embed_token(rt1)
                                t = (rt1)
                    continue
        t = kit.first_token
        first_pass2895 = True
        while True:
            if first_pass2895: first_pass2895 = False
            else: t = (None if t is None else t.next0_)
            if (not (t is not None)): break
            if (t.is_ignored): 
                continue
            g = Utils.asObjectOrNull(t.get_referent(), GeoReferent)
            if (g is None): 
                continue
            if (not (isinstance(t.previous, TextToken))): 
                continue
            t0 = None
            if (t.previous.is_value("СОЮЗ", None)): 
                t0 = t.previous
            elif (t.previous.is_value("ГОСУДАРСТВО", None) and t.previous.previous is not None and t.previous.previous.is_value("СОЮЗНЫЙ", None)): 
                t0 = t.previous.previous
            if (t0 is None): 
                continue
            npt = MiscLocationHelper._try_parse_npt(t0.previous)
            if (npt is not None and npt.end_token == t.previous): 
                t0 = t0.previous
            uni = GeoReferent()
            typ = MiscHelper.get_text_value(t0, t.previous, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
            if (typ is None): 
                continue
            uni._add_typ_union(t0.kit.base_language)
            uni._add_typ(typ.lower())
            uni.add_slot(GeoReferent.ATTR_REF, g, False, 0)
            t1 = t
            i = 1
            t = t.next0_
            first_pass2896 = True
            while True:
                if first_pass2896: first_pass2896 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_comma_and): 
                    continue
                g = Utils.asObjectOrNull(t.get_referent(), GeoReferent)
                if ((g) is None): 
                    break
                if (uni.find_slot(GeoReferent.ATTR_REF, g, True) is not None): 
                    break
                if (t.is_newline_before): 
                    break
                t1 = t
                uni.add_slot(GeoReferent.ATTR_REF, g, False, 0)
                i += 1
            if (i < 2): 
                continue
            uni = (Utils.asObjectOrNull(ad.register_referent(uni), GeoReferent))
            rt = ReferentToken(uni, t0, t1)
            kit.embed_token(rt)
            t = (rt)
        sw.stop()
        kit.msgs.append("Territories: {0}ms".format(sw.elapsedMilliseconds))
        if (not self._on_progress(90, 100, kit)): 
            return
        sw.reset()
        sw.start()
        new_cities = False
        is_city_before = False
        t = kit.first_token
        first_pass2897 = True
        while True:
            if first_pass2897: first_pass2897 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_ignored): 
                continue
            if (t.is_char_of(".,")): 
                continue
            li = None
            li = CityItemToken.try_parse_list(t, 5, ad)
            rt = None
            if (li is not None): 
                rt = CityAttachHelper.try_define(li, ad, False)
                if ((rt) is not None): 
                    tt = t.previous
                    if (tt is not None and tt.is_comma): 
                        tt = tt.previous
                    if (tt is not None and (isinstance(tt.get_referent(), GeoReferent))): 
                        if (tt.get_referent().can_be_equals(rt.referent, ReferentsEqualType.WITHINONETEXT)): 
                            rt.begin_token = tt
                            rt.referent = ad.register_referent(rt.referent)
                            kit.embed_token(rt)
                            t = (rt)
                            continue
                    if (len(ad.referents) > 2000): 
                        break
                    if (len(li) == 2 and li[0].orto_city is not None): 
                        li[0].orto_city.referent = ad.register_referent(li[0].orto_city.referent)
                        rt1 = ReferentToken(li[0].orto_city.referent, li[0].begin_token, li[1].begin_token.previous)
                        kit.embed_token(rt1)
                        rt.begin_token = li[1].begin_token
                        rt.end_token = li[1].end_token
                    rt.referent = (Utils.asObjectOrNull(ad.register_referent(rt.referent), GeoReferent))
                    kit.embed_token(rt)
                    t = (rt)
                    is_city_before = True
                    new_cities = True
                    tt = t
                    while True:
                        rr = self.__try_attach_territory_before_city(tt, ad)
                        if (rr is None): 
                            break
                        geo_ = Utils.asObjectOrNull(rr.referent, GeoReferent)
                        if (not geo_.is_city and not geo_.is_state): 
                            non_registered.append(geo_)
                        else: 
                            rr.referent = ad.register_referent(geo_)
                        kit.embed_token(rr)
                        tt = (rr)
                    rt = self.__try_attach_territory_after_city(t, ad)
                    if (rt is not None): 
                        rt.referent = ad.register_referent(rt.referent)
                        kit.embed_token(rt)
                        t = (rt)
                    continue
            if (not t.inner_bool): 
                is_city_before = False
                continue
            if (not is_city_before): 
                continue
            tts = TerrItemToken.try_parse_list(t, 5, None)
            if (tts is not None and len(tts) > 1 and ((tts[0].termin_item is not None or tts[1].termin_item is not None))): 
                rt = TerrDefineHelper.try_define(tts, ad, True, None, None)
                if ((rt) is not None): 
                    geo_ = Utils.asObjectOrNull(rt.referent, GeoReferent)
                    if (not geo_.is_city and not geo_.is_state): 
                        non_registered.append(geo_)
                    else: 
                        rt.referent = ad.register_referent(geo_)
                    kit.embed_token(rt)
                    t = (rt)
                    continue
            is_city_before = False
        sw.stop()
        kit.msgs.append("Cities: {0}ms".format(sw.elapsedMilliseconds))
        sw.reset()
        sw.start()
        if (new_cities and len(ad.local_ontology.items) > 0): 
            t = kit.first_token
            first_pass2898 = True
            while True:
                if first_pass2898: first_pass2898 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_ignored): 
                    continue
                if (not (isinstance(t, TextToken))): 
                    continue
                if (t.chars.is_all_lower): 
                    continue
                li = ad.local_ontology.try_attach(t, None, False)
                if (li is None): 
                    continue
                mc = t.get_morph_class_in_dictionary()
                if (mc.is_proper_surname or mc.is_proper_name or mc.is_proper_secname): 
                    continue
                if (t.morph.class0_.is_adjective): 
                    continue
                geo_ = Utils.asObjectOrNull(li[0].item.referent, GeoReferent)
                if (geo_ is not None): 
                    geo_ = (Utils.asObjectOrNull(geo_.clone(), GeoReferent))
                    geo_.occurrence.clear()
                    rt = ReferentToken._new956(geo_, li[0].begin_token, li[0].end_token, t.morph)
                    if (rt.begin_token == rt.end_token): 
                        geo_._add_name(t.term)
                    if (rt.begin_token.previous is not None and rt.begin_token.previous.is_value("СЕЛО", None) and geo_.is_city): 
                        rt.begin_token = rt.begin_token.previous
                        rt.morph = rt.begin_token.morph
                        geo_.add_slot(GeoReferent.ATTR_TYPE, "село", True, 0)
                    kit.embed_token(rt)
                    t = li[0].end_token
        go_back = False
        t = kit.first_token
        first_pass2899 = True
        while True:
            if first_pass2899: first_pass2899 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_ignored): 
                continue
            if (go_back): 
                go_back = False
                if (t.previous is not None): 
                    t = t.previous
            geo_ = Utils.asObjectOrNull(t.get_referent(), GeoReferent)
            if (geo_ is None): 
                continue
            geo1 = None
            tt = t.next0_
            bra = False
            comma1 = False
            comma2 = False
            inp = False
            adj = False
            first_pass2900 = True
            while True:
                if first_pass2900: first_pass2900 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_char_of(",")): 
                    comma1 = True
                    continue
                if (tt.is_value("IN", None) or tt.is_value("В", None)): 
                    inp = True
                    continue
                if (MiscHelper.is_eng_adj_suffix(tt)): 
                    adj = True
                    tt = tt.next0_
                    continue
                det = AddressItemToken.try_parse_pure_item(tt, None, ad)
                if (det is not None and det.typ == AddressItemType.DETAIL): 
                    tt = det.end_token
                    comma1 = True
                    continue
                if (tt.morph.class0_.is_preposition): 
                    continue
                if (tt.is_char('(') and tt == t.next0_): 
                    bra = True
                    continue
                if ((isinstance(tt, TextToken)) and BracketHelper.is_bracket(tt, True)): 
                    continue
                geo1 = (Utils.asObjectOrNull(tt.get_referent(), GeoReferent))
                break
            if (geo1 is None): 
                continue
            if (tt.whitespaces_before_count > 15): 
                continue
            ttt = tt.next0_
            geo2 = None
            first_pass2901 = True
            while True:
                if first_pass2901: first_pass2901 = False
                else: ttt = ttt.next0_
                if (not (ttt is not None)): break
                if (ttt.is_comma_and): 
                    comma2 = True
                    continue
                det = AddressItemToken.try_parse_pure_item(ttt, None, ad)
                if (det is not None and det.typ == AddressItemType.DETAIL): 
                    ttt = det.end_token
                    comma2 = True
                    continue
                if (ttt.morph.class0_.is_preposition): 
                    continue
                geo2 = (Utils.asObjectOrNull(ttt.get_referent(), GeoReferent))
                break
            if (ttt is not None and ttt.whitespaces_before_count > 15): 
                geo2 = (None)
            if (geo2 is not None): 
                if ((comma1 and comma2 and GeoOwnerHelper._can_be_higher_token(t, tt)) and GeoOwnerHelper._can_be_higher_token(tt, ttt)): 
                    geo2.higher = geo1
                    geo1.higher = geo_
                    rt0 = ReferentToken._new956(geo1, t, tt, tt.morph)
                    kit.embed_token(rt0)
                    rt = ReferentToken._new956(geo2, rt0, ttt, ttt.morph)
                    kit.embed_token(rt)
                    t = (rt)
                    go_back = True
                    continue
                elif (GeoOwnerHelper._can_be_higher_token(ttt, tt)): 
                    if (GeoOwnerHelper._can_be_higher_token(t, ttt)): 
                        if (geo2.find_slot(GeoReferent.ATTR_TYPE, "город", True) is not None and geo1.find_slot(GeoReferent.ATTR_TYPE, "район", True) is not None and geo_.is_region): 
                            geo2.higher = geo1
                            geo1.higher = geo_
                            rt0 = ReferentToken._new956(geo1, t, tt, tt.morph)
                            kit.embed_token(rt0)
                            rt = ReferentToken._new956(geo2, rt0, ttt, ttt.morph)
                            kit.embed_token(rt)
                            t = (rt)
                            go_back = True
                            continue
                        else: 
                            geo2.higher = geo_
                            geo1.higher = geo2
                            rt = ReferentToken._new956(geo1, t, ttt, tt.morph)
                            kit.embed_token(rt)
                            t = (rt)
                            go_back = True
                            continue
                    if (GeoOwnerHelper._can_be_higher_token(ttt, t) and GeoOwnerHelper._can_be_higher_token(t, tt)): 
                        if (ttt.is_newline_before): 
                            ttt = tt
                        else: 
                            geo_.higher = geo2
                        geo1.higher = geo_
                        rt = ReferentToken._new956(geo1, t, ttt, tt.morph)
                        kit.embed_token(rt)
                        t = (rt)
                        go_back = True
                        continue
                    if (GeoOwnerHelper._can_be_higher_token(tt, t)): 
                        geo_.higher = geo1
                        geo1.higher = geo2
                        rt0 = ReferentToken._new956(geo1, tt, ttt, tt.morph)
                        kit.embed_token(rt0)
                        rt = ReferentToken._new956(geo_, t, rt0, t.morph)
                        kit.embed_token(rt)
                        t = (rt)
                        go_back = True
                        continue
                    if (GeoOwnerHelper._can_be_higher_token(t, tt) and GeoOwnerHelper._can_be_higher_token(ttt, tt)): 
                        if (geo1.find_slot(GeoReferent.ATTR_TYPE, "муниципальный округ", True) is not None and geo_.find_slot(GeoReferent.ATTR_TYPE, "город", True) is not None and geo2.find_slot(GeoReferent.ATTR_TYPE, "город", True) is not None): 
                            if (geo2.find_slot(GeoReferent.ATTR_NAME, "МОСКВА", True) is not None): 
                                geo_.higher = geo1
                                geo1.higher = geo2
                                rt0 = ReferentToken._new956(geo1, tt, ttt, tt.morph)
                                kit.embed_token(rt0)
                                rt = ReferentToken._new956(geo_, t, rt0, t.morph)
                                kit.embed_token(rt)
                                t = (rt)
                                go_back = True
                                continue
                            else: 
                                geo2.higher = geo1
                                geo1.higher = geo_
                                rt0 = ReferentToken._new956(geo1, t, tt, tt.morph)
                                kit.embed_token(rt0)
                                rt = ReferentToken._new956(geo2, rt0, ttt, ttt.morph)
                                kit.embed_token(rt)
                                t = (rt)
                                go_back = True
                                continue
                if (comma2): 
                    continue
            if (GeoOwnerHelper._can_be_higher_token(t, tt) and ((not GeoOwnerHelper._can_be_higher_token(tt, t) or adj))): 
                geo1.higher = geo_
                rt = ReferentToken._new956(geo1, t, tt, tt.morph)
                if ((geo1.is_city and not geo_.is_city and t.previous is not None) and t.previous.is_value("СТОЛИЦА", "СТОЛИЦЯ")): 
                    rt.begin_token = t.previous
                    rt.morph = t.previous.morph
                kit.embed_token(rt)
                t = (rt)
                go_back = True
                continue
            if (GeoOwnerHelper._can_be_higher_token(tt, t) and ((not GeoOwnerHelper._can_be_higher_token(t, tt) or inp))): 
                if (geo_.higher is None): 
                    geo_.higher = geo1
                elif (geo1.higher is None and GeoOwnerHelper.can_be_higher(geo_.higher, geo1, None, None) and not GeoOwnerHelper.can_be_higher(geo1, geo_.higher, None, None)): 
                    geo1.higher = geo_.higher
                    geo_.higher = geo1
                else: 
                    geo_.higher = geo1
                if (bra and tt.next0_ is not None and tt.next0_.is_char(')')): 
                    tt = tt.next0_
                rt = ReferentToken._new956(geo_, t, tt, t.morph)
                kit.embed_token(rt)
                t = (rt)
                go_back = True
                continue
            if ((not tt.morph.class0_.is_adjective and not t.morph.class0_.is_adjective and tt.chars.is_cyrillic_letter) and t.chars.is_cyrillic_letter and not tt.morph.case_.is_instrumental): 
                geo0 = geo_
                while geo0 is not None: 
                    if (GeoOwnerHelper.can_be_higher(geo1, geo0, None, None)): 
                        geo0.higher = geo1
                        rt = ReferentToken._new956(geo_, t, tt, t.morph)
                        kit.embed_token(rt)
                        t = (rt)
                        go_back = True
                        break
                    geo0 = geo0.higher
        cities_settls = dict()
        cities_settls2 = dict()
        for v in ad.local_ontology.items: 
            g = Utils.asObjectOrNull(v.referent, GeoReferent)
            if (g is None or not g.is_city): 
                continue
            if (g.find_slot(GeoReferent.ATTR_TYPE, "городское поселение", True) is not None): 
                for n in g.get_string_values(GeoReferent.ATTR_NAME): 
                    if (not n in cities_settls): 
                        cities_settls[n] = g
        for g in non_registered: 
            if (not g.is_region): 
                continue
            if (g.find_slot(GeoReferent.ATTR_TYPE, "городской округ", True) is None): 
                continue
            for n in g.get_string_values(GeoReferent.ATTR_NAME): 
                if (not n in cities_settls2): 
                    cities_settls2[n] = g
        for v in ad.local_ontology.items: 
            g = Utils.asObjectOrNull(v.referent, GeoReferent)
            if (g is None or not g.is_city): 
                continue
            if (g.higher is not None): 
                continue
            if (g.find_slot(GeoReferent.ATTR_TYPE, "город", True) is None): 
                continue
            for n in g.get_string_values(GeoReferent.ATTR_NAME): 
                if (n in cities_settls): 
                    g.higher = cities_settls[n]
                    break
                elif (n in cities_settls2): 
                    g.higher = cities_settls2[n]
                    break
        k = 0
        while k < len(non_registered): 
            ch = False
            i = 0
            while i < (len(non_registered) - 1): 
                if (GeoAnalyzer.__geo_comp(non_registered[i], non_registered[i + 1]) > 0): 
                    ch = True
                    v = non_registered[i]
                    non_registered[i] = non_registered[i + 1]
                    non_registered[i + 1] = v
                i += 1
            if (not ch): 
                break
            k += 1
        for g in non_registered: 
            g.tag = None
        for ng in non_registered: 
            for s in ng.slots: 
                if (isinstance(s.value, GeoReferent)): 
                    if (isinstance(s.value.tag, GeoReferent)): 
                        ng.upload_slot(s, Utils.asObjectOrNull(s.value.tag, GeoReferent))
            rg = Utils.asObjectOrNull(ad.register_referent(ng), GeoReferent)
            if (rg == ng): 
                continue
            ng.tag = (rg)
            for oc in ng.occurrence: 
                oc.occurence_of = rg
                rg.add_occurence(oc)
        if (len(non_registered) > 0): 
            t = kit.first_token
            first_pass2902 = True
            while True:
                if first_pass2902: first_pass2902 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_ignored): 
                    continue
                geo_ = Utils.asObjectOrNull(t.get_referent(), GeoReferent)
                if (geo_ is None): 
                    continue
                GeoAnalyzer.__replace_terrs(Utils.asObjectOrNull(t, ReferentToken))
        ad.oregime = False
        ad.otregime = False
        ad.tregime = False
        ad.cregime = False
        ad.sregime = False
        ad.aregime = False
        sw.stop()
        kit.msgs.append("GeoMisc: {0}ms".format(sw.elapsedMilliseconds))
        if (not self._on_progress(100, 100, kit)): 
            return
    
    @staticmethod
    def __replace_terrs(mt : 'ReferentToken') -> None:
        if (mt is None): 
            return
        geo_ = Utils.asObjectOrNull(mt.referent, GeoReferent)
        if (geo_ is not None and (isinstance(geo_.tag, GeoReferent))): 
            mt.referent = (Utils.asObjectOrNull(geo_.tag, GeoReferent))
        if (geo_ is not None): 
            for s in geo_.slots: 
                if (isinstance(s.value, GeoReferent)): 
                    g = Utils.asObjectOrNull(s.value, GeoReferent)
                    if (isinstance(g.tag, GeoReferent)): 
                        geo_.upload_slot(s, g.tag)
        t = mt.begin_token
        while t is not None: 
            if (t.end_char > mt.end_token.end_char): 
                break
            else: 
                if (isinstance(t, ReferentToken)): 
                    GeoAnalyzer.__replace_terrs(Utils.asObjectOrNull(t, ReferentToken))
                if (t == mt.end_token): 
                    break
            t = t.next0_
    
    @staticmethod
    def __geo_comp(x : 'GeoReferent', y : 'GeoReferent') -> int:
        xcou = 0
        g = x.higher
        while g is not None: 
            xcou += 1
            g = g.higher
        ycou = 0
        g = y.higher
        while g is not None: 
            ycou += 1
            g = g.higher
        if (xcou < ycou): 
            return -1
        if (xcou > ycou): 
            return 1
        return Utils.compareStrings(x.to_string_ex(True, MorphLang.UNKNOWN, 0), y.to_string_ex(True, MorphLang.UNKNOWN, 0), False)
    
    def __try_parse_city_list_back(self, t : 'Token') -> typing.List['CityItemToken']:
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        if (t is None): 
            return None
        while t is not None and ((t.morph.class0_.is_preposition or t.is_char_of(",.") or t.morph.class0_.is_conjunction)):
            t = t.previous
        if (t is None): 
            return None
        res = None
        tt = t
        while tt is not None: 
            if (not (isinstance(tt, TextToken))): 
                break
            if (tt.previous is not None and tt.previous.is_hiphen and (isinstance(tt.previous.previous, TextToken))): 
                if (not tt.is_whitespace_before and not tt.previous.is_whitespace_before): 
                    tt = tt.previous.previous
            ci = CityItemToken.try_parse_list(tt, 5, None)
            if (ci is None and tt.previous is not None): 
                ci = CityItemToken.try_parse_list(tt.previous, 5, None)
            if (ci is None): 
                break
            if (ci[len(ci) - 1].end_token == t): 
                res = ci
            tt = tt.previous
        if (res is not None): 
            res.reverse()
        return res
    
    def __try_attach_territory_before_city(self, t : 'Token', ad : 'AnalyzerDataWithOntology') -> 'ReferentToken':
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        from pullenti.ner.geo.internal.TerrDefineHelper import TerrDefineHelper
        if (isinstance(t, ReferentToken)): 
            t = t.previous
        while t is not None: 
            if (not t.is_char_of(",.") and not t.morph.class0_.is_preposition): 
                break
            t = t.previous
        if (t is None): 
            return None
        i = 0
        res = None
        tt = t
        first_pass2903 = True
        while True:
            if first_pass2903: first_pass2903 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            i += 1
            if (tt.is_newline_after and not tt.inner_bool): 
                break
            if (i > 10): 
                break
            tits0 = TerrItemToken.try_parse_list(tt, 5, None)
            if (tits0 is None): 
                continue
            if (tits0[len(tits0) - 1].end_token != t): 
                break
            tits1 = TerrItemToken.try_parse_list(tt.previous, 5, None)
            if (tits1 is not None and tits1[len(tits1) - 1].end_token == t and len(tits1) == len(tits0)): 
                tits0 = tits1
            rr = TerrDefineHelper.try_define(tits0, ad, False, None, None)
            if (rr is not None): 
                res = rr
        return res
    
    def __try_attach_territory_after_city(self, t : 'Token', ad : 'AnalyzerDataWithOntology') -> 'ReferentToken':
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        from pullenti.ner.geo.internal.TerrDefineHelper import TerrDefineHelper
        if (t is None): 
            return None
        city = Utils.asObjectOrNull(t.get_referent(), GeoReferent)
        if (city is None): 
            return None
        if (not city.is_city): 
            return None
        if (t.next0_ is None or not t.next0_.is_comma or t.next0_.whitespaces_after_count > 1): 
            return None
        tt = t.next0_.next0_
        if (tt is None or not tt.chars.is_capital_upper or not (isinstance(tt, TextToken))): 
            return None
        if (tt.chars.is_latin_letter): 
            re1 = TerrDefineHelper.try_attach_stateusaterritory(tt)
            if (re1 is not None): 
                return re1
        t0 = tt
        t1 = tt
        for i in range(2):
            tit0 = TerrItemToken.try_parse(tt, None, None)
            if (tit0 is None or tit0.termin_item is not None): 
                if (i == 0): 
                    return None
            cit0 = CityItemToken.try_parse(tt, None, False, None)
            if (cit0 is None or cit0.typ == CityItemToken.ItemType.NOUN): 
                if (i == 0): 
                    return None
            ait0 = AddressItemToken.try_parse(tt, False, None, None)
            if (ait0 is not None): 
                return None
            if (tit0 is None): 
                if (not tt.chars.is_cyrillic_letter): 
                    return None
                cla = tt.get_morph_class_in_dictionary()
                if (not cla.is_noun and not cla.is_adjective): 
                    return None
                t1 = tt
            else: 
                tt = tit0.end_token
                t1 = tt
            if (tt.next0_ is None): 
                return None
            if (tt.next0_.is_comma): 
                tt = tt.next0_.next0_
                break
            if (i > 0): 
                return None
            tt = tt.next0_
        ait = AddressItemToken.try_parse(tt, False, None, None)
        if (ait is None): 
            return None
        if (ait.typ != AddressItemType.STREET or ait.ref_token is not None): 
            return None
        reg = GeoReferent()
        reg._add_typ("муниципальный район")
        reg._add_name(MiscHelper.get_text_value(t0, t1, GetTextAttr.NO))
        return ReferentToken(reg, t0, t1)
    
    def process_referent(self, begin : 'Token', param : str) -> 'ReferentToken':
        # Это привязка стран к прилагательным (например, "французский лидер")
        from pullenti.ner.geo.internal.CityAttachHelper import CityAttachHelper
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        from pullenti.ner.geo.internal.TerrDefineHelper import TerrDefineHelper
        if (not (isinstance(begin, TextToken))): 
            return None
        ad = GeoAnalyzer._get_data(begin)
        if (ad is None): 
            return None
        if (ad.level > 1): 
            return None
        ad.level += 1
        toks = CityItemToken.M_CITY_ADJECTIVES.try_parse_all(begin, TerminParseAttr.FULLWORDSONLY)
        ad.level -= 1
        res1 = None
        if (toks is not None): 
            for tok in toks: 
                cit = Utils.asObjectOrNull(tok.termin.tag, IntOntologyItem)
                if (cit is None): 
                    continue
                city = GeoReferent()
                city._add_name(cit.canonic_text)
                city._add_typ_city(begin.kit.base_language, True)
                res1 = ReferentToken._new1281(city, tok.begin_token, tok.end_token, tok.morph, begin.kit.get_analyzer_data(self))
                break
        if (not begin.morph.class0_.is_adjective): 
            te = Utils.asObjectOrNull(begin, TextToken)
            if ((te.chars.is_all_upper and te.chars.is_cyrillic_letter and te.length_char == 2) and te.get_morph_class_in_dictionary().is_undefined): 
                abbr = te.term
                geo0 = None
                cou = 0
                for t in ad.local_ontology.items: 
                    geo_ = Utils.asObjectOrNull(t.referent, GeoReferent)
                    if (geo_ is None): 
                        continue
                    if (not geo_.is_region and not geo_.is_state): 
                        continue
                    if (geo_._check_abbr(abbr)): 
                        cou += 1
                        geo0 = geo_
                if (cou == 1 and res1 is None): 
                    res1 = ReferentToken._new1282(geo0, begin, begin, ad)
            ad.level += 1
            tt0 = TerrItemToken.try_parse(begin, None, None)
            ad.level -= 1
            if (tt0 is not None and tt0.termin_item is not None and tt0.termin_item.canonic_text == "РАЙОН"): 
                ad.level += 1
                tt1 = TerrItemToken.try_parse(tt0.end_token.next0_, None, None)
                ad.level -= 1
                if ((tt1 is not None and tt1.chars.is_capital_upper and tt1.termin_item is None) and tt1.onto_item is None): 
                    li = list()
                    li.append(tt0)
                    li.append(tt1)
                    res = TerrDefineHelper.try_define(li, ad, True, None, None)
                    if (res is None): 
                        return None
                    res.morph = begin.morph
                    res.data = (ad)
                    if (res1 is None or res.length_char > res1.length_char): 
                        res1 = res
            ad.level += 1
            ctoks = CityItemToken.try_parse_list(begin, 3, None)
            if (ctoks is None and begin.morph.class0_.is_preposition): 
                ctoks = CityItemToken.try_parse_list(begin.next0_, 3, None)
            ad.level -= 1
            if (ctoks is not None): 
                if (((len(ctoks) == 2 and ctoks[0].typ == CityItemToken.ItemType.NOUN and ctoks[1].typ == CityItemToken.ItemType.PROPERNAME)) or ((len(ctoks) == 1 and ctoks[0].typ == CityItemToken.ItemType.CITY))): 
                    if (len(ctoks) == 1 and ctoks[0].begin_token.get_morph_class_in_dictionary().is_proper_surname): 
                        kk = begin.kit.process_referent("PERSON", ctoks[0].begin_token, None)
                        if (kk is not None): 
                            return None
                    res = CityAttachHelper.try_define(ctoks, ad, True)
                    if (res is not None): 
                        res.data = (ad)
                        if (res1 is None or res.length_char > res1.length_char): 
                            res1 = res
            if ((ctoks is not None and len(ctoks) == 1 and ctoks[0].typ == CityItemToken.ItemType.NOUN) and ctoks[0].value == "ГОРОД"): 
                cou = 0
                t = begin.previous
                first_pass2904 = True
                while True:
                    if first_pass2904: first_pass2904 = False
                    else: t = t.previous
                    if (not (t is not None)): break
                    cou += 1
                    if (cou > 500): 
                        break
                    if (not (isinstance(t, ReferentToken))): 
                        continue
                    geos = t.get_referents()
                    if (geos is None): 
                        continue
                    for g in geos: 
                        gg = Utils.asObjectOrNull(g, GeoReferent)
                        if (gg is not None): 
                            res = None
                            if (gg.is_city): 
                                res = ReferentToken._new1281(gg, begin, ctoks[0].end_token, ctoks[0].morph, ad)
                            if (gg.higher is not None and gg.higher.is_city): 
                                res = ReferentToken._new1281(gg.higher, begin, ctoks[0].end_token, ctoks[0].morph, ad)
                            if (res is not None and ((res1 is None or res.length_char > res1.length_char))): 
                                res1 = res
            if (tt0 is not None and tt0.onto_item is not None): 
                pass
            else: 
                return res1
        ad.level += 1
        tt = TerrItemToken.try_parse(begin, None, None)
        ad.level -= 1
        if (tt is None or tt.onto_item is None): 
            tok = TerrItemToken._m_terr_ontology.try_attach(begin, None, False)
            if ((tok is not None and tok[0].item is not None and (isinstance(tok[0].item.referent, GeoReferent))) and tok[0].item.referent.is_state): 
                tt = TerrItemToken._new1243(tok[0].begin_token, tok[0].end_token, tok[0].item)
        if (tt is None): 
            return res1
        if (tt.onto_item is not None): 
            ad.level += 1
            li = TerrItemToken.try_parse_list(begin, 3, None)
            res = TerrDefineHelper.try_define(li, ad, True, None, None)
            ad.level -= 1
            if (res is None): 
                tt.onto_item = (None)
            else: 
                if (res.begin_token == res.end_token): 
                    mc = res.begin_token.get_morph_class_in_dictionary()
                    if (mc.is_adjective): 
                        geo_ = Utils.asObjectOrNull(tt.onto_item.referent, GeoReferent)
                        if (geo_.is_city or geo_.is_state): 
                            pass
                        elif (geo_.find_slot(GeoReferent.ATTR_TYPE, "федеральный округ", True) is not None): 
                            return None
                res.data = (ad)
                if (res1 is None or res.length_char > res1.length_char): 
                    res1 = res
        if (not tt.is_adjective): 
            return res1
        if (tt.onto_item is None): 
            t1 = tt.end_token.next0_
            if (t1 is None): 
                return res1
            ad.level += 1
            ttyp = TerrItemToken.try_parse(t1, None, None)
            ad.level -= 1
            if (ttyp is None or ttyp.termin_item is None): 
                ad.level += 1
                cits = CityItemToken.try_parse_list(begin, 2, None)
                ad.level -= 1
                if (cits is not None and cits[0].typ == CityItemToken.ItemType.CITY): 
                    ad.level += 1
                    res2 = CityAttachHelper.try_define(cits, ad, True)
                    ad.level -= 1
                    if (res2 is not None): 
                        if (res1 is None or res2.length_char > res1.length_char): 
                            res1 = res2
                return res1
            if (t1.get_morph_class_in_dictionary().is_adjective): 
                return res1
            li = list()
            li.append(tt)
            li.append(ttyp)
            ad.level += 1
            res = TerrDefineHelper.try_define(li, ad, True, None, None)
            ad.level -= 1
            if (res is None): 
                return res1
            res.morph = ttyp.morph
            res.data = (ad)
            if (res1 is None or res.length_char > res1.length_char): 
                res1 = res
        return res1
    
    def process_citizen(self, begin : 'Token') -> 'ReferentToken':
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        if (not (isinstance(begin, TextToken))): 
            return None
        tok = TerrItemToken.M_MANS_BY_STATE.try_parse(begin, TerminParseAttr.FULLWORDSONLY)
        if (tok is not None): 
            tok.morph.gender = tok.termin.gender
        if (tok is None): 
            return None
        geo0 = Utils.asObjectOrNull(tok.termin.tag, GeoReferent)
        if (geo0 is None): 
            return None
        geo_ = GeoReferent()
        geo_._merge_slots2(geo0, begin.kit.base_language)
        res = ReferentToken(geo_, tok.begin_token, tok.end_token)
        res.morph = tok.morph
        ad = Utils.asObjectOrNull(begin.kit.get_analyzer_data(self), AnalyzerDataWithOntology)
        res.data = (ad)
        return res
    
    def process_ontology_item(self, begin : 'Token') -> 'ReferentToken':
        from pullenti.ner.geo.internal.CityAttachHelper import CityAttachHelper
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        li = CityItemToken.try_parse_list(begin, 4, None)
        if (li is not None and len(li) > 1 and li[0].typ == CityItemToken.ItemType.NOUN): 
            rt = CityAttachHelper.try_define(li, None, True)
            if (rt is None): 
                return None
            city = Utils.asObjectOrNull(rt.referent, GeoReferent)
            t = rt.end_token.next0_
            first_pass2905 = True
            while True:
                if first_pass2905: first_pass2905 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (not t.is_char(';')): 
                    continue
                t = t.next0_
                if (t is None): 
                    break
                li = CityItemToken.try_parse_list(t, 4, None)
                rt1 = CityAttachHelper.try_define(li, None, False)
                if (rt1 is not None): 
                    rt.end_token = rt1.end_token
                    t = rt.end_token
                    city._merge_slots2(rt1.referent, begin.kit.base_language)
                else: 
                    tt = None
                    ttt = t
                    while ttt is not None: 
                        if (ttt.is_char(';')): 
                            break
                        else: 
                            tt = ttt
                        ttt = ttt.next0_
                    if (tt is not None): 
                        str0_ = MiscHelper.get_text_value(t, tt, GetTextAttr.NO)
                        if (str0_ is not None): 
                            city._add_name(str0_)
                        rt.end_token = tt
                        t = rt.end_token
            return rt
        typ = None
        terr = None
        te = None
        t = begin
        first_pass2906 = True
        while True:
            if first_pass2906: first_pass2906 = False
            else: t = t.next0_
            if (not (t is not None)): break
            t0 = t
            t1 = None
            tn0 = None
            tn1 = None
            tt = t0
            first_pass2907 = True
            while True:
                if first_pass2907: first_pass2907 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_char_of(";")): 
                    break
                tit = TerrItemToken.try_parse(tt, None, None)
                if (tit is not None and tit.termin_item is not None): 
                    if (not tit.is_adjective): 
                        if (typ is None): 
                            typ = tit.termin_item.canonic_text
                        tt = tit.end_token
                        t1 = tt
                        continue
                elif (tit is not None and tit.onto_item is not None): 
                    pass
                if (tn0 is None): 
                    tn0 = tt
                if (tit is not None): 
                    tt = tit.end_token
                tn1 = tt
                t1 = tn1
            if (t1 is None): 
                continue
            if (terr is None): 
                terr = GeoReferent()
            if (tn0 is not None): 
                terr._add_name(MiscHelper.get_text_value(tn0, tn1, GetTextAttr.NO))
            te = t1
            t = te
        if (terr is None or te is None): 
            return None
        if (typ is not None): 
            terr._add_typ(typ)
        if (not terr.is_city and not terr.is_region and not terr.is_state): 
            terr._add_typ_reg(begin.kit.base_language)
        return ReferentToken(terr, begin, te)
    
    @staticmethod
    def get_all_countries() -> typing.List['Referent']:
        """ Получить список всех стран из внутреннего словаря
        
        """
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        return TerrItemToken._m_all_states
    
    __m_initialized = False
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.address.AddressAnalyzer import AddressAnalyzer
        from pullenti.ner.geo.internal.NameToken import NameToken
        from pullenti.ner.geo.internal.OrgTypToken import OrgTypToken
        if (GeoAnalyzer.__m_initialized): 
            return
        GeoAnalyzer.__m_initialized = True
        MetaGeo.initialize()
        MetaAddress.initialize()
        MetaStreet.initialize()
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
            MiscLocationHelper._initialize()
            OrgTypToken.initialize()
            NameToken.initialize()
            TerrItemToken.initialize()
            CityItemToken.initialize()
            AddressAnalyzer.initialize()
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        ProcessorService.register_analyzer(GeoAnalyzer())