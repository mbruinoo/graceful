# Assemble index.html from the template, the atlas data and the evidence table.
import json, pathlib
here=pathlib.Path(__file__).parent
ev=json.loads((here/"evidence.json").read_text())
t=(here/"page.template.html").read_text()
t=t.replace("__ATLAS__",(here/"atlas.json").read_text()).replace("__EVID__",json.dumps(ev))
(here/"index.html").write_text(t)
