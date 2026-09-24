#!/usr/bin/env python3
"""/chat/ ↔ gate wiring (idempotent), plus canonicals on the app legal pages.

- Fallback gate URL is the real Railway domain (gate-production-51c9), used
  until/if gate.dirk.it doesn't resolve.
- Back from Stripe (?paid=1&session_id=cs_…): POST /api/paid and go straight
  into the workspace; the email link stays as the backup.
- /api/access may answer {status:'login'} (member with a password, email off):
  send them to chat.dirk.it/login.
- App legal pages (/app/*, /culinaris/*, /culinaris/gelato/*) get a canonical.
"""
import os, re
assert open("CNAME").read().strip() == "dirk.it"
changed = 0

def edit(path, pairs):
    global changed
    s = open(path, encoding="utf-8").read(); o = s
    for a, b in pairs:
        if b in s:
            continue
        if a not in s:
            raise SystemExit(f"{path}: anchor not found: {a[:70]}")
        s = s.replace(a, b, 1)
    if s != o:
        open(path, "w", encoding="utf-8").write(s); changed += 1

edit("chat/index.html", [
    ("var GATES=['https://gate.dirk.it','https://gate-production.up.railway.app'];",
     "var GATES=['https://gate.dirk.it','https://gate-production-51c9.up.railway.app'];"),
    ("""  if(q.get('paid'))say('Payment received. Your sign-in link is on its way — check your inbox (and spam) for "Your dirk.it AI workspace is ready".');""",
     """  function call(i,path,body){return fetch(GATES[i]+path,{method:'POST',headers:{'content-type':'application/json'},body:body}).catch(function(err){if(i+1<GATES.length)return call(i+1,path,body);throw err;});}
  if(q.get('paid')){
    say('Payment received — opening your workspace…');
    var sid=q.get('session_id')||'';
    if(/^cs_/.test(sid)){
      call(0,'/api/paid',JSON.stringify({session_id:sid})).then(function(r){return r.json();}).then(function(j){
        if(j.status==='go'&&j.url){location.replace(j.url);}
        else{say('Payment received. Your sign-in link is on its way — check your inbox (and spam) for "Your dirk.it AI workspace is ready".');}
      }).catch(function(){say('Payment received. Your sign-in link is on its way — check your inbox (and spam) for "Your dirk.it AI workspace is ready".');});
    } else say('Payment received. Your sign-in link is on its way — check your inbox (and spam) for "Your dirk.it AI workspace is ready".');
  }"""),
    ("""        else if(x.ok&&x.j.status==='checkout'&&x.j.url){say('Taking you to a secure checkout…');location.href=x.j.url;}""",
     """        else if(x.ok&&x.j.status==='checkout'&&x.j.url){say('Taking you to a secure checkout…');location.href=x.j.url;}
        else if(x.ok&&x.j.status==='login'&&x.j.url){say('You already have a workspace — taking you to sign in…');location.href=x.j.url;}"""),
])

edit("contact/index.html", [("Booking Dirk for an event?", "Inviting Dirk to speak?")])

for d in ["app", "culinaris", "culinaris/gelato"]:
    for page in ["privacy", "terms", "support", "delete-account"]:
        p = f"{d}/{page}/index.html"
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        if 'rel="canonical"' in s:
            continue
        s2 = re.sub(r"(</title>)", r'\1\n<link rel="canonical" href="https://dirk.it/' + d + "/" + page + '/">', s, count=1)
        if s2 != s:
            open(p, "w", encoding="utf-8").write(s2); changed += 1

print(f"{changed} files changed")
