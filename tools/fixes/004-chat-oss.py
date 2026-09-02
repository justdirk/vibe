#!/usr/bin/env python3
"""Adds the 'Built on open source' section (+ CSS) to /chat/. Idempotent."""
assert open("CNAME").read().strip() == "dirk.it"
p = "chat/index.html"; s = open(p, encoding="utf-8").read()
if 'class="oss"' not in s:
    CSS = """  .oss{max-width:1100px;margin:0 auto;padding:0 56px 72px;display:flex;flex-direction:column;gap:16px}
  .oss h2{font-weight:500;font-size:clamp(28px,3.4vw,40px);line-height:1.08;margin:0;text-wrap:balance;max-width:24ch}
  .ossgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1px;background:rgba(242,239,233,.1);border:1px solid rgba(242,239,233,.1);margin-top:12px}
  .ossgrid a{background:#0A0A09;padding:20px 22px;display:flex;flex-direction:column;gap:4px;color:#F2EFE9}
  .ossgrid a:hover{background:#121110}
  .ossgrid b{font-weight:600;font-size:15px}
  .ossgrid span{font-size:13px;color:#9B958A}
"""
    SEC = """  <section class="oss">
    <div class="eyebrow" style="font-size:12px;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;color:#E0B15C">Built on open source</div>
    <h2>Open models, open tools. Nothing here locks you in.</h2>
    <p class="lead" style="font-size:16px;line-height:1.6;color:#9B958A;margin:0;max-width:60ch">Every piece of the workspace is open source and self-hosted. You could run the same stack yourself — the course shows you how. What you pay for is the curation, the credits and the setup you don't have to do.</p>
    <div class="ossgrid">
      <a href="https://github.com/danny-avila/LibreChat" rel="noopener"><b>LibreChat</b><span>the chat workspace</span></a>
      <a href="https://github.com/stackblitz-labs/bolt.diy" rel="noopener"><b>bolt.diy</b><span>the app builder</span></a>
      <a href="https://github.com/ace-step/ACE-Step" rel="noopener"><b>ACE-Step 1.5</b><span>the music model (coming next)</span></a>
      <a href="https://huggingface.co/moonshotai/Kimi-K2-Instruct" rel="noopener"><b>Kimi K2</b><span>frontier open model</span></a>
      <a href="https://huggingface.co/deepseek-ai" rel="noopener"><b>DeepSeek</b><span>reasoning model</span></a>
      <a href="https://huggingface.co/Qwen" rel="noopener"><b>Qwen3</b><span>fast model</span></a>
      <a href="https://github.com/justdirk/ai" rel="noopener"><b>justdirk/ai</b><span>our own config &amp; glue, in the open</span></a>
      <a href="https://github.com/justdirk/kitchenos" rel="noopener"><b>justdirk/kitchenos</b><span>camera + kitchen-ops hub, open on GitHub</span></a>
    </div>
  </section>

"""
    anchor_css = "  .faq{max-width:1100px;margin:0 auto;padding:0 56px 96px;"
    assert anchor_css in s and '  <section class="faq">' in s
    s = s.replace(anchor_css, CSS + anchor_css, 1)
    s = s.replace('  <section class="faq">', SEC + '  <section class="faq">', 1)
    s = s.replace('.faq{padding:0 20px 72px}}', '.faq{padding:0 20px 72px}.oss{padding:0 20px 56px}}', 1)
    open(p, "w", encoding="utf-8").write(s); print("1 files changed")
else:
    print("0 files changed")
