#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buduje i18n do v2 index.html: keyuje template ({{ t.tN }}), injektuje STRINGS + lang stav
+ prepinac + RTL do builder frameworku. Stage 1: CZ + EN (machinery). Dalsi jazyky se doplni do TRANS."""
import re, json, sys, os
_B = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_B)

SRC = os.path.join(_REPO, '.source.html')
OUT = sys.argv[1] if len(sys.argv) > 1 else SRC
TM  = json.load(open(os.path.join(_B, 'TM.json'), encoding='utf-8'))

# ---- Keyovane retezce: (cs_source, key). Poradi nerozhoduje. ----
# Brand/vlastni jmena/cisla se NEKEYUJI (zustavaji literal): headofai, .cz, Vesely.ai, VeselyLab.com,
# OmegaTeam.ai, hello@headofai.cz, @headofaicz, David VeselY, agent names, CIPHER pismena, ICO/DIC.
K = {}
def k(key, cs, en, sk=None, de=None, uk=None, ar=None):
    K[cs] = key
    d = {'cs': cs, 'en': en}
    if sk: d['sk']=sk
    if de: d['de']=de
    if uk: d['uk']=uk
    if ar: d['ar']=ar
    TRANS[key] = d

TRANS = {}

# NAV
k('t_nav_problem','Problém','Problem')
k('t_nav_solution','Řešení a cena','Approach & pricing')
k('t_nav_about','O mně','About')
k('t_nav_cta','Objednat call','Book a call')

# HERO
k('t_hero_eyebrow','Fractional Head of AI / CAIO','Fractional Head of AI / CAIO')
k('t_hero_h1a','AI už ve vaší firmě běží.','AI is already running in your company.')
k('t_hero_h1b','Převezměte nad ní kontrolu.','Take control of it.')
k('t_hero_after','Po 90 dnech','After 90 days')
k('t_hero_sub','AI má jasného vlastníka, schválená pravidla, prioritizované portfolio a první nasazení s měřeným dopadem.','AI has a clear owner, approved rules, a prioritized portfolio and a first deployment with measured impact.')
k('t_hero_cta','Objednat AI Leadership Call →','Book an AI Leadership Call →')
k('t_hero_note','30 min · bez prodejní prezentace','30 min · no sales pitch')
# hero stats
k('t_stat1_k','k prvnímu měřenému provozu','to first measured production')
k('t_stat2_v','1–3 priority','1–3 priorities')
k('t_stat2_k','místo desítek experimentů','instead of dozens of experiments')
k('t_stat3_v','1 vlastník','1 owner')
k('t_stat3_k','jasná odpovědnost','clear accountability')
k('t_stat4_v','Měřený dopad','Measured impact')
k('t_stat4_k','tržby, náklady nebo riziko','revenue, cost or risk')
k('t_unit_days','90 dní','90 days')

# 01 PROBLEM
# t_p_eyebrow zruseno — eyebrow "Problém" reuse t_nav_problem (bez cisla)
k('t_p_h2','AI aktivita není AI výkon.','AI activity is not AI performance.')
k('t_p1_h','AI bez vlastníka','AI with no owner')
k('t_p1_b','Vzniká po odděleních, ale nikdo ji neřídí jako firemní schopnost.','It grows across departments, but no one runs it as a company capability.')
k('t_p2_h','Aktivita bez P&amp;L','Activity without P&amp;L')
k('t_p2_b','Měří se počet nástrojů a promptů — ne tržby, náklad, rychlost a uvolněná kapacita.','You measure tools and prompts — not revenue, cost, speed and freed capacity.')
k('t_p3_h','Riziko bez hranic','Risk without limits')
k('t_p3_b','Data, odpovědnost a lidská kontrola zůstávají nejasné. Povinnost AI gramotnosti zaměstnanců přitom platí už od února 2025 — a od srpna 2026 se začíná vymáhat.','Data, accountability and human oversight remain unclear. Meanwhile, the AI literacy duty for employees has applied since February 2025 — with enforcement starting August 2026.','Dáta, zodpovednosť a ľudská kontrola zostávajú nejasné. Povinnosť AI gramotnosti zamestnancov pritom platí už od februára 2025 — a od augusta 2026 sa začína vymáhať.','Daten, Verantwortlichkeit und menschliche Kontrolle bleiben ungeklärt. Die KI-Kompetenzpflicht für Mitarbeiter gilt derweil bereits seit Februar 2025 — mit Durchsetzung ab August 2026.',"Дані, відповідальність і людський контроль залишаються невизначеними. Водночас обов'язок AI-грамотності працівників діє вже з лютого 2025 — а з серпня 2026 починається його примус.",'تبقى البيانات والمسؤولية والرقابة البشرية غير واضحة. وفي الوقت نفسه، يسري واجب الإلمام بالذكاء الاصطناعي للموظفين منذ فبراير 2025 — مع بدء الإنفاذ في أغسطس 2026.')
k('t_p4_h','Pokrok bez orientace','Progress without direction')
k('t_p4_b','Možnosti AI rostou rychleji, než se v nich firmy dokážou zorientovat.','AI capabilities grow faster than companies can keep up with.')

# 02 SOLUTION
# t_s_eyebrow zruseno — eyebrow "Řešení a cena" reuse t_nav_solution (bez cisla)
k('t_s_h2','Z chaosu do řízeného výkonu. Čtyři kroky.','From chaos to managed performance. Four steps.')
k('t_s_lead','Neprodávám audit do šuplíku ani izolovaný chatbot. Na prvních 90 dní přebírám mandát k řízení AI agendy — od rozhodnutí po provoz. Krok 1 je zdarma, kroky 2–3 tvoří fixní 90denní sprint, krok 4 je volitelné pokračování.','I don\'t sell a shelved audit or an isolated chatbot. For the first 90 days I take the mandate to run your AI agenda — from decision to operation. Step 1 is free, steps 2–3 form the fixed 90-day sprint, step 4 is optional continuation.')
# t_s_result zruseno (odebrano ze stranky)
# step 1
k('t_st1_title','AI Leadership Call','AI Leadership Call')
k('t_st1_tag','Vstup','Entry')
k('t_st1_meta','30 minut · bez přípravy · přímo s Davidem Veselým','30 minutes · no prep · directly with David Veselý')
k('t_st1_body','Rozhodovací call, ne prodejní prezentace. Pojmenujeme problém, ověříme fit — a řekneme si na rovinu, jestli dává smysl pokračovat.','A decision call, not a sales pitch. We name the problem, check the fit — and say honestly whether it makes sense to continue.')
k('t_st1_cta','Objednat call →','Book a call →')
# step 2 CIPHER
k('t_st2_title','Diagnostika — CIPHER Snapshot','Diagnosis — CIPHER Snapshot')
k('t_st2_tag','90denní sprint · Týdny 1–3','90-day sprint · Weeks 1–3')
k('t_st2_body','Nejde o checklist ani technologický audit. Každý AI use case posuzuji přes šest napětí připravenosti — výsledkem je mapa, kde je ekonomická páka, kde riziko a kdo musí rozhodovat.','No checklist, no technology audit. I assess every AI use case through six readiness tensions — the result is a map of where the economic leverage is, where the risk is and who must decide.')
k('t_cip1_h','Má tým úsudek poznat, kde AI pomůže a kde škodí?','Does the team have the judgment to tell where AI helps and where it hurts?')
k('t_cip2_h','Je problém dobře vymezený a máte k němu data?','Is the problem well defined and do you have the data for it?')
k('t_cip3_h','Umíte záměr přeložit do zadání, které jde postavit?','Can you translate intent into a spec that can actually be built?')
k('t_cip4_h','Kde pracuje AI — a kde musí zůstat člověk a kontrola?','Where does AI work — and where must the human and control remain?')
k('t_cip5_h','Kdo rozhoduje, kdo nese odpovědnost, kde jsou hranice?','Who decides, who is accountable, where are the limits?')
k('t_cip6_h','Stačí lidé, rozpočet a nejmenší dostatečné řešení?','Are the people, budget and smallest-sufficient solution enough?')
k('t_cip_cite_a','Vychází z frameworku CIPHER (Armanios &amp; Tucci, 2025) —','Based on the CIPHER framework (Armanios &amp; Tucci, 2025) —')
k('t_cip_cite_link','open-access paper ↗','open-access paper ↗')
k('t_cip_cite_b','. Výstupem je','. The output is')
k('t_cip_cite_c',': mapa připravenosti a doporučení pilot / odklad / stop.',': a readiness map and a pilot / defer / stop recommendation.')
# step 3 deploy
k('t_st3_title','Nasazení AI pracovníků','Deploying AI workers')
k('t_st3_tag','90denní sprint · Týdny 3–12','90-day sprint · Weeks 3–12')
k('t_st3_body','Priority, metriky, governance a vendor-neutral architektura — a poté 3+ prioritní AI pracovníci v pilotu nebo provozu, včetně kontroly a měření dopadu. Níže příklady seskupené podle výsledku; skutečný scope vychází z CIPHER Snapshotu.','Priorities, metrics, governance and a vendor-neutral architecture — then 3+ priority AI workers in pilot or production, including control and impact measurement. Examples below are grouped by outcome; the real scope comes from the CIPHER Snapshot.')
k('t_cat_rev','Zvýšení tržeb','Growing revenue')
k('t_cat_cost','Snížení provozních nákladů','Cutting operating cost')
k('t_cat_risk','Omezení rizika a závislosti na lidech','Reducing risk and key-person dependence')
# operator descriptions + impacts
k('t_op1_b','Přivítá návštěvníka, rozpozná záměr, kvalifikuje ho a dovede k rezervaci nebo nákupu.','Greets the visitor, detects intent, qualifies them and leads to a booking or purchase.')
k('t_op1_i','↗ vyšší konverze webu','↗ higher website conversion')
k('t_op2_b','Nepřetržitě přijímá hovory, kvalifikuje poptávku a rezervuje schůzky.','Answers calls around the clock, qualifies demand and books meetings.')
k('t_op2_i','↗ méně zmeškaných hovorů','↗ fewer missed calls')
k('t_op3_b','Zpracovává a kvalifikuje poptávky z formulářů, e-mailu a DM, hned předává obchodu.','Processes and qualifies inquiries from forms, e-mail and DMs, hands them to sales instantly.')
k('t_op3_i','↗ reakce do minut','↗ response in minutes')
k('t_op4_b','Řídí retenci, obnovu smluv, cross-sell a upsell u stávajících zákazníků.','Runs retention, renewals, cross-sell and upsell with existing customers.')
k('t_op4_i','↗ nižší churn, vyšší LTV','↗ lower churn, higher LTV')
k('t_op5_b','Zpracovává e-maily, faktury, smlouvy a objednávky bez ručního přepisování.','Processes e-mails, invoices, contracts and orders without manual re-keying.')
k('t_op5_i','↗ hodiny administrativy zpět','↗ admin hours back')
k('t_op6_b','Řeší zákaznickou podporu, na člověka eskaluje jen výjimky.','Handles customer support, escalates only exceptions to a human.')
k('t_op6_i','↗ dostupnost 24/7','↗ 24/7 availability')
k('t_op7_b','Hlídá pohledávky, páruje platby a rozesílá upomínky.','Watches receivables, matches payments and sends reminders.')
k('t_op7_i','↗ nižší DSO','↗ lower DSO')
k('t_op8_b','Odhaluje nevyfakturované výkony, chybné ceny a úniky marže.','Uncovers unbilled work, pricing errors and margin leaks.')
k('t_op8_i','↗ vyšší marže','↗ higher margin')
k('t_op9_b','Odpovídá podle směrnic a spouští HR/IT procesy.','Answers per internal policy and triggers HR/IT processes.')
k('t_op9_i','↗ méně dotazů na HR a IT','↗ fewer HR and IT tickets')
# sprint result / pricing
k('t_spr_result_head','Výsledek sprintu · 90 dní','Sprint outcome · 90 days')
k('t_spr_result_h','AI má vlastníka, pravidla a první prokazatelný výkon.','AI has an owner, rules and first provable performance.')
k('t_spr_result_b1','Do realizace jdeme jen tehdy, pokud očekávaný roční dopad výrazně převyšuje investici. Když čísla nevycházejí, doporučím projekt zastavit.','We only proceed to build if the expected annual impact clearly exceeds the investment. If the numbers don\'t add up, I\'ll recommend stopping the project.')
k('t_spr_result_b2','Interní Head of AI vás první rok stojí miliony a půl roku náboru — sprint dodá výsledky za jedno čtvrtletí.','An in-house Head of AI costs you millions and half a year of hiring in year one — the sprint delivers results in a single quarter.')
k('t_spr_cta','Ověřit fit →','Check the fit →')
# retainer
k('t_ret_title','Fractional AI Retainer','Fractional AI Retainer')
k('t_ret_tag','Volitelné · Po sprintu','Optional · After the sprint')
k('t_ret_per','/ měsíc','/ month')
k('t_sprint_per','/ 90 dní bez DPH','/ 90 days excl. VAT','/ 90 dní bez DPH','/ 90 Tage zzgl. MwSt.','/ 90 днів без ПДВ','/ ٩٠ يومًا غير شامل الضريبة')
k('t_call_result_label','Výsledek callu','Call outcome','Výsledok callu','Ergebnis des Calls','Результат дзвінка','نتيجة المكالمة')
k('t_call_result_h','Jasné rozhodnutí, jestli pokračovat — a jestli jste fit.','A clear decision on whether to continue — and whether you are a fit.','Jasné rozhodnutie, či pokračovať — a či ste fit.','Eine klare Entscheidung, ob es weitergeht — und ob Sie passen.','Чітке рішення, чи продовжувати — і чи ви підходите.','قرار واضح بشأن الاستمرار — وما إذا كنتم مناسبين.')
# t_call_result_note zruseno (poznamka nahrazena fit/nefit listy)
k('t_ret_result_label','Výsledek','Outcome','Výsledok','Ergebnis','Результат','النتيجة')
k('t_ret_result_h','Průběžně řízený výkon a měřený dopad.','Continuously managed performance and measured impact.','Priebežne riadený výkon a meraný dopad.','Laufend gesteuerte Leistung und gemessene Wirkung.','Постійно керований результат і виміряний вплив.','أداء مُدار باستمرار وأثر مقاس.')
k('t_ret_body','Průběžné řízení AI agendy jako externí Head of AI: portfolio iniciativ, vendoři, adopce a board reporting. Pokračujeme, jen pokud sprint prokázal hodnotu.','Ongoing management of the AI agenda as your fractional Head of AI: initiative portfolio, vendors, adoption and board reporting. We continue only if the sprint proved its value.')

# 03 FIT

# 04 ABOUT
k('t_ab_eyebrow','Kdo za tím stojí','Who stands behind it')
k('t_ab_role','Zakladatel · Vesely.ai s.r.o. · fractional CAIO','Founder · Vesely.ai s.r.o. · fractional CAIO','Zakladateľ · Vesely.ai s.r.o. · fractional CAIO','Gründer · Vesely.ai s.r.o. · fractional CAIO','Засновник · Vesely.ai s.r.o. · fractional CAIO','المؤسس · Vesely.ai s.r.o. · fractional CAIO')
k('t_ab_p1','Pomáhám vedení firem dostat AI pod kontrolu: určit priority, nastavit governance, nasadit první AI pracovníky a měřit jejich skutečný dopad.','I help company leadership get AI under control: set priorities, establish governance, deploy the first AI workers and measure their real impact.')
k('t_ab_p2a','Doporučuji jen přístupy, které jsem si ověřil v reálném provozu nebo na vlastním kapitálu. Na platformě ','I only recommend approaches I\'ve verified myself, in real operation or with my own capital. On the ')
k('t_ab_p2b',' provozuji AI pracovníky v produkčním nasazení. Ve venture studiu ',' platform I run AI workers in production. In the ')
k('t_ab_p2c',' ověřuji, které automatizované byznysy obstojí proti skutečné poptávce a cashflow. Akvizici mi řídí autonomní tým AI agentů ',' venture studio I test which automated businesses hold up against real demand and cash flow. My acquisition is run by an autonomous team of AI agents, ')
k('t_ab_p3','Nehraji za dodavatele. Řídím vaši AI agendu tak, aby každá iniciativa obhájila návratnost nebo snížení rizika. Když čísla nevycházejí, doporučím odklad nebo zastavení. Výsledkem musí být jasné priority, měřitelné výstupy a board report místo neurčitých slibů.','I don\'t play for the vendors. I run your AI agenda so that every initiative justifies its return or risk reduction. If the numbers don\'t add up, I recommend deferring or stopping. The result must be clear priorities, measurable outputs and a board report instead of vague promises.')
k('t_ab_p4','Head of AI bude v příští dekádě klíčová role pro přežití a úspěch firem — a někdo ji ve vaší firmě bude držet. Jako bývalý voják vím, že strategická výšina se obsazuje dřív, než o ni začne boj. Proto držím headofai.cz.','Head of AI will be a role critical to companies\' survival and success in the next decade — and someone will hold it in your company. As a former soldier I know the strategic high ground is taken before the fight for it begins. That\'s why I hold headofai.cz.')
k('t_ab_principles','Provozní principy','Operating principles')
k('t_pr1','Business na prvním místě. AI až na druhém.','Business first. AI second.')
k('t_pr2','Důkazy, ne hype.','Evidence, not hype.')
k('t_pr3','Malé piloty. Rychlá zpětná vazba.','Small pilots. Fast feedback.')
k('t_pr4','Stavím jen to, co vytváří měřitelnou hodnotu.','I build only what creates measurable value.')
k('t_pr5','Každý AI systém má vlastníka.','Every AI system has an owner.')
k('t_pr6','Jednoduché architektury přežijí déle.','Simple architectures survive longer.')
k('t_pr7','AI dodavatel může dodat nástroj. Nemá ale vlastnit vaši AI strategii.','An AI vendor can deliver a tool. It must not own your AI strategy.')
k('t_pr8','Neprodávám chatboty. Pomáhám vedení firem převzít kontrolu nad AI.','I don\'t sell chatbots. I help leadership take control of AI.')

# 05 CONTACT
k('t_c_eyebrow','Ne další AI workshop','Not another AI workshop')
k('t_c_h2','Rozhodovací call.','A decision call.')
k('t_c_lead','Během 30 minut zjistíme, jestli vaše firma potřebuje prvního AI pracovníka, 90denní sprint — nebo nejdřív nastavit odpovědnost.','In 30 minutes we\'ll find out whether your company needs a first AI worker, the 90-day sprint — or to set accountability first.')
k('t_c_note1','ozvu se do 24 hodin','I reply within 24 hours')
k('t_c_note2','bez prodejní prezentace','no sales pitch')
k('t_f_name','Jméno','Name')
k('t_f_role','Role ve firmě','Role in the company')
k('t_f_company','Firma','Company')
k('t_f_phone','Telefon','Phone')
k('t_f_email','E-mail','E-mail')
k('t_f_msg','Co vás dnes v souvislosti s AI nejvíc pálí?','What\'s your biggest AI pain point right now?')
k('t_f_submit','Objednat AI Leadership Call','Book an AI Leadership Call')
k('t_f_consent','Odesláním souhlasíte se zpracováním osobních údajů.','By submitting you agree to the processing of personal data.')
k('t_f_privacy','Zásady ochrany osobních údajů','Privacy policy')

# 06 FAQ
k('t_faq_eyebrow','FAQ','FAQ')
k('t_faq_h2','Časté otázky','Frequently asked questions')
k('t_faq_q1','Co bude po 90 dnech ve firmě skutečně hotové?','What will actually be done in the company after 90 days?')
k('t_faq_a1','Po 90 dnech má AI agenda jasného vlastníka, schválené priority a pravidla pro data, oprávnění a lidské schvalování. Nejméně jeden prioritní AI pracovník běží v reálném provozu s definovanými KPI. Vedení dostane přehled dosaženého dopadu a doporučení pro další období.','After 90 days the AI agenda has a clear owner, approved priorities and rules for data, permissions and human approval. At least one priority AI worker runs in real operation with defined KPIs. Leadership gets an overview of the impact achieved and a recommendation for the next period.')
k('t_faq_q2','Jakou dáváte garanci?','What guarantee do you give?')
k('t_faq_a2','Konkrétní výši úspor nebo tržeb nelze poctivě garantovat, protože závisí také na datech, procesech, lidech a rozhodnutích klienta. Garantuji sjednané výstupy, transparentní měření a jasnou rozhodovací bránu. Pokud diagnostika neodhalí příležitost, jejíž očekávaný přínos obhájí další investici, doporučím projekt zastavit. Další fáze se bez rozhodnutí klienta nerealizuje ani nefakturuje. Nesplněný sjednaný výstup dokončím bez dodatečné odměny.','A specific amount of savings or revenue can\'t be honestly guaranteed, because it also depends on the client\'s data, processes, people and decisions. I guarantee the agreed deliverables, transparent measurement and a clear decision gate. If diagnosis reveals no opportunity whose expected benefit justifies further investment, I\'ll recommend stopping. No further phase is executed or invoiced without the client\'s decision. An agreed deliverable that isn\'t met I\'ll complete at no extra charge.')
k('t_faq_q3','Kolik času a lidí budete potřebovat z naší strany?','How much time and how many people will you need from us?')
k('t_faq_a3','CEO nebo člen vedení je potřeba při zahájení, prioritizaci a klíčových rozhodnutích. Průběžně spolupracuji s jedním interním garantem a vlastníky dotčených procesů. Nevytvářím zbytečnou pracovní skupinu ani nekonečnou sérii workshopů. Konkrétní časovou náročnost stanovíme před každou fází.','The CEO or a leadership member is needed at kickoff, prioritization and key decisions. Day to day I work with one internal sponsor and the owners of the processes involved. I don\'t create a needless task force or an endless series of workshops. We set the specific time demand before each phase.')
k('t_faq_q4','Je to poradenství, implementace, nebo dočasná náhrada interního Head of AI?','Is it consulting, implementation, or a temporary stand-in for an in-house Head of AI?')
k('t_faq_a4','Jde o dočasný exekutivní mandát. Neodevzdávám pouze prezentaci: určím priority, navrhnu architekturu, nastavím pravidla a řídím první produkční nasazení. Nenahrazuji interní IT ani neobcházím jeho odpovědnost. Po 90 dnech lze agendu předat internímu vlastníkovi, pokračovat formou Fractional Head of AI nebo připravit nábor interního vedoucího. Dokumentace, data, účty a integrace zůstávají klientovi.','It\'s a temporary executive mandate. I don\'t just hand over a deck: I set priorities, design the architecture, establish rules and run the first production deployment. I don\'t replace internal IT or bypass its responsibility. After 90 days the agenda can be handed to an internal owner, continued as a Fractional Head of AI, or used to prepare hiring an in-house lead. Documentation, data, accounts and integrations stay with the client.')
k('t_faq_q5','Jak řešíte bezpečnost dat a odpovědnost AI pracovníků?','How do you handle data security and the accountability of AI workers?')
k('t_faq_a5','Každé nasazení má interního vlastníka, definovaná oprávnění, auditovatelný provoz a pravidla lidského schvalování. Používáme minimální oprávnění, minimalizaci předávaných dat, kontrolované fallbacky a možnost zásah vrátit. Do produkce nejde systém, u něhož není jasné, kdo odpovídá za jeho rozhodnutí a výstupy.','Every deployment has an internal owner, defined permissions, auditable operation and human-approval rules. We use least privilege, minimize the data passed, use controlled fallbacks and keep every action reversible. No system goes to production if it isn\'t clear who is accountable for its decisions and outputs.')
k('t_faq_q6','Jaké jsou platební podmínky a co není zahrnuto v ceně?','What are the payment terms and what isn\'t included in the price?')
k('t_faq_a6','Cena 90denního mandátu je 750 000 Kč bez DPH a fakturuje se ve třech měsíčních platbách po 250 000 Kč bez DPH, vždy před zahájením příslušné třicetidenní fáze. Externí licence, cloud a služby třetích stran nejsou zahrnuty, pokud není uvedeno jinak. Každý takový náklad klient předem schvaluje a hradí přímo dodavateli. Nepřijímám provize za doporučení technologií. Fractional retainer se fakturuje měsíčně předem.','The 90-day mandate costs CZK 750,000 excl. VAT, invoiced in three monthly payments of CZK 250,000 excl. VAT, each before the start of the relevant 30-day phase. External licenses, cloud and third-party services are not included unless stated otherwise. The client approves each such cost in advance and pays the vendor directly. I take no commissions for technology recommendations. The fractional retainer is invoiced monthly in advance.')
k('t_faq_q7','Doteď jsme Head of AI neměli. Proč ho potřebujeme právě teď?','We\'ve never had a Head of AI. Why do we need one now?')
k('t_faq_a7','Možná ho ještě nepotřebujete. Tato role začíná dávat smysl ve chvíli, kdy AI ovlivňuje tržby, náklady, firemní data, zákazníky nebo rozhodování zaměstnanců. Bez jasného vlastníka se AI agenda nezastaví — její směr fakticky určují zaměstnanci, IT a dodavatelé podle vlastních priorit. Úkolem Head of AI není přidat další manažerskou vrstvu, ale sjednotit odpovědnost, zastavit slabé experimenty a soustředit investice tam, kde mají měřitelný dopad. Pokud je AI stále jen okrajový experiment, tuto roli zatím nepotřebujete.','Maybe you don\'t yet. This role starts to make sense once AI affects revenue, costs, company data, customers or employee decisions. Without a clear owner the AI agenda won\'t stop — its direction is effectively set by employees, IT and vendors following their own priorities. The job of a Head of AI isn\'t to add another management layer, but to unify accountability, stop weak experiments and focus investment where it has measurable impact. If AI is still just a marginal experiment, you don\'t need this role yet.')

# FOOTER
k('t_foot_tag','Fractional AI leadership pro firmy, které chtějí kontrolu, měřitelný dopad a první AI pracovníky v provozu.','Fractional AI leadership for companies that want control, measurable impact and their first AI workers in production.')
k('t_foot_contact','Kontakt','Contact')
k('t_foot_operator','Provozovatel','Operator')
k('t_foot_country','Česko','Czechia')

# FIT kriteria (vracena do boxu Vysledek callu)
k('t_fit_yes','Dává smysl, pokud','Makes sense if','Dáva zmysel, ak','Sinnvoll, wenn','Має сенс, якщо','يكون منطقيًا إذا')
k('t_fit_y1','dokážete pojmenovat příležitost nebo riziko za jednotky milionů ročně','you can name an opportunity or risk worth single-digit millions a year','dokážete pomenovať príležitosť alebo riziko za jednotky miliónov ročne','Sie eine Chance oder ein Risiko im Wert von einigen Millionen pro Jahr benennen können','ви можете назвати можливість або ризик на одиниці мільйонів на рік','يمكنك تحديد فرصة أو مخاطرة بقيمة بضعة ملايين سنويًا')
k('t_fit_y2','máte opakovanou práci v obchodě, komunikaci nebo provozu','you have repeat work in sales, communication or operations','máte opakovanú prácu v obchode, komunikácii alebo prevádzke','Sie wiederkehrende Arbeit im Vertrieb, in der Kommunikation oder im Betrieb haben','у вас є повторювана робота в продажах, комунікації чи операціях','لديك عمل متكرر في المبيعات أو التواصل أو العمليات')
k('t_fit_y3','máte leady, rezervace nebo tickety, které dnes řeší lidé ručně','you have leads, bookings or tickets handled manually today','máte leady, rezervácie alebo tickety, ktoré dnes riešia ľudia ručne','Sie Leads, Buchungen oder Tickets haben, die heute manuell bearbeitet werden','у вас є ліди, бронювання чи тікети, які зараз обробляють люди вручну','لديك عملاء محتملون أو حجوزات أو تذاكر يعالجها الأفراد يدويًا اليوم')
k('t_fit_y4','vedení ví, že AI bude důležitá, ale nechce kupovat nástroje naslepo',"leadership knows AI will matter but won't buy tools blindly",'vedenie vie, že AI bude dôležitá, ale nechce kupovať nástroje naslepo','die Führung weiß, dass KI wichtig sein wird, aber keine Tools blind kaufen will','керівництво розуміє важливість ШІ, але не хоче купувати інструменти наосліп','تدرك الإدارة أهمية الذكاء الاصطناعي لكنها لا تريد شراء الأدوات دون تبصر')
k('t_fit_y5','chybí člověk, který propojí business, IT, data a dodavatele','you lack someone to connect business, IT, data and vendors','chýba človek, ktorý prepojí biznis, IT, dáta a dodávateľov','Ihnen jemand fehlt, der Business, IT, Daten und Anbieter verbindet','вам бракує людини, яка поєднає бізнес, IT, дані та постачальників','تفتقر إلى شخص يربط بين الأعمال وتقنية المعلومات والبيانات والموردين')
k('t_fit_no','Není to pro vás, pokud','Not for you if','Nie je to pre vás, ak','Nichts für Sie, wenn','Це не для вас, якщо','ليس لك إذا')
k('t_fit_n1','hledáte levného chatbota','you want a cheap chatbot','hľadáte lacného chatbota','Sie einen billigen Chatbot suchen','ви шукаєте дешевого чат-бота','تبحث عن روبوت محادثة رخيص')
k('t_fit_n2','chcete inspirativní přednášku','you want an inspirational talk','chcete inšpiratívnu prednášku','Sie einen inspirierenden Vortrag wollen','вам потрібна лише надихаюча лекція','تريد محاضرة ملهمة فقط')
k('t_fit_n3','nemáte podporu vedení nebo nechcete měřit dopad',"you lack leadership support or won't measure impact",'nemáte podporu vedenia alebo nechcete merať dopad','Ihnen die Unterstützung der Führung fehlt oder Sie Wirkung nicht messen wollen','вам бракує підтримки керівництва або ви не хочете вимірювати ефект','تفتقر إلى دعم الإدارة أو لا ترغب في قياس الأثر')

# NOVE BLOKY: governance, data, adopce, FAQ (uloha CAIO/governance)
k('t_gov_label','AI Governance','AI Governance','AI Governance','KI-Governance','Управління ШІ','حوكمة الذكاء الاصطناعي')
k('t_gov_h','Pravidla, která obstojí před auditem','Rules that survive an audit','Pravidlá, ktoré obstoja pred auditom','Regeln, die einem Audit standhalten','Правила, що витримають аудит','قواعد تصمد أمام التدقيق')
k('t_gov_b1','Registr AI use-casů — přehled, kde všude ve firmě AI běží a co dělá','AI use-case registry — a live map of where AI runs in your company and what it does','Register AI use-casov — prehľad, kde všade vo firme AI beží a čo robí','AI-Use-Case-Register — eine Live-Übersicht, wo im Unternehmen KI läuft und was sie tut','Реєстр AI use-case-ів — жива мапа, де в компанії працює ШІ і що робить','سجل حالات استخدام الذكاء الاصطناعي — خريطة حيّة لأماكن عمله في شركتك وما يفعله')
k('t_gov_b2','Pravidla použití AI pro zaměstnance — co je povoleno, co ne a s jakými daty',"AI usage policy for employees — what's allowed, what isn't, and with which data",'Pravidlá používania AI pre zamestnancov — čo je povolené, čo nie a s akými dátami','KI-Nutzungsrichtlinie für Mitarbeiter — was erlaubt ist, was nicht und mit welchen Daten','Політика використання ШІ для працівників — що дозволено, що ні та з якими даними','سياسة استخدام الذكاء الاصطناعي للموظفين — ما المسموح وما الممنوع وبأي بيانات')
k('t_gov_b3','Odpovědnostní matice — u každého nasazení je jasné, kdo za výstup ručí','Accountability matrix — every deployment has a named owner for its output','Matica zodpovednosti — pri každom nasadení je jasné, kto za výstup ručí','Verantwortungsmatrix — jeder Einsatz hat einen benannten Verantwortlichen für sein Ergebnis','Матриця відповідальності — у кожного впровадження є названий власник за результат','مصفوفة المساءلة — لكل تطبيق مالك محدد مسؤول عن مخرجاته')
k('t_gov_b4','Zdokumentované AI školení zaměstnanců — plní povinnost AI gramotnosti dle čl. 4 AI Act, přizpůsobené rolím a nástrojům, které reálně používáte','Documented AI training for employees — meets the Article 4 AI literacy duty, tailored to the roles and tools you actually use','Zdokumentované AI školenie zamestnancov — plní povinnosť AI gramotnosti podľa čl. 4 AI Act, prispôsobené rolám a nástrojom, ktoré reálne používate','Dokumentierte KI-Schulung für Mitarbeiter — erfüllt die KI-Kompetenzpflicht nach Artikel 4, zugeschnitten auf die Rollen und Tools, die Sie tatsächlich nutzen',"Задокументоване AI-навчання працівників — виконує обов'язок AI-грамотності за статтею 4 AI Act, адаптоване до ролей та інструментів, які ви реально використовуєте",'تدريب موثّق على الذكاء الاصطناعي للموظفين — يفي بواجب الإلمام بالذكاء الاصطناعي وفق المادة 4، مصمَّم حسب الأدوار والأدوات التي تستخدمونها فعليًا')
k('t_gov_note','Nastaveno s ohledem na EU AI Act, GDPR a interní compliance.','Aligned with the EU AI Act, GDPR and your internal compliance.','Nastavené s ohľadom na EU AI Act, GDPR a internú compliance.','Ausgerichtet am EU AI Act, an der DSGVO und Ihrer internen Compliance.','Налаштовано з огляду на EU AI Act, GDPR та вашу внутрішню compliance.','مُعدّ بما يتوافق مع قانون الذكاء الاصطناعي الأوروبي وGDPR والامتثال الداخلي لديكم.')
k('t_st3_data','Agenty zprovozním nad vašimi stávajícími systémy a daty — CRM, ERP, e-mail, tabulky. Žádná výměna infrastruktury, žádný rok trvající datový projekt.','Agents run on top of your existing systems and data — CRM, ERP, e-mail, spreadsheets. No infrastructure swap, no year-long data project.','Agentov zprevádzkujem nad vašimi existujúcimi systémami a dátami — CRM, ERP, e-mail, tabuľky. Žiadna výmena infraštruktúry, žiadny rok trvajúci dátový projekt.','Die Agenten laufen auf Ihren bestehenden Systemen und Daten — CRM, ERP, E-Mail, Tabellen. Kein Infrastrukturwechsel, kein jahrelanges Datenprojekt.','Агентів запускаю над вашими наявними системами й даними — CRM, ERP, e-mail, таблиці. Жодної заміни інфраструктури, жодного річного дата-проєкту.','أُشغِّل الوكلاء فوق أنظمتكم وبياناتكم الحالية — CRM وERP والبريد والجداول. دون استبدال البنية التحتية ودون مشروع بيانات يستغرق عامًا.')
k('t_ret_adoption','Součástí je adopce a proškolení vašeho týmu — lidé vědí, kdy výstupu agenta věřit, kdy zasáhnout a jak s ním pracovat. AI, kterou tým sabotuje, nevydělává.',"Includes team adoption and training — your people know when to trust an agent's output, when to step in, and how to work with it. AI your team resists never pays off.",'Súčasťou je adopcia a preškolenie vášho tímu — ľudia vedia, kedy výstupu agenta veriť, kedy zasiahnuť a ako s ním pracovať. AI, ktorú tím sabotuje, nezarába.','Inklusive Adoption und Schulung Ihres Teams — Ihre Leute wissen, wann sie dem Output eines Agenten vertrauen, wann sie eingreifen und wie sie mit ihm arbeiten. KI, die das Team ablehnt, zahlt sich nie aus.','Включає адопцію та навчання вашої команди — люди знають, коли довіряти результату агента, коли втрутитися і як з ним працювати. ШІ, який команда саботує, не приносить прибутку.','يشمل تبنّي وتدريب فريقكم — يعرف موظفوكم متى يثقون بمخرجات الوكيل ومتى يتدخلون وكيف يعملون معه. الذكاء الاصطناعي الذي يقاومه الفريق لا يعود بأي ربح.')
k('t_faq_q8','Pomůžete nám s EU AI Act?','Can you help us with the EU AI Act?','Pomôžete nám s EU AI Act?','Helfen Sie uns mit dem EU AI Act?','Чи допоможете нам з EU AI Act?','هل تساعدوننا بشأن قانون الذكاء الاصطناعي الأوروبي؟')
k('t_faq_a8','Ano. Součástí sprintu je zmapování vašich AI use-casů, jejich zařazení podle rizikových kategorií AI Actu a nastavení pravidel a odpovědností tak, abyste byli připraveni na dotazy auditora i zákazníků. Součástí je i zdokumentované školení zaměstnanců podle článku 4 — povinnost, která platí od února 2025 a kterou většina českých firem zatím neřeší. Nejsem právní kancelář — na finální právní výklad spolupracuji s vaším právníkem.',"Yes. The sprint includes mapping your AI use cases, classifying them under the AI Act risk categories, and setting rules and ownership so you're ready for auditors and customers. This includes documented employee training under Article 4 — a duty in force since February 2025 that most companies haven't addressed yet. I'm not a law firm — for final legal interpretation I work with your counsel.",'Áno. Súčasťou šprintu je zmapovanie vašich AI use-casov, ich zaradenie podľa rizikových kategórií AI Actu a nastavenie pravidiel a zodpovedností tak, aby ste boli pripravení na otázky audítora aj zákazníkov. Súčasťou je aj zdokumentované školenie zamestnancov podľa článku 4 — povinnosť, ktorá platí od februára 2025 a ktorú väčšina firiem zatiaľ nerieši. Nie som právna kancelária — na finálny právny výklad spolupracujem s vaším právnikom.','Ja. Der Sprint umfasst die Erfassung Ihrer KI-Use-Cases, ihre Einordnung nach den Risikokategorien des AI Act sowie das Festlegen von Regeln und Verantwortlichkeiten, damit Sie für Auditoren und Kunden gerüstet sind. Dazu gehört auch eine dokumentierte Mitarbeiterschulung nach Artikel 4 — eine Pflicht, die seit Februar 2025 gilt und die die meisten Unternehmen noch nicht angehen. Ich bin keine Kanzlei — für die endgültige rechtliche Auslegung arbeite ich mit Ihrem Anwalt zusammen.',"Так. Спринт включає мапування ваших AI use-case-ів, їх класифікацію за категоріями ризику AI Act і встановлення правил та відповідальності, щоб ви були готові до запитань аудиторів і клієнтів. Це включає й задокументоване навчання працівників за статтею 4 — обов'язок, що діє з лютого 2025 і який більшість компаній ще не вирішує. Я не юридична фірма — для остаточного правового тлумачення співпрацюю з вашим юристом.",'نعم. يشمل السبرنت حصر حالات استخدام الذكاء الاصطناعي لديكم، وتصنيفها وفق فئات المخاطر في قانون الذكاء الاصطناعي، ووضع القواعد والمسؤوليات لتكونوا جاهزين لأسئلة المدققين والعملاء. ويشمل ذلك أيضًا تدريبًا موثّقًا للموظفين وفق المادة 4 — وهو واجب سارٍ منذ فبراير 2025 ولم تعالجه معظم الشركات بعد. لستُ مكتب محاماة — وللتفسير القانوني النهائي أتعاون مع مستشاركم القانوني.')
k('t_faq_q9','Co to udělá s naším týmem?','What happens to our team?','Čo to urobí s naším tímom?','Was passiert mit unserem Team?','Що це зробить з нашою командою?','ماذا سيحدث لفريقنا؟')
k('t_faq_a9','Agenti přebírají repetitivní práci, ne lidi. Součástí nasazení je proškolení týmu a jasná pravidla, kdo agenty řídí a kontroluje. Cílem je tým, který s AI pracuje sebevědomě — ne tým, který se jí bojí.','Agents take over repetitive work, not people. Every deployment includes team training and clear rules on who runs and reviews the agents. The goal is a team that works with AI confidently — not one that fears it.','Agenti preberajú repetitívnu prácu, nie ľudí. Súčasťou nasadenia je preškolenie tímu a jasné pravidlá, kto agentov riadi a kontroluje. Cieľom je tím, ktorý s AI pracuje sebavedomo — nie tím, ktorý sa jej bojí.','Agenten übernehmen repetitive Arbeit, nicht Menschen. Jeder Einsatz umfasst Teamschulung und klare Regeln, wer die Agenten steuert und prüft. Ziel ist ein Team, das souverän mit KI arbeitet — nicht eines, das sie fürchtet.','Агенти беруть на себе рутинну роботу, а не людей. Кожне впровадження включає навчання команди та чіткі правила, хто керує й перевіряє агентів. Мета — команда, яка впевнено працює зі ШІ, а не боїться його.','يتولى الوكلاء العمل المتكرر، لا البشر. يشمل كل تطبيق تدريب الفريق وقواعد واضحة لمن يدير الوكلاء ويراجعهم. والهدف فريق يعمل مع الذكاء الاصطناعي بثقة — لا فريق يخافه.')

# ---- doplnit TM (stara verze) pro jazyky, kde mame shodu ----
for cs, key in K.items():
    src = TM.get(cs)
    if src:
        for lg in ('sk','de','uk','ar'):
            if lg in src and lg not in TRANS[key]:
                TRANS[key][lg] = src[lg]

# ---- doplnit rucni preklady (extra.py) ----
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location('extra', os.path.join(_B, 'extra.py'))
_ex = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_ex)
for key, d in _ex.EXTRA.items():
    if key not in TRANS:   # preskoc zastarale klice (napr. rozdeleny t_ab_p2)
        continue
    for lg, v in d.items():
        TRANS[key].setdefault(lg, v)

# ---- keyovani templatu ----
html = open(SRC, encoding='utf-8').read()
# nahrad >CS< -> >{{ t.KEY }}<  (delsi retezce prvni, at nedojde k substr kolizi)
missing = []
for cs in sorted(K, key=len, reverse=True):
    key = K[cs]
    needle = '>' + cs + '<'
    if needle in html:
        html = html.replace(needle, '>{{ t.' + key + ' }}<')
    else:
        pat = re.compile('>\\s*' + re.escape(cs) + '\\s*<')
        if pat.search(html):
            html = pat.sub('>{{ t.' + key + ' }}<', html, count=1)
        else:
            missing.append((cs, key))

# jazyky, ktere realne mame kompletni (kazdy klic ma dany jazyk)
def lang_complete(lg):
    return all(lg in TRANS[key] for key in TRANS)
langs_ready = [lg for lg in ('cs','en','sk','de','uk','ar') if lg == 'cs' or lang_complete(lg)]

report = {
  'keys': len(K),
  'missing_in_template': missing,
  'langs_ready': langs_ready,
  'coverage': {lg: sum(1 for key in TRANS if lg in TRANS[key]) for lg in ('en','sk','de','uk','ar')},
  'total_keys': len(TRANS),
}
json.dump(report, open(os.path.join(_B, 'i18n_report.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)

# normalizace: &amp; -> & (STRINGS se renderuje jako textContent, ne HTML)
for _key in TRANS:
    for _lg in list(TRANS[_key]):
        TRANS[_key][_lg] = TRANS[_key][_lg].replace('&amp;', '&')

# ---- build STRINGS JS ----
def jsstr(s):
    return json.dumps(s, ensure_ascii=False)
strings_lines = []
for key, d in TRANS.items():
    parts = ','.join(f'{lg}:{jsstr(d[lg])}' for lg in ('cs','en','sk','de','uk','ar') if lg in d)
    strings_lines.append(f'  {key}:{{{parts}}}')
STRINGS_JS = 'const STRINGS = {\n' + ',\n'.join(strings_lines) + '\n};\n'
LANGS_JS = "const LANGS=[{c:'cs',f:'🇨🇿',n:'Čeština'},{c:'en',f:'🇬🇧',n:'English'},{c:'sk',f:'🇸🇰',n:'Slovenčina'},{c:'de',f:'🇩🇪',n:'Deutsch'},{c:'uk',f:'🇺🇦',n:'Українська'},{c:'ar',f:'🇸🇦',n:'العربية'}];\n"

# ---- injektaz do frameworku ----
COMPONENT_OLD = '''class Component extends DCLogic {
  state = { faqOpen: 0 };
  renderVals() {
    const vals = {};
    for (let i = 0; i < 7; i++) {
      const open = this.state.faqOpen === i;
      vals['faqExp' + i] = open;
      vals['faqRows' + i] = open ? '1fr' : '0fr';
      vals['faqIcon' + i] = open ? 'rotate(45deg)' : 'rotate(0deg)';
      vals['faqOpen' + i] = () => this.setState({ faqOpen: i });
    }
    return vals;
  }
}'''
COMPONENT_NEW = LANGS_JS + STRINGS_JS + '''class Component extends DCLogic {
  state = { faqOpen: 0, lang: null, langMenuOpen: false };
  toggleLangMenu = () => this.setState((s) => ({ langMenuOpen: !s.langMenuOpen }));
  setLang = (code) => this.setState({ lang: code, langMenuOpen: false });
  renderVals() {
    const lang = this.state.lang || 'cs';
    const t = {};
    for (const key in STRINGS) t[key] = STRINGS[key][lang] ?? STRINGS[key].en;
    const li = LANGS.find((l) => l.c === lang) || LANGS[0];
    const langList = LANGS.map((l) => ({ flag: l.f, name: l.n, code: l.c, select: () => this.setLang(l.c) }));
    const vals = { t, dir: lang === 'ar' ? 'rtl' : 'ltr', langFlag: li.f, langLabel: li.c.toUpperCase(), langMenuOpen: this.state.langMenuOpen, toggleLangMenu: this.toggleLangMenu, langList };
    for (let i = 0; i < 9; i++) {
      const open = this.state.faqOpen === i;
      vals['faqExp' + i] = open;
      vals['faqRows' + i] = open ? '1fr' : '0fr';
      vals['faqIcon' + i] = open ? 'rotate(45deg)' : 'rotate(0deg)';
      vals['faqOpen' + i] = () => this.setState({ faqOpen: i });
    }
    return vals;
  }
}'''
assert COMPONENT_OLD in html, 'component blok nenalezen!'
html = html.replace(COMPONENT_OLD, COMPONENT_NEW)

SPAN_OLD = '<span style="font-size: 12px; letter-spacing: 0.05em; color: color-mix(in srgb, var(--color-text) 55%, transparent); border: 1px solid var(--color-divider); padding: 4px 9px;">\U0001F1E8\U0001F1FF CS</span>'
SWITCHER = '<div style="position: relative;"><button onClick="{{ toggleLangMenu }}" aria-label="Language" style="font-size: 12px; letter-spacing: 0.05em; color: color-mix(in srgb, var(--color-text) 55%, transparent); border: 1px solid var(--color-divider); padding: 4px 9px; background: none; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;">{{ langFlag }} {{ langLabel }} <span style="font-size: 9px; opacity: 0.7;">▾</span></button><sc-if value="{{ langMenuOpen }}" hint-placeholder-val="{{ false }}"><div style="position: absolute; top: calc(100% + 6px); right: 0; background: var(--color-surface); border: 1px solid var(--color-divider); min-width: 154px; z-index: 60; box-shadow: 0 10px 34px rgba(0,0,0,0.55);"><sc-for list="{{ langList }}" as="l" hint-placeholder-count="6"><button onClick="{{ l.select }}" style="display: flex; align-items: center; gap: 10px; width: 100%; padding: 10px 14px; font-size: 13px; background: none; border: none; text-align: left; cursor: pointer; color: var(--color-text);" style-hover="background: var(--color-bg);"><span style="font-size: 15px;">{{ l.flag }}</span><span>{{ l.name }}</span></button></sc-for></div></sc-if></div>'
assert SPAN_OLD in html, 'lang span nenalezen!'
html = html.replace(SPAN_OLD, SWITCHER)

WRAP_OLD = '<div style="--color-bg: #161718;'
assert WRAP_OLD in html, 'wrapper nenalezen!'
html = html.replace(WRAP_OLD, '<div dir="{{ dir }}" style="--color-bg: #161718;', 1)

open(OUT, 'w', encoding='utf-8').write(html)
print(json.dumps(report, ensure_ascii=False, indent=1))
print('--- injektaz OK, klicu:', len(TRANS), '| jazyku ready:', langs_ready)
