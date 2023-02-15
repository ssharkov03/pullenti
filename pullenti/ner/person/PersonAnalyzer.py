# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.person.internal.PersonAttrTerminType import PersonAttrTerminType
from pullenti.ner.core.Termin import Termin
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.person.internal.FioTemplateType import FioTemplateType
from pullenti.ner.person.internal.ShortNameHelper import ShortNameHelper
from pullenti.ner.person.PersonPropertyKind import PersonPropertyKind
from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.mail.internal.MailLine import MailLine
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.core.internal.PullentiNerCoreInternalResourceHelper import PullentiNerCoreInternalResourceHelper
from pullenti.ner.person.internal.MetaPersonProperty import MetaPersonProperty
from pullenti.ner.person.internal.MetaPerson import MetaPerson
from pullenti.ner.TextToken import TextToken
from pullenti.ner.person.internal.MetaPersonIdentity import MetaPersonIdentity
from pullenti.ner.Token import Token
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.Referent import Referent
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.Analyzer import Analyzer

class PersonAnalyzer(Analyzer):
    """ Анализатор выделения персон и их атрибутов (должности, звания и пр.) """
    
    ANALYZER_NAME = "PERSON"
    """ Имя анализатора ("PERSON") """
    
    @property
    def name(self) -> str:
        return PersonAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Персоны"
    
    @property
    def description(self) -> str:
        return "Персоны и их атрибуты"
    
    def clone(self) -> 'Analyzer':
        return PersonAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaPerson._global_meta, MetaPersonProperty._global_meta, MetaPersonIdentity._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaPerson.MAN_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("man.png")
        res[MetaPerson.WOMEN_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("women.png")
        res[MetaPerson.PERSON_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("person.png")
        res[MetaPerson.GENERAL_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("general.png")
        res[MetaPersonProperty.PERSON_PROP_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("personproperty.png")
        res[MetaPersonProperty.PERSON_PROP_BOSS_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("boss.png")
        res[MetaPersonProperty.PERSON_PROP_KING_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("king.png")
        res[MetaPersonProperty.PERSON_PROP_KIN_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("kin.png")
        res[MetaPersonProperty.PERSON_PROP_MILITARY_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("militaryrank.png")
        res[MetaPersonProperty.PERSON_PROP_NATION_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("nationality.png")
        res[MetaPersonIdentity.IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("identity.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == PersonReferent.OBJ_TYPENAME): 
            return PersonReferent()
        if (type0_ == PersonPropertyReferent.OBJ_TYPENAME): 
            return PersonPropertyReferent()
        if (type0_ == PersonIdentityReferent.OBJ_TYPENAME): 
            return PersonIdentityReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["ORGANIZATION", "GEO", "ADDRESS", "TRANSPORT"]
    
    @property
    def progress_weight(self) -> int:
        return 35
    
    NOMINATIVE_CASE_ALWAYS = False
    """ При анализе считать, что все персоны идут в именительном падеже """
    
    TEXT_STARTS_WITH_LASTNAME_FIRSTNAME_MIDDLENAME = False
    """ При анализе считать, что текст начинается с Фамилии Имени Отчества """
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        from pullenti.ner.person.internal.PersonAnalyzerData import PersonAnalyzerData
        return PersonAnalyzerData()
    
    @staticmethod
    def _get_data(t : 'Token') -> 'PersonAnalyzerData':
        from pullenti.ner.person.internal.PersonAnalyzerData import PersonAnalyzerData
        if (t is None): 
            return None
        return Utils.asObjectOrNull(t.kit.get_analyzer_data_by_analyzer_name(PersonAnalyzer.ANALYZER_NAME), PersonAnalyzerData)
    
    def process(self, kit : 'AnalysisKit') -> None:
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        from pullenti.ner.person.internal.PersonIdToken import PersonIdToken
        from pullenti.ner.person.internal.PersonAnalyzerData import PersonAnalyzerData
        ad = Utils.asObjectOrNull(kit.get_analyzer_data(self), PersonAnalyzerData)
        ad.nominative_case_always = PersonAnalyzer.NOMINATIVE_CASE_ALWAYS
        ad.text_starts_with_lastname_firstname_middlename = PersonAnalyzer.TEXT_STARTS_WITH_LASTNAME_FIRSTNAME_MIDDLENAME
        ad.need_second_step = False
        PersonAttrToken.SPEED_REGIME = False
        PersonAttrToken._prepare_all_data(kit.first_token)
        ad.aregime = True
        t = kit.first_token
        while t is not None: 
            t.inner_bool = False
            t = t.next0_
        steps = 2
        max0_ = steps
        delta = 100000
        tlen = len(kit.sofa.text)
        if (kit.sofa.ignored_end_char > 0): 
            tlen = (kit.sofa.ignored_begin_char + ((tlen - kit.sofa.ignored_end_char)))
        parts = math.floor((((tlen + delta) - 1)) / delta)
        if (parts == 0): 
            parts = 1
        max0_ *= parts
        cur = 0
        step = 0
        while step < steps: 
            next_pos = delta
            t = kit.first_token
            first_pass3006 = True
            while True:
                if first_pass3006: first_pass3006 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_ignored): 
                    continue
                if (t.begin_char > next_pos): 
                    next_pos += delta
                    if (next_pos <= t.begin_char): 
                        next_pos = (t.begin_char + delta)
                    cur += 1
                    if (cur > max0_): 
                        cur = max0_
                    if (not self._on_progress(cur, max0_, kit)): 
                        return
                if ((isinstance(t, NumberToken)) and t.value == "70"): 
                    pass
                rts = self.__try_attach_persons(t, step)
                if (rts is not None): 
                    if (not MetaToken.check(rts)): 
                        pass
                    else: 
                        for rt in rts: 
                            if (rt.length_char == 1): 
                                pass
                            if (rt.referent is None): 
                                t = rt.end_token
                            else: 
                                pats = list()
                                for s in rt.referent.slots: 
                                    if (isinstance(s.value, PersonAttrToken)): 
                                        pat = Utils.asObjectOrNull(s.value, PersonAttrToken)
                                        pats.append(pat)
                                        if (pat.prop_ref is None): 
                                            continue
                                        for ss in pat.prop_ref.slots: 
                                            if (ss.type_name == PersonPropertyReferent.ATTR_REF and (isinstance(ss.value, ReferentToken))): 
                                                rt1 = Utils.asObjectOrNull(ss.value, ReferentToken)
                                                rt1.referent = ad.register_referent(rt1.referent)
                                                ss.value = rt1.referent
                                                rr = ReferentToken._new956(rt1.referent, rt1.begin_token, rt1.end_token, rt1.morph)
                                                kit.embed_token(rr)
                                                if (rr.begin_token == rt.begin_token): 
                                                    rt.begin_token = rr
                                                if (rr.end_token == rt.end_token): 
                                                    rt.end_token = rr
                                                if (rr.begin_token == pat.begin_token): 
                                                    pat.begin_token = rr
                                                if (rr.end_token == pat.end_token): 
                                                    pat.end_token = rr
                                    elif (isinstance(s.value, ReferentToken)): 
                                        rt0 = Utils.asObjectOrNull(s.value, ReferentToken)
                                        if (rt0.referent is not None): 
                                            for s1 in rt0.referent.slots: 
                                                if (isinstance(s1.value, PersonAttrToken)): 
                                                    pat = Utils.asObjectOrNull(s1.value, PersonAttrToken)
                                                    if (pat.prop_ref is None): 
                                                        continue
                                                    for ss in pat.prop_ref.slots: 
                                                        if (ss.type_name == PersonPropertyReferent.ATTR_REF and (isinstance(ss.value, ReferentToken))): 
                                                            rt1 = Utils.asObjectOrNull(ss.value, ReferentToken)
                                                            rt1.referent = ad.register_referent(rt1.referent)
                                                            ss.value = rt1.referent
                                                            rr = ReferentToken._new956(rt1.referent, rt1.begin_token, rt1.end_token, rt1.morph)
                                                            kit.embed_token(rr)
                                                            if (rr.begin_token == rt0.begin_token): 
                                                                rt0.begin_token = rr
                                                            if (rr.end_token == rt0.end_token): 
                                                                rt0.end_token = rr
                                                            if (rr.begin_token == pat.begin_token): 
                                                                pat.begin_token = rr
                                                            if (rr.end_token == pat.end_token): 
                                                                pat.end_token = rr
                                                    pat.prop_ref = Utils.asObjectOrNull(ad.register_referent(pat.prop_ref), PersonPropertyReferent)
                                                    rt2 = ReferentToken._new956(pat.prop_ref, pat.begin_token, pat.end_token, pat.morph)
                                                    kit.embed_token(rt2)
                                                    if (rt2.begin_token == rt0.begin_token): 
                                                        rt0.begin_token = rt2
                                                    if (rt2.end_token == rt0.end_token): 
                                                        rt0.end_token = rt2
                                                    s1.value = pat.prop_ref
                                        rt0.referent = ad.register_referent(rt0.referent)
                                        if (rt0.begin_char == rt.begin_char): 
                                            rt.begin_token = rt0
                                        if (rt0.end_char == rt.end_char): 
                                            rt.end_token = rt0
                                        kit.embed_token(rt0)
                                        s.value = rt0.referent
                                rt.referent = ad.register_referent(rt.referent)
                                for p in pats: 
                                    if (p.prop_ref is not None): 
                                        rr = ReferentToken._new956(p.prop_ref, p.begin_token, p.end_token, p.morph)
                                        kit.embed_token(rr)
                                        if (rr.begin_token == rt.begin_token): 
                                            rt.begin_token = rr
                                        if (rr.end_token == rt.end_token): 
                                            rt.end_token = rr
                                kit.embed_token(rt)
                                t = (rt)
                elif (step == 0): 
                    rt = PersonIdToken.try_attach(t)
                    if (rt is not None): 
                        rt.referent = ad.register_referent(rt.referent)
                        tt = t.previous
                        if (tt is not None and tt.is_char_of(":,")): 
                            tt = tt.previous
                        pers = (None if tt is None else Utils.asObjectOrNull(tt.get_referent(), PersonReferent))
                        if (pers is not None): 
                            pers.add_slot(PersonReferent.ATTR_IDDOC, rt.referent, False, 0)
                        kit.embed_token(rt)
                        t = (rt)
            if (len(ad.referents) == 0 and not ad.need_second_step): 
                break
            step += 1
        gen_attrs = list()
        t = kit.first_token
        first_pass3007 = True
        while True:
            if first_pass3007: first_pass3007 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_ignored or not (isinstance(t, ReferentToken))): 
                continue
            p = Utils.asObjectOrNull(t.get_referent(), PersonReferent)
            if (p is None): 
                continue
            if (p.find_slot(PersonReferent.ATTR_ATTR, None, True) is None): 
                continue
            tt = t.begin_token
            first_pass3008 = True
            while True:
                if first_pass3008: first_pass3008 = False
                else: tt = tt.next0_
                if (not (tt is not None and tt.end_char <= t.end_char)): break
                pr = Utils.asObjectOrNull(tt.get_referent(), PersonPropertyReferent)
                if (pr is None): 
                    continue
                s0 = p.find_slot(PersonReferent.ATTR_ATTR, pr, True)
                for s in p.slots: 
                    if (s.type_name == PersonReferent.ATTR_ATTR and s != s0): 
                        pr1 = Utils.asObjectOrNull(s.value, PersonPropertyReferent)
                        if (pr1 is None): 
                            continue
                        if (not pr.can_be_general_for(pr1)): 
                            continue
                        tt.referent = (pr1)
                        if (pr1.general_referent is not None): 
                            pr1.general_referent = None
                        pr1.add_occurence_of_ref_tok(Utils.asObjectOrNull(tt, ReferentToken))
                        if (not pr in gen_attrs): 
                            gen_attrs.append(pr)
                        for o in pr.occurrence: 
                            if (o.begin_char == tt.begin_char): 
                                pr.occurrence.remove(o)
                                break
                        hi = pr.higher
                        if (hi is not None): 
                            if (pr1.higher is not None and hi.can_be_general_for(pr1.higher)): 
                                if (not hi in gen_attrs): 
                                    gen_attrs.append(hi)
                                for o in hi.occurrence: 
                                    if (o.begin_char >= tt.begin_char and o.end_char <= tt.end_char): 
                                        hi.occurrence.remove(o)
                                        break
                        if (s0 is not None): 
                            p.slots.remove(s0)
                        break
        for g in gen_attrs: 
            if (len(g.occurrence) == 0): 
                ad.remove_referent(g)
        props = dict()
        for r in ad.referents: 
            p = Utils.asObjectOrNull(r, PersonReferent)
            if (p is None): 
                continue
            for s in p.slots: 
                if (s.type_name == PersonReferent.ATTR_ATTR and (isinstance(s.value, PersonPropertyReferent))): 
                    pr = Utils.asObjectOrNull(s.value, PersonPropertyReferent)
                    li = [ ]
                    wrapli2377 = RefOutArgWrapper(None)
                    inoutres2378 = Utils.tryGetValue(props, pr, wrapli2377)
                    li = wrapli2377.value
                    if (not inoutres2378): 
                        li = list()
                        props[pr] = li
                    if (not p in li): 
                        li.append(p)
        t = kit.first_token
        first_pass3009 = True
        while True:
            if first_pass3009: first_pass3009 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_ignored): 
                continue
            if (isinstance(t, ReferentToken)): 
                if (t.chars.is_latin_letter and MiscHelper.is_eng_adj_suffix(t.next0_)): 
                    pass
                else: 
                    continue
            if (not t.begin_char in ad.can_be_person_prop_begin_chars): 
                continue
            pat = PersonAttrToken.try_attach(t, PersonAttrToken.PersonAttrAttachAttrs.NO)
            if (pat is None): 
                continue
            if (pat.prop_ref is None or ((pat.typ != PersonAttrTerminType.POSITION and pat.typ != PersonAttrTerminType.KING))): 
                t = pat.end_token
                continue
            pers = list()
            ppr = None
            for kp in props.items(): 
                if (kp[0].can_be_equals(pat.prop_ref, ReferentsEqualType.WITHINONETEXT)): 
                    ppr = kp[0]
                    for pp in kp[1]: 
                        if (not pp in pers): 
                            pers.append(pp)
                    if (len(pers) > 1): 
                        break
            if (len(pers) == 1): 
                tt = pat.end_token.next0_
                if (tt is not None and ((tt.is_char('_') or tt.is_newline_before or tt.is_table_control_char))): 
                    pass
                else: 
                    rt1 = ReferentToken._new956(ppr, pat, pat, pat.morph)
                    kit.embed_token(rt1)
                    rt2 = ReferentToken._new956(pers[0], rt1, rt1, pat.morph)
                    kit.embed_token(rt2)
                    continue
            if (pat.prop_ref is not None): 
                if (pat.can_be_independent_property or len(pers) > 0): 
                    rt = ReferentToken._new956(ad.register_referent(pat.prop_ref), pat.begin_token, pat.end_token, pat.morph)
                    kit.embed_token(rt)
                    t = (rt)
                    continue
            t = pat.end_token
        ad.aregime = False
    
    @staticmethod
    def process_referent_stat(begin : 'Token', param : str=None) -> 'ReferentToken':
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        if (begin is None): 
            return None
        ad = PersonAnalyzer._get_data(begin)
        if (ad is None or ad.level > 1): 
            return None
        begin.kit.fix_analyzer("ORGANIZATION", True)
        ad.level += 1
        rt = PersonAnalyzer._try_attach_person(begin, False, -1, False)
        ad.level -= 1
        begin.kit.fix_analyzer("ORGANIZATION", False)
        if (rt is not None and rt.referent is None): 
            rt = (None)
        if (rt is not None): 
            rt.data = (ad)
            return rt
        ad.level += 1
        begin.kit.fix_analyzer("ORGANIZATION", True)
        pat = PersonAttrToken.try_attach(begin, PersonAttrToken.PersonAttrAttachAttrs.NO)
        begin.kit.fix_analyzer("ORGANIZATION", False)
        ad.level -= 1
        if (pat is None or pat.prop_ref is None): 
            return None
        rt = ReferentToken._new956(pat.prop_ref, pat.begin_token, pat.end_token, pat.morph)
        rt.data = (ad)
        return rt
    
    def process_referent(self, begin : 'Token', param : str) -> 'ReferentToken':
        return PersonAnalyzer.process_referent_stat(begin, param)
    
    def __try_attach_persons(self, t : 'Token', step : int) -> typing.List['ReferentToken']:
        from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
        rt = PersonAnalyzer._try_attach_person(t, False, step, False)
        if (rt is None): 
            return None
        res = list()
        res.append(rt)
        names = None
        tt = rt.end_token.next0_
        while tt is not None: 
            if (not tt.is_comma_and): 
                break
            pits = PersonItemToken.try_attach_list(tt.next0_, PersonItemToken.ParseAttr.NO, 10)
            if (pits is None or len(pits) != 1): 
                break
            rt1 = PersonAnalyzer._try_attach_person(tt.next0_, False, step, False)
            if (rt1 is not None): 
                break
            if (pits[0].firstname is None or len(pits[0].firstname.vars0_) == 0): 
                break
            if (names is None): 
                names = list()
            names.append(pits[0])
            if (tt.is_and): 
                break
            tt = tt.next0_
            tt = tt.next0_
        if (names is not None): 
            for n in names: 
                pers = PersonReferent()
                bi = MorphBaseInfo._new2383(MorphNumber.SINGULAR, t.kit.base_language)
                bi.class0_ = MorphClass._new2344(True)
                if (n.firstname.vars0_[0].gender == MorphGender.FEMINIE): 
                    pers.is_female = True
                    bi.gender = MorphGender.FEMINIE
                elif (n.firstname.vars0_[0].gender == MorphGender.MASCULINE): 
                    pers.is_male = True
                    bi.gender = MorphGender.MASCULINE
                for v in n.firstname.vars0_: 
                    pers.add_slot(PersonReferent.ATTR_FIRSTNAME, v.value, False, 0)
                for s in rt.referent.slots: 
                    if (s.type_name == PersonReferent.ATTR_ATTR): 
                        pers.add_slot(s.type_name, s.value, False, 0)
                    elif (s.type_name == PersonReferent.ATTR_LASTNAME): 
                        sur = Utils.asObjectOrNull(s.value, str)
                        if (bi.gender != MorphGender.UNDEFINED): 
                            sur0 = MorphologyService.get_wordform(sur, bi)
                            if (sur0 is not None): 
                                pers.add_slot(PersonReferent.ATTR_LASTNAME, sur0, False, 0)
                        pers.add_slot(PersonReferent.ATTR_LASTNAME, sur, False, 0)
                res.append(ReferentToken._new956(pers, n.begin_token, n.end_token, n.morph))
        return res
    
    @staticmethod
    def _try_attach_person(t : 'Token', for_ext_ontos : bool, step : int, for_attribute : bool=False) -> 'ReferentToken':
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
        from pullenti.ner.person.internal.PersonMorphCollection import PersonMorphCollection
        from pullenti.ner.person.internal.PersonHelper import PersonHelper
        from pullenti.ner.person.internal.PersonIdentityToken import PersonIdentityToken
        attrs = None
        mi = MorphBaseInfo()
        ad = PersonAnalyzer._get_data(t)
        if (ad is None): 
            return None
        mi.case_ = (MorphCase.NOMINATIVE if (for_ext_ontos or ad.nominative_case_always) else MorphCase.ALL_CASES)
        mi.gender = Utils.valToEnum((MorphGender.MASCULINE) | (MorphGender.FEMINIE), MorphGender)
        t0 = t
        and0_ = False
        and_was_terminated = False
        is_genitive = False
        can_attach_to_previous_person = True
        is_king = False
        after_be_predicate = False
        first_pass3010 = True
        while True:
            if first_pass3010: first_pass3010 = False
            else: t = (None if t is None else t.next0_)
            if (not (t is not None)): break
            if (attrs is not None and t.next0_ is not None): 
                if (and0_): 
                    break
                if (t.is_char(',')): 
                    t = t.next0_
                elif (t.is_and and t.is_whitespace_after and t.chars.is_all_lower): 
                    t = t.next0_
                    and0_ = True
                elif (t.is_hiphen and t.is_newline_after): 
                    t = t.next0_
                    and0_ = True
                elif (t.is_hiphen and t.whitespaces_after_count == 1 and t.whitespaces_before_count == 1): 
                    t = t.next0_
                    and0_ = True
                elif ((t.is_hiphen and t.next0_ is not None and t.next0_.is_hiphen) and t.next0_.whitespaces_after_count == 1 and t.whitespaces_before_count == 1): 
                    t = t.next0_.next0_
                    and0_ = True
                elif (t.is_char(':')): 
                    if (not attrs[len(attrs) - 1].morph.case_.is_nominative and not attrs[len(attrs) - 1].morph.case_.is_undefined): 
                        pass
                    else: 
                        mi.case_ = MorphCase.NOMINATIVE
                        mi.gender = Utils.valToEnum((MorphGender.MASCULINE) | (MorphGender.FEMINIE), MorphGender)
                    t = t.next0_
                    if (not BracketHelper.can_be_start_of_sequence(t, False, False)): 
                        can_attach_to_previous_person = False
                elif (t.is_char('_')): 
                    cou = 0
                    te = t
                    while te is not None: 
                        if (not te.is_char('_') or ((te.is_whitespace_before and te != t))): 
                            break
                        else: 
                            cou += 1
                        te = te.next0_
                    if (cou > 2 and ((not t.is_newline_before or ((te is not None and not te.is_newline_before))))): 
                        mi.case_ = MorphCase.NOMINATIVE
                        mi.gender = Utils.valToEnum((MorphGender.MASCULINE) | (MorphGender.FEMINIE), MorphGender)
                        can_attach_to_previous_person = False
                        t = te
                        if (t is not None and t.is_char('/') and t.next0_ is not None): 
                            t = t.next0_
                        break
                elif ((t.is_value("ЯВЛЯТЬСЯ", None) or t.is_value("БЫТЬ", None) or t.is_value("Є", None)) or t.is_value("IS", None)): 
                    mi.case_ = MorphCase.NOMINATIVE
                    mi.gender = Utils.valToEnum((MorphGender.MASCULINE) | (MorphGender.FEMINIE), MorphGender)
                    after_be_predicate = True
                    continue
                elif (((t.is_value("LIKE", None) or t.is_value("AS", None))) and attrs is not None): 
                    t = t.next0_
                    break
            if (t.chars.is_latin_letter and step == 0): 
                tt2 = t
                if (MiscHelper.is_eng_article(t)): 
                    tt2 = t.next0_
                pit0 = PersonItemToken.try_attach(tt2, PersonItemToken.ParseAttr.CANBELATIN, None)
                if (pit0 is not None and MiscHelper.is_eng_adj_suffix(pit0.end_token.next0_) and ad is not None): 
                    pp = PersonIdentityToken.try_attach_onto_for_single(pit0, ad.local_ontology)
                    if (pp is None): 
                        pp = PersonIdentityToken.try_attach_latin_surname(pit0, ad.local_ontology)
                    if (pp is not None): 
                        return PersonHelper._create_referent_token(pp, pit0.begin_token, pit0.end_token, pit0.morph, attrs, for_attribute, after_be_predicate)
            a = None
            if ((step < 1) or t.inner_bool): 
                a = PersonAttrToken.try_attach(t, PersonAttrToken.PersonAttrAttachAttrs.NO)
                if (step == 0 and a is not None): 
                    t.inner_bool = True
            if ((a is not None and a.begin_token == a.end_token and not a.begin_token.chars.is_all_lower) and (a.whitespaces_after_count < 3)): 
                pits = PersonItemToken.try_attach_list(t, PersonItemToken.ParseAttr.IGNOREATTRS, 10)
                if (pits is not None and len(pits) >= 6): 
                    if (pits[2].is_newline_after and pits[5].is_newline_after): 
                        a = (None)
            if ((a is None and t.is_value("НА", None) and t.next0_ is not None) and t.next0_.is_value("ИМЯ", None)): 
                a = PersonAttrToken._new2162(t, t.next0_, MorphCollection._new2166(MorphCase.GENITIVE))
                is_genitive = True
            if (a is None): 
                break
            if (after_be_predicate): 
                return None
            if (a.newlines_after_count > 3): 
                break
            if (not t.chars.is_all_lower and a.begin_token == a.end_token): 
                pit = PersonItemToken.try_attach(t, PersonItemToken.ParseAttr.CANBELATIN, None)
                if (pit is not None and pit.lastname is not None and ((pit.lastname.is_in_ontology or pit.lastname.is_in_dictionary))): 
                    break
            if (ad is not None and not a.begin_char in ad.can_be_person_prop_begin_chars): 
                ad.can_be_person_prop_begin_chars[a.begin_char] = True
            if (attrs is None): 
                if (a.is_doubt): 
                    if (a.is_newline_after): 
                        break
                attrs = list()
            else: 
                if (not a.morph.case_.is_undefined and not mi.case_.is_undefined): 
                    if (((a.morph.case_) & mi.case_).is_undefined): 
                        return None
                if ((t.previous.is_and and len(attrs) == 1 and attrs[0].prop_ref is not None) and a.prop_ref is not None): 
                    r1 = Utils.asObjectOrNull(attrs[0].prop_ref.get_slot_value(PersonPropertyReferent.ATTR_REF), Referent)
                    r2 = Utils.asObjectOrNull(a.prop_ref.get_slot_value(PersonPropertyReferent.ATTR_REF), Referent)
                    if ((isinstance(r1, GeoReferent)) and (isinstance(r2, GeoReferent))): 
                        if (not r1.can_be_equals(r2, ReferentsEqualType.WITHINONETEXT)): 
                            return None
            attrs.append(a)
            if (len(attrs) > 5): 
                return ReferentToken(None, attrs[0].begin_token, a.end_token)
            if (a.typ == PersonAttrTerminType.KING): 
                is_king = True
            if (a.typ == PersonAttrTerminType.BESTREGARDS): 
                mi.case_ = MorphCase.NOMINATIVE
            if (and0_): 
                and_was_terminated = True
            if (a.can_has_person_after >= 0): 
                if (a.gender != MorphGender.UNDEFINED): 
                    if (a.typ != PersonAttrTerminType.POSITION): 
                        mi.gender = Utils.valToEnum((mi.gender) & (a.gender), MorphGender)
                    elif (a.gender == MorphGender.FEMINIE): 
                        mi.gender = Utils.valToEnum((mi.gender) & (a.gender), MorphGender)
                if (not a.morph.case_.is_undefined and a.can_has_person_after == 0): 
                    mi.case_ = (mi.case_) & a.morph.case_
            t = a.end_token
        if (attrs is not None and and0_ and not and_was_terminated): 
            if ((t is not None and t.previous is not None and t.previous.is_hiphen) and (t.whitespaces_before_count < 2)): 
                pass
            else: 
                return None
        if (attrs is not None): 
            if (t is not None and BracketHelper.can_be_end_of_sequence(t, False, None, False)): 
                t = t.next0_
        while t is not None and ((t.is_table_control_char or t.is_char('_'))):
            t = t.next0_
        if (t is None): 
            if (attrs is not None): 
                attr = attrs[len(attrs) - 1]
                if (attr.can_be_single_person and attr.prop_ref is not None): 
                    return ReferentToken(attr.prop_ref, attr.begin_token, attr.end_token)
            return None
        if (attrs is not None and t.is_char('(')): 
            pr = PersonAnalyzer._try_attach_person(t.next0_, for_ext_ontos, step, for_attribute)
            if (pr is not None and pr.end_token.next0_ is not None and pr.end_token.next0_.is_char(')')): 
                res = PersonHelper._create_referent_token(Utils.asObjectOrNull(pr.referent, PersonReferent), t, pr.end_token.next0_, attrs[0].morph, attrs, True, after_be_predicate)
                if (res is not None): 
                    res.end_token = pr.end_token.next0_
                return res
            attr = PersonAttrToken.try_attach(t.next0_, PersonAttrToken.PersonAttrAttachAttrs.NO)
            if (attr is not None and attr.end_token.next0_ is not None and attr.end_token.next0_.is_char(')')): 
                attrs.append(attr)
                t = attr.end_token.next0_.next0_
                while t is not None and ((t.is_table_control_char or t.is_char_of("_:"))):
                    t = t.next0_
        if (attrs is not None and t is not None and t.is_char('(')): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (br is not None and (br.length_char < 200)): 
                t = br.end_token.next0_
        tt0 = t0.previous
        if (mi.case_.equals(MorphCase.ALL_CASES) and tt0 is not None): 
            if (tt0 is not None and tt0.is_comma_and): 
                tt0 = tt0.previous
                if (tt0 is not None and (isinstance(tt0.get_referent(), PersonReferent))): 
                    if (not tt0.morph.case_.is_undefined): 
                        mi.case_ = (mi.case_) & tt0.morph.case_
        if ((attrs is not None and t is not None and t.previous is not None) and t.previous.is_char(',')): 
            if (attrs[0].typ != PersonAttrTerminType.BESTREGARDS and not attrs[0].chars.is_latin_letter): 
                if (attrs[0].is_newline_before): 
                    pass
                elif (attrs[0].begin_token.previous is not None and attrs[0].begin_token.previous.is_value("ЛИЦО", "ОСОБІ")): 
                    pass
                else: 
                    return None
        if (step == 1): 
            pass
        if (t is None): 
            return None
        if (t.previous is not None and t.previous.is_comma_and): 
            pass
        for k in range(2):
            pits = None
            pattr = PersonItemToken.ParseAttr.NO
            if ((step < 1) or t.inner_bool): 
                if (k == 0): 
                    pattr = (Utils.valToEnum((pattr) | (PersonItemToken.ParseAttr.ALTVAR), PersonItemToken.ParseAttr))
                if (for_ext_ontos or t.chars.is_latin_letter): 
                    pattr = (Utils.valToEnum((pattr) | (PersonItemToken.ParseAttr.CANBELATIN), PersonItemToken.ParseAttr))
                if (attrs is not None): 
                    pattr = (Utils.valToEnum((pattr) | (PersonItemToken.ParseAttr.AFTERATTRIBUTE), PersonItemToken.ParseAttr))
                pits = PersonItemToken.try_attach_list(t, pattr, 15)
                if (pits is not None and step == 0): 
                    t.inner_bool = True
                if (pits is not None and is_genitive): 
                    for p in pits: 
                        p.remove_not_genitive()
            if (pits is None): 
                continue
            if (not for_ext_ontos): 
                pass
            if ((step == 0 and len(pits) == 1 and attrs is not None) and attrs[len(attrs) - 1].end_token == t.previous and pits[0].end_token == t): 
                stat = t.kit.statistics.get_word_info(t)
                if (stat is not None): 
                    stat.has_before_person_attr = True
                if (ad is not None): 
                    ad.need_second_step = True
            if (pits is not None and len(pits) == 1 and pits[0].firstname is not None): 
                if (pits[0].end_token.next0_ is not None and pits[0].end_token.next0_.is_and and (isinstance(pits[0].end_token.next0_.next0_, ReferentToken))): 
                    pr = Utils.asObjectOrNull(pits[0].end_token.next0_.next0_.get_referent(), PersonReferent)
                    if (pr is not None): 
                        if (len(pits[0].firstname.vars0_) < 1): 
                            return None
                        v = pits[0].firstname.vars0_[0]
                        pers = PersonReferent()
                        bi = MorphBaseInfo._new2388(v.gender, MorphNumber.SINGULAR, pits[0].kit.base_language)
                        bi.class0_ = MorphClass._new2344(True)
                        if (v.gender == MorphGender.MASCULINE): 
                            pers.is_male = True
                        elif (v.gender == MorphGender.FEMINIE): 
                            pers.is_female = True
                        for s in pr.slots: 
                            if (s.type_name == PersonReferent.ATTR_LASTNAME): 
                                str0_ = Utils.asObjectOrNull(s.value, str)
                                str0 = MorphologyService.get_wordform(str0_, bi)
                                pers.add_slot(s.type_name, str0, False, 0)
                                if (str0 != str0_): 
                                    pers.add_slot(s.type_name, str0_, False, 0)
                        if (len(pers.slots) == 0): 
                            return None
                        pers.add_slot(PersonReferent.ATTR_FIRSTNAME, v.value, False, 0)
                        return PersonHelper._create_referent_token(pers, pits[0].begin_token, pits[0].end_token, pits[0].firstname.morph, attrs, for_attribute, after_be_predicate)
                attr = (attrs[len(attrs) - 1] if attrs is not None and len(attrs) > 0 else None)
                if ((attr is not None and attr.prop_ref is not None and attr.prop_ref.kind == PersonPropertyKind.KIN) and attr.gender != MorphGender.UNDEFINED): 
                    vvv = attr.prop_ref.get_slot_value(PersonPropertyReferent.ATTR_REF)
                    pr = Utils.asObjectOrNull(vvv, PersonReferent)
                    if (isinstance(vvv, ReferentToken)): 
                        pr = (Utils.asObjectOrNull(vvv.referent, PersonReferent))
                    if (pr is not None): 
                        pers = PersonReferent()
                        bi = MorphBaseInfo._new2390(MorphNumber.SINGULAR, attr.gender, attr.kit.base_language)
                        bi.class0_ = MorphClass._new2344(True)
                        for s in pr.slots: 
                            if (s.type_name == PersonReferent.ATTR_LASTNAME): 
                                sur = Utils.asObjectOrNull(s.value, str)
                                sur0 = MorphologyService.get_wordform(sur, bi)
                                pers.add_slot(s.type_name, sur0, False, 0)
                                if (sur0 != sur): 
                                    pers.add_slot(s.type_name, sur, False, 0)
                        v = pits[0].firstname.vars0_[0]
                        pers.add_slot(PersonReferent.ATTR_FIRSTNAME, v.value, False, 0)
                        if (attr.gender == MorphGender.MASCULINE): 
                            pers.is_male = True
                        elif (attr.gender == MorphGender.FEMINIE): 
                            pers.is_female = True
                        return PersonHelper._create_referent_token(pers, pits[0].begin_token, pits[0].end_token, pits[0].firstname.morph, attrs, for_attribute, after_be_predicate)
            if (pits is not None and len(pits) == 1 and pits[0].lastname is not None): 
                if (t.morph.number == MorphNumber.PLURAL or ((t.previous is not None and ((t.previous.is_value("БРАТ", None) or t.previous.is_value("СЕСТРА", None)))))): 
                    t1 = pits[0].end_token.next0_
                    if (t1 is not None and ((t1.is_char(':') or t1.is_hiphen))): 
                        t1 = t1.next0_
                    pits1 = PersonItemToken.try_attach_list(t1, pattr, 10)
                    if (pits1 is not None and len(pits1) == 1): 
                        pits.extend(pits1)
                    elif (pits1 is not None and len(pits1) == 2 and pits1[1].middlename is not None): 
                        pits.extend(pits1)
            if (mi.case_.is_undefined): 
                if (pits[0].is_newline_before and pits[len(pits) - 1].end_token.is_newline_after): 
                    mi.case_ = MorphCase.NOMINATIVE
            if (len(pits) == 1): 
                pass
            if (for_attribute and len(pits) > 1): 
                tmp = list()
                pit0 = None
                i = 0
                while i < len(pits): 
                    tmp.append(pits[i])
                    pit = PersonIdentityToken.try_attach_onto_int(tmp, 0, mi, ad.local_ontology)
                    if (pit is not None): 
                        pit0 = pit
                    i += 1
                if (pit0 is not None): 
                    return PersonHelper._create_referent_token(pit0.ontology_person, pit0.begin_token, pit0.end_token, pit0.morph, attrs, for_attribute, after_be_predicate)
            i = 0
            while (i < len(pits)) and (i < 3): 
                pit = PersonIdentityToken.try_attach_onto_int(pits, i, mi, ad.local_ontology)
                if (pit is not None): 
                    return PersonHelper._create_referent_token(pit.ontology_person, pit.begin_token, pit.end_token, pit.morph, (attrs if pit.begin_token == pits[0].begin_token else None), for_attribute, after_be_predicate)
                i += 1
            if (len(pits) == 1 and not for_ext_ontos and attrs is None): 
                pp = PersonIdentityToken.try_attach_onto_for_single(pits[0], ad.local_ontology)
                if (pp is not None): 
                    return PersonHelper._create_referent_token(pp, pits[0].begin_token, pits[0].end_token, pits[0].morph, attrs, for_attribute, after_be_predicate)
            if ((len(pits) == 1 and not for_ext_ontos and attrs is not None) and pits[0].chars.is_latin_letter and attrs[0].chars.is_latin_letter): 
                pp = PersonIdentityToken.try_attach_latin_surname(pits[0], ad.local_ontology)
                if (pp is not None): 
                    return PersonHelper._create_referent_token(pp, pits[0].begin_token, pits[0].end_token, pits[0].morph, attrs, for_attribute, after_be_predicate)
            if (len(pits) == 2 and not for_ext_ontos): 
                pp = PersonIdentityToken.try_attach_onto_for_duble(pits[0], pits[1])
                if (pp is not None): 
                    return PersonHelper._create_referent_token(pp, pits[0].begin_token, pits[1].end_token, pits[0].morph, attrs, for_attribute, after_be_predicate)
            if (pits[0].begin_token.kit.ontology is not None): 
                i = 0
                while i < len(pits): 
                    pit = PersonIdentityToken.try_attach_onto_ext(pits, i, mi, pits[0].begin_token.kit.ontology)
                    if (pit is not None): 
                        return PersonHelper._create_referent_token(pit.ontology_person, pit.begin_token, pit.end_token, pit.morph, attrs, for_attribute, after_be_predicate)
                    i += 1
            pli0 = PersonIdentityToken.try_attach(pits, 0, mi, t0, is_king, attrs is not None)
            if (len(pli0) > 0 and pli0[0].typ == FioTemplateType.NAMESURNAME): 
                if ((attrs is not None and len(attrs) > 0 and attrs[len(attrs) - 1].begin_token == attrs[len(attrs) - 1].end_token) and attrs[len(attrs) - 1].begin_token.chars.is_capital_upper): 
                    if (pits[1].lastname is not None and pits[1].middlename is None): 
                        pass
                    else: 
                        pits1 = PersonItemToken.try_attach_list(attrs[len(attrs) - 1].begin_token, pattr, 10)
                        if (pits1 is not None and pits1[0].lastname is not None): 
                            pli11 = PersonIdentityToken.try_attach(pits1, 0, mi, t0, is_king, len(attrs) > 1)
                            if ((pli11 is not None and len(pli11) > 0 and pli11[0].coef > 1) and pli11[0].end_token == pli0[0].end_token): 
                                pli0 = pli11
                                del attrs[len(attrs) - 1]
                                if (len(attrs) == 0): 
                                    attrs = (None)
            if (t.previous is None and ((ad is not None and ad.text_starts_with_lastname_firstname_middlename)) and len(pits) == 3): 
                exi = False
                for pit in pli0: 
                    if (pit.typ == FioTemplateType.SURNAMENAMESECNAME): 
                        pit.coef += (10)
                        exi = True
                if (not exi): 
                    pit = PersonIdentityToken.create_typ(pits, FioTemplateType.SURNAMENAMESECNAME, mi)
                    if (pit is not None): 
                        pit.coef = (10)
                        pli0.append(pit)
            if (for_ext_ontos): 
                te = False
                if (pli0 is None or len(pli0) == 0): 
                    te = True
                else: 
                    PersonIdentityToken.sort(pli0)
                    if (pli0[0].coef < 2): 
                        te = True
                if (te): 
                    pli0 = PersonIdentityToken.try_attach_for_ext_onto(pits)
            if (for_ext_ontos and pli0 is not None): 
                et = pits[len(pits) - 1].end_token
                for pit in pli0: 
                    if (pit.end_token == et): 
                        pit.coef += (1)
            pli = pli0
            pli1 = None
            if (not for_ext_ontos and ((attrs is None or attrs[len(attrs) - 1].typ == PersonAttrTerminType.POSITION))): 
                if ((len(pits) == 4 and pits[0].firstname is not None and pits[1].firstname is None) and pits[2].firstname is not None and pits[3].firstname is None): 
                    pass
                elif (pli0 is not None and len(pli0) > 0 and pli0[0].typ == FioTemplateType.ARABICLONG): 
                    pass
                else: 
                    pli1 = PersonIdentityToken.try_attach(pits, 1, mi, t0, is_king, attrs is not None)
                    if (pli0 is not None and pli1 is not None and len(pli1) > 0): 
                        PersonIdentityToken.correctxfml(pli0, pli1, attrs)
            if (pli is None): 
                pli = pli1
            elif (pli1 is not None): 
                pli.extend(pli1)
            if (((pli is None or len(pli) == 0)) and len(pits) == 1 and pits[0].firstname is not None): 
                if (is_king): 
                    first = PersonIdentityToken(pits[0].begin_token, pits[0].end_token)
                    PersonIdentityToken.manage_firstname(first, pits[0], mi)
                    first.coef = (2)
                    if (first.morph.gender == MorphGender.UNDEFINED and first.firstname is not None): 
                        first.morph.gender = first.firstname.gender
                    pli.append(first)
                elif (attrs is not None): 
                    for a in attrs: 
                        if (a.can_be_same_surname and a.referent is not None): 
                            pr0 = Utils.asObjectOrNull(a.referent.get_slot_value(PersonPropertyReferent.ATTR_REF), PersonReferent)
                            if (pr0 is not None): 
                                first = PersonIdentityToken(pits[0].begin_token, pits[0].end_token)
                                PersonIdentityToken.manage_firstname(first, pits[0], mi)
                                first.coef = (2)
                                pli.append(first)
                                first.lastname = PersonMorphCollection()
                                for v in pr0.slots: 
                                    if (v.type_name == PersonReferent.ATTR_LASTNAME): 
                                        first.lastname.add(v.value, None, (MorphGender.MASCULINE if pr0.is_male else ((MorphGender.FEMINIE if pr0.is_female else MorphGender.UNDEFINED))), True)
            if ((((pli is None or len(pli) == 0)) and len(pits) == 1 and pits[0].lastname is not None) and attrs is not None and not pits[0].is_in_dictionary): 
                for a in attrs: 
                    if (a.prop_ref is not None and ((a.typ == PersonAttrTerminType.PREFIX or a.prop_ref.kind == PersonPropertyKind.BOSS))): 
                        mc = pits[0].begin_token.get_morph_class_in_dictionary()
                        if (not mc.is_proper): 
                            break
                        last = PersonIdentityToken(pits[0].begin_token, pits[0].end_token)
                        PersonIdentityToken.manage_lastname(last, pits[0], mi)
                        last.coef = (2)
                        pli.append(last)
                        break
            if (pli is not None and len(pli) > 0): 
                PersonIdentityToken.sort(pli)
                best = pli[0]
                min_coef = 2
                if ((best.coef < min_coef) and ((attrs is not None or for_ext_ontos))): 
                    pit = PersonIdentityToken.try_attach_identity(pits, mi)
                    if (pit is not None and pit.coef > best.coef and pit.coef > 0): 
                        pers = PersonReferent()
                        pers._add_identity(pit.lastname)
                        return PersonHelper._create_referent_token(pers, pit.begin_token, pit.end_token, pit.morph, attrs, for_attribute, after_be_predicate)
                    if ((best.kit.base_language.is_en and best.typ == FioTemplateType.NAMESURNAME and attrs is not None) and attrs[0].typ == PersonAttrTerminType.BESTREGARDS): 
                        best.coef += (10)
                    if (best.coef >= 0): 
                        best.coef += ((1 if best.chars.is_all_upper else 2))
                if (best.coef >= 0 and (best.coef < min_coef)): 
                    tee = best.end_token.next0_
                    tee1 = None
                    if (tee is not None and tee.is_char('(')): 
                        br = BracketHelper.try_parse(tee, BracketParseAttr.NO, 100)
                        if (br is not None and (br.length_char < 100)): 
                            tee1 = br.begin_token.next0_
                            tee = br.end_token.next0_
                    if (isinstance(tee, TextToken)): 
                        if (tee.is_char_of(":,") or tee.is_hiphen or tee.is_verb_be): 
                            tee = tee.next0_
                    att = PersonAttrToken.try_attach(tee, PersonAttrToken.PersonAttrAttachAttrs.NO)
                    if (att is None and tee1 is not None): 
                        att = PersonAttrToken.try_attach(tee1, PersonAttrToken.PersonAttrAttachAttrs.NO)
                    if (att is not None): 
                        if (tee == best.end_token.next0_ and not att.morph.case_.is_nominative and not att.morph.case_.is_undefined): 
                            pass
                        else: 
                            best.coef += (2)
                    elif (tee is not None and tee.is_value("АГЕНТ", None)): 
                        best.coef += (1)
                    if (for_attribute): 
                        best.coef += (1)
                if ((len(pits) >= 3 and best.typ == FioTemplateType.IISURNAME and (best.coef < min_coef)) and best.coef > 1 and pits[2].value is not None): 
                    aaa = ad.local_ontology.try_attach(pits[2].begin_token, None, False)
                    if (aaa is not None and len(aaa) > 0): 
                        best.coef += (1)
                if (((best.coef >= 0 and (best.coef < min_coef) and attrs is None) and best.begin_token.previous is not None and best.begin_token.previous.is_comma_and) and (isinstance(best.begin_token.previous.previous, ReferentToken))): 
                    ppp = Utils.asObjectOrNull(best.begin_token.previous.previous.get_referent(), PersonReferent)
                    if (ppp is not None and ppp._m_person_identity_typ == best.typ): 
                        best.coef += (1)
                if (best.coef >= min_coef): 
                    i = 0
                    gender = MorphGender.UNDEFINED
                    i = 0
                    while i < len(pli): 
                        if (pli[i].coef != best.coef): 
                            del pli[i:i+len(pli) - i]
                            break
                        elif (pli[i].probable_gender != MorphGender.UNDEFINED): 
                            gender = (Utils.valToEnum((gender) | (pli[i].probable_gender), MorphGender))
                        i += 1
                    if (len(pli) > 1): 
                        return None
                    if (gender != MorphGender.FEMINIE and gender != MorphGender.MASCULINE): 
                        if ((pli[0].is_newline_before and pli[0].is_newline_after and pli[0].lastname is not None) and pli[0].lastname.has_lastname_standard_tail): 
                            if (len(pli[0].lastname.values) == 2): 
                                ok = True
                                cou = 100
                                sur = pli[0].lastname.items[0].value
                                ttt = pli[0].end_token.next0_
                                first_pass3011 = True
                                while True:
                                    if first_pass3011: first_pass3011 = False
                                    else: ttt = ttt.next0_; cou -= 1
                                    if (not (ttt is not None and cou > 0)): break
                                    if (step > 0): 
                                        break
                                    if (not ttt.is_value(sur, None)): 
                                        continue
                                    pr = PersonAnalyzer._try_attach_person(ttt, for_ext_ontos, step, False)
                                    if (pr is not None and not pr.referent.is_female): 
                                        ok = False
                                    break
                                if (ok): 
                                    pli[0].lastname.remove(None, MorphGender.MASCULINE)
                                    gender = MorphGender.FEMINIE
                                    if (pli[0].firstname is not None and len(pli[0].firstname.values) == 2): 
                                        pli[0].firstname.remove(None, MorphGender.MASCULINE)
                    if (gender == MorphGender.UNDEFINED): 
                        if (pli[0].firstname is not None and pli[0].lastname is not None): 
                            g = pli[0].firstname.gender
                            if (pli[0].lastname.gender != MorphGender.UNDEFINED): 
                                g = (Utils.valToEnum((g) & (pli[0].lastname.gender), MorphGender))
                            if (g == MorphGender.FEMINIE or g == MorphGender.MASCULINE): 
                                gender = g
                            elif (pli[0].firstname.gender == MorphGender.MASCULINE or pli[0].firstname.gender == MorphGender.FEMINIE): 
                                gender = pli[0].firstname.gender
                            elif (pli[0].lastname.gender == MorphGender.MASCULINE or pli[0].lastname.gender == MorphGender.FEMINIE): 
                                gender = pli[0].lastname.gender
                    pers = PersonReferent()
                    if (gender == MorphGender.MASCULINE): 
                        pers.is_male = True
                    elif (gender == MorphGender.FEMINIE): 
                        pers.is_female = True
                    for v in pli: 
                        if (v.ontology_person is not None): 
                            for s in v.ontology_person.slots: 
                                pers.add_slot(s.type_name, s.value, False, 0)
                        elif (v.typ == FioTemplateType.ASIANNAME or v.typ == FioTemplateType.ARABICLONG): 
                            pers._add_identity(v.lastname)
                        else: 
                            pers._add_fio_identity(v.lastname, v.firstname, v.middlename)
                            if (v.typ == FioTemplateType.ASIANSURNAMENAME): 
                                pers.add_slot("NAMETYPE", "china", False, 0)
                    if (not for_ext_ontos): 
                        pers._m_person_identity_typ = pli[0].typ
                    if (pli[0].begin_token != pits[0].begin_token and attrs is not None): 
                        if (pits[0].whitespaces_before_count > 2): 
                            attrs = (None)
                        else: 
                            s = pits[0].get_source_text()
                            pat = attrs[len(attrs) - 1]
                            if (pat.typ == PersonAttrTerminType.POSITION and not Utils.isNullOrEmpty(s) and not pat.is_newline_before): 
                                if (pat.value is None and pat.prop_ref is not None): 
                                    while pat is not None: 
                                        if (pat.prop_ref is None): 
                                            break
                                        elif (pat.higher_prop_ref is None): 
                                            str0_ = s.lower()
                                            if (pat.prop_ref.name is not None and not LanguageHelper.ends_with(pat.prop_ref.name, str0_)): 
                                                pat.prop_ref.name = pat.prop_ref.name + (" " + str0_)
                                            if (pat.add_outer_org_as_ref): 
                                                pat.prop_ref.add_slot(PersonPropertyReferent.ATTR_REF, None, True, 0)
                                                pat.add_outer_org_as_ref = False
                                            break
                                        pat = pat.higher_prop_ref
                                elif (pat.value is not None): 
                                    pat.value = "{0} {1}".format(pat.value, s.lower())
                                pat.end_token = pits[0].end_token
                    latin = PersonIdentityToken.check_latin_after(pli[0])
                    if (latin is not None): 
                        pers._add_fio_identity(latin.lastname, latin.firstname, latin.middlename)
                    return PersonHelper._create_referent_token(pers, pli[0].begin_token, (latin.end_token if latin is not None else pli[0].end_token), pli[0].morph, attrs, for_attribute, after_be_predicate)
        if (attrs is not None): 
            attr = attrs[len(attrs) - 1]
            if (attr.can_be_single_person and attr.prop_ref is not None): 
                return ReferentToken._new956(attr.prop_ref, attr.begin_token, attr.end_token, attr.morph)
        return None
    
    def process_ontology_item(self, begin : 'Token') -> 'ReferentToken':
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        if (begin is None): 
            return None
        rt = PersonAnalyzer._try_attach_person(begin, True, -1, False)
        if (rt is None): 
            pat = PersonAttrToken.try_attach(begin, PersonAttrToken.PersonAttrAttachAttrs.NO)
            if (pat is not None and pat.prop_ref is not None): 
                return ReferentToken(pat.prop_ref, pat.begin_token, pat.end_token)
            return None
        t = rt.end_token.next0_
        while t is not None: 
            if (t.is_char(';') and t.next0_ is not None): 
                rt1 = PersonAnalyzer._try_attach_person(t.next0_, True, -1, False)
                if (rt1 is not None and rt1.referent.type_name == rt.referent.type_name): 
                    rt.referent.merge_slots(rt1.referent, True)
                    rt.end_token = rt1.end_token
                    t = rt.end_token
                elif (rt1 is not None): 
                    t = rt1.end_token
            t = t.next0_
        return rt
    
    __m_inited = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        from pullenti.ner.person.internal.PersonPropAnalyzer import PersonPropAnalyzer
        from pullenti.ner.person.internal.PersonIdToken import PersonIdToken
        from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
        if (PersonAnalyzer.__m_inited): 
            return
        PersonAnalyzer.__m_inited = True
        try: 
            MetaPerson.initialize()
            MetaPersonIdentity.initialize()
            MetaPersonProperty.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            PersonItemToken._initialize()
            PersonAttrToken.initialize()
            ShortNameHelper.initialize()
            PersonIdToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
            MailLine.initialize()
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        ProcessorService.register_analyzer(PersonAnalyzer())
        ProcessorService.register_analyzer(PersonPropAnalyzer())