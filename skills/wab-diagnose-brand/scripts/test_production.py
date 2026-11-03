#!/usr/bin/env python3
"""Behavioral and safety regressions for standalone production proofs; standard library only."""

import copy
import json
import tempfile
from pathlib import Path
from render_brand_deliverable import SKILL, validate, render, main

ROOT = SKILL / "assets/production"
BASE = json.loads((ROOT / "demo-brief.json").read_text())
COUNT = 0


def check(name, condition):
    global COUNT
    if not condition:
        raise AssertionError(name)
    COUNT += 1
    print(f"PASS {name}")


def bad(name, mutate, kind="website"):
    data = copy.deepcopy(BASE)
    mutate(data)
    check(name, bool(validate(data, ROOT, kind)))


def test():
    for kind in ["website", "publication"]:
        check(f"valid {kind} brief", validate(BASE, ROOT, kind) == [])
        output = render(BASE, ROOT, kind)
        check(f"{kind} embeds local artwork", 'src="data:image/svg+xml;base64,' in output)
        check(f"{kind} keeps review status visible", "SYNTHETIC EXAMPLE / NOT A CLIENT RESULT" in output and "Public release: not granted" in output)
        check(f"{kind} has no form or remote script", "<form" not in output and '<script src=' not in output)
    magazine = render(BASE, ROOT, "publication")
    check("publication follows the supplied page order", [magazine.index('id="'+p['id']+'"') for p in BASE['publication']['pages']] == sorted(magazine.index('id="'+p['id']+'"') for p in BASE['publication']['pages']))
    check("publication includes folios and trim", magazine.count('class="folio"') == 6 and "size:210mm 285mm" in magazine)
    check("non-object is rejected without a crash", bool(validate([], ROOT, "website")))
    bad("unknown field", lambda d: d.update(unrecognized=True))
    bad("unknown evidence", lambda d: d['website']['pages'][0]['paragraphs'][0].update(evidence_ids=['MISSING']))
    bad("fact without source", lambda d: d['website']['pages'][0]['paragraphs'][0].update(evidence_ids=[]))
    bad("pending fact is not public", lambda d: d['evidence'][0].update(public_use='pending'))
    bad("restricted fact is not public", lambda d: d['evidence'][0].update(public_use='restricted'))
    bad("management claim cannot become fact", lambda d: d['evidence'][0].update(classification='management_claim'))
    bad("observation cannot become fact", lambda d: d['evidence'][0].update(classification='public_observation'))
    bad("synthetic records require synthetic label", lambda d: d.update(is_synthetic=False))
    bad("duplicate evidence IDs", lambda d: d['evidence'].append(copy.deepcopy(d['evidence'][0])))
    bad("duplicate page IDs", lambda d: d['website']['pages'][1].update(id='home'))
    bad("reserved website anchor", lambda d: d['website']['pages'][0].update(id='review-contact'))
    bad("unknown asset", lambda d: d['website']['pages'][0].update(asset_ids=['UNKNOWN']))
    bad("pending asset", lambda d: d['assets'][0].update(public_use='pending'))
    bad("parent traversal", lambda d: d['assets'][0].update(path='../ceramics.svg'))
    bad("absolute asset path", lambda d: d['assets'][0].update(path='/etc/passwd'))
    bad("remote asset URL", lambda d: d['assets'][0].update(path='https://example.invalid/image.svg'))
    bad("Windows absolute asset path", lambda d: d['assets'][0].update(path='C:\\private\\image.png'))
    bad("CSS injection", lambda d: d['brand']['palette'].update(ink='#111111; background:url(https://example.invalid)'))
    bad("approved status needs receipt", lambda d: d['review'].update(content_status='approved'))
    bad("render does not grant release", lambda d: d['review'].update(public_release='granted'))
    bad("invalid date", lambda d: d['evidence'][0].update(as_of='2026-02-31'))
    bad("missing selected mode", lambda d: d.pop('website'))
    bad("empty magazine page plan", lambda d: d['publication'].update(pages=[]), 'publication')
    bad("non-finite trim", lambda d: d['publication'].update(trim_width_mm=float('nan')), 'publication')
    escaped = copy.deepcopy(BASE)
    escaped['website']['pages'][0]['headline'] = '<script>alert("x")</script>'
    check("headlines are escaped", '&lt;script&gt;' in render(escaped, ROOT, 'website') and '<script>' not in render(escaped, ROOT, 'website'))
    unused = copy.deepcopy(BASE)
    unused['evidence'].append({'id':'SECRET','statement':'PRIVATE_SENTINEL_NOT_FOR_OUTPUT','classification':'management_claim','source_ref':'private:internal','as_of':'2026-11-03','public_use':'restricted'})
    check("unused private records do not leak in appendix", 'PRIVATE_SENTINEL_NOT_FOR_OUTPUT' not in render(unused, ROOT, 'website'))
    with tempfile.TemporaryDirectory(prefix='wab-production-test-') as folder:
        root = Path(folder)
        for name, xml in [('active.svg','<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>'), ('remote.svg','<svg xmlns="http://www.w3.org/2000/svg"><image href="https://example.invalid/i.png"/></svg>'), ('event.svg','<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>')]:
            (root/name).write_text(xml)
            data=copy.deepcopy(BASE);data['assets'][0]['path']=name
            check(f"unsafe SVG {name}", bool(validate(data,root,'website')))
        (root/'escape.svg').symlink_to(ROOT/'ceramics.svg')
        data=copy.deepcopy(BASE);data['assets'][0]['path']='escape.svg'
        check('symlink escape',bool(validate(data,root,'website')))
        (root/'gradient.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g"/></defs><rect width="10" height="10" fill="url(\'#g\')"/></svg>')
        data=copy.deepcopy(BASE);data['assets'][0]['path']='gradient.svg'
        check('quoted local SVG paint reference is allowed',validate(data,root,'website')==[])
        (root/'css.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"><rect fill="url(\'https://example.invalid/i.svg\')"/></svg>')
        data['assets'][0]['path']='css.svg'
        check('external SVG paint reference is rejected',bool(validate(data,root,'website')))
        dest=root/'proof.html'
        args=['--brief',str(ROOT/'demo-brief.json'),'--kind','website','--output',str(dest)]
        check('CLI renders a real output',main(args)==0 and dest.exists())
        before=dest.read_bytes()
        check('CLI refuses accidental overwrite',main(args)==1 and dest.read_bytes()==before)
        check('explicit output overwrite',main(args+['--overwrite'])==0)
        check('CLI never overwrites source brief',main(['--brief',str(ROOT/'demo-brief.json'),'--kind','website','--output',str(ROOT/'demo-brief.json'),'--overwrite'])==1)
        check('CLI never overwrites registered asset',main(['--brief',str(ROOT/'demo-brief.json'),'--kind','website','--output',str(ROOT/'ceramics.svg'),'--overwrite'])==1)
    print(f"PASS {COUNT} production checks")


if __name__ == '__main__':
    test()
