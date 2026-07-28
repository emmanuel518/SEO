#!/usr/bin/env python3
"""Generate the interactive Library Builder artifact: drag-and-drop rearranging of
the content library hierarchy, auto-saved locally, exportable as JSON."""
import json

SCRATCH = "/tmp/claude-0/-home-user-SEO/902ba0b1-362e-51aa-be60-e911903115d7/scratchpad"
lib = json.load(open(f"{SCRATCH}/serp/library.json"))

ENTRIES = json.dumps([{"e":x["entry"],"pid":x["pillar_id"],"r":x["ig_rank"],"n":x["size"],
    "v":x["volume"],"fr":x["fruits"],"bp":x["bca_pos"],"st":x["status"],"u":x["url"],
    "m":x["members"]} for x in lib], separators=(",", ":"))
PILLAR_NAMES = json.dumps({
 "P1":"Platform, Ad Network & Traffic","P2":"Vertical Advertising Playbooks",
 "P3":"Compliance & Ad Policies","P4":"Affiliate Economy",
 "P5":"Growth & Marketing Strategy","P6":"Operator & Industry Resources"}, separators=(",", ":"))

HTML = """<title>Library Builder — iGaming Content Hierarchy</title>
<style>
:root{
  --bg:#f6f7f5; --panel:#ffffff; --ink:#1c2420; --ink-2:#5a675f; --line:#dde3de;
  --accent:#0e7a4f; --accent-ink:#0a5c3c; --chip:#eef2ee; --hl:#f0f7f2;
  --new:#fdf0d3; --new-t:#7a5410; --exist:#dff2e4; --exist-t:#0a5c3c;
  --pos-good:#0e7a4f; --pos-mid:#a06a00; --pos-far:#9a9a9a; --drop:#0e7a4f;
  --hidden-bg:#f1f1ef;
}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;margin:0;padding:20px 16px 80px}
.wrap{max-width:980px;margin:0 auto;display:flex;flex-direction:column;gap:14px}
header{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline}
header h1{font-size:20px;margin:0;letter-spacing:-.02em}
header p{margin:0;color:var(--ink-2);font-size:12px}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:5;border-bottom:1px solid var(--line)}
button{background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:7px 12px;font:inherit;font-size:13px;cursor:pointer}
button:hover{border-color:var(--accent);color:var(--accent-ink)}
button.primary{background:var(--accent);border-color:var(--accent);color:#fff}
button.primary:hover{background:var(--accent-ink);color:#fff}
button:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.saved{color:var(--ink-2);font-size:12px;margin-left:auto}
.pillar{background:var(--panel);border:1px solid var(--line);border-radius:10px}
.pillar+.pillar{margin-top:10px}
.phead{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding:10px 14px;border-bottom:1px solid var(--line)}
.phead .grip{color:var(--ink-2);cursor:default;font-size:12px}
.pname{font-weight:700;font-size:14px;min-width:180px;flex:1;border:1px dashed transparent;border-radius:4px;padding:1px 5px}
.pname:hover{border-color:var(--line)} .pname:focus{border-color:var(--accent);outline:none}
.pstat{color:var(--ink-2);font-size:12px;font-variant-numeric:tabular-nums}
.pbody{padding:8px 10px;min-height:34px}
.pbody.dragover{background:var(--hl);outline:2px dashed var(--drop);outline-offset:-4px;border-radius:8px}
.card{display:flex;flex-wrap:wrap;gap:8px;align-items:center;border:1px solid var(--line);border-radius:7px;padding:6px 9px;margin:5px 0;background:var(--bg);cursor:grab}
.card:active{cursor:grabbing}
.card.dragging{opacity:.4}
.card.dropbefore{box-shadow:0 -3px 0 0 var(--drop)}
.card.dropafter{box-shadow:0 3px 0 0 var(--drop)}
.grab{color:var(--ink-2);font-size:13px;user-select:none}
.ename{font-weight:600;flex:1;min-width:160px}
.meta{color:var(--ink-2);font-size:11.5px;font-variant-numeric:tabular-nums;white-space:nowrap}
.pill{border-radius:99px;padding:0 8px;font-size:10.5px;font-weight:700}
.st-new{background:var(--new);color:var(--new-t)} .st-existing{background:var(--exist);color:var(--exist-t)}
.pos{font-weight:700} .p-good{color:var(--pos-good)} .p-mid{color:var(--pos-mid)} .p-far{color:var(--pos-far)}
.tools{display:flex;gap:3px;align-items:center}
.tools button{padding:2px 7px;font-size:12px;border-radius:5px}
.tools select{border:1px solid var(--line);border-radius:5px;font-size:11px;padding:2px 3px;background:var(--panel);color:var(--ink)}
details.mem{width:100%}
details.mem summary{font-size:11px;color:var(--ink-2);cursor:pointer;list-style:none}
details.mem summary::-webkit-details-marker{display:none}
details.mem span{font-size:11px;color:var(--ink-2)}
#hiddenShelf .card{background:var(--hidden-bg);opacity:.85}
.note{color:var(--ink-2);font-size:12px;margin:0}
h2{font-size:15px;margin:10px 0 0}
dialog{border:1px solid var(--line);border-radius:10px;padding:16px;max-width:640px;width:92%}
dialog textarea{width:100%;height:220px;font:11px/1.4 ui-monospace,Menlo,Consolas,monospace;border:1px solid var(--line);border-radius:6px;padding:8px}
::backdrop{background:rgba(20,26,22,.35)}
</style>
<div class="wrap">
<header>
  <h1>Library Builder</h1>
  <p>Drag entries to reorder or move them between pillars · rename pillars inline · changes auto-save in this browser</p>
</header>
<div class="bar">
  <button class="primary" id="exportBtn">Export arrangement</button>
  <button id="copyBtn">Copy JSON</button>
  <button id="addPillar">+ Add pillar</button>
  <button id="resetBtn">Reset to IG order</button>
  <span class="saved" id="saved"></span>
</div>
<div id="board"></div>
<h2>Hidden entries</h2>
<p class="note">Drag a card here (or press ✕ on a card) to park it outside the library. Nothing is deleted.</p>
<div class="pillar"><div class="pbody" id="hiddenShelf" data-pid="__hidden__"></div></div>
<dialog id="dlg"><h2 style="margin:0 0 8px">Arrangement JSON</h2>
<textarea id="dlgText" readonly></textarea>
<div style="display:flex;gap:8px;margin-top:10px"><button id="dlgClose">Close</button></div></dialog>
</div>
<script>
const ENTRIES = __ENTRIES__;
const PILLAR_NAMES = __PILLAR_NAMES__;
const BYKEY = Object.fromEntries(ENTRIES.map(e=>[e.e,e]));
const LSKEY = "bca-igaming-library-v1";

function defaultState(){
  const pillars = Object.keys(PILLAR_NAMES).sort().map(pid => ({
    id: pid, name: PILLAR_NAMES[pid],
    entries: ENTRIES.filter(e=>e.pid===pid).sort((a,b)=>a.r-b.r).map(e=>e.e),
  }));
  return {version:1, pillars, hidden:[]};
}
function loadState(){
  try{
    const s = JSON.parse(localStorage.getItem(LSKEY));
    if(!s || !s.pillars) return defaultState();
    const known = new Set([...s.pillars.flatMap(p=>p.entries), ...(s.hidden||[])]);
    ENTRIES.forEach(e => {                       // merge in entries added since last save
      if(!known.has(e.e)){
        const p = s.pillars.find(p=>p.id===e.pid) || s.pillars[0];
        p.entries.push(e.e);
      }
    });
    s.pillars.forEach(p => p.entries = p.entries.filter(k=>BYKEY[k]));
    s.hidden = (s.hidden||[]).filter(k=>BYKEY[k]);
    return s;
  }catch(err){ return defaultState(); }
}
let state = loadState();
let saveTimer = null;
function save(){
  localStorage.setItem(LSKEY, JSON.stringify(state));
  const el = document.getElementById("saved");
  el.textContent = "Saved " + new Date().toLocaleTimeString();
  clearTimeout(saveTimer); saveTimer = setTimeout(()=>el.textContent="", 4000);
}

function posClass(p){ return p==null ? "" : p<=10 ? "p-good" : p<=20 ? "p-mid" : "p-far"; }
function esc(s){ return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"/g,"&quot;"); }

function cardHTML(key){
  const e = BYKEY[key];
  const pillarOpts = state.pillars.map(p=>`<option value="${esc(p.id)}">${esc(p.name)}</option>`).join("");
  return `<div class="card" draggable="true" data-k="${esc(key)}">
    <span class="grab" aria-hidden="true">⠿</span>
    <span class="ename">${esc(e.e)}</span>
    <span class="meta">${e.n} kw${e.n>1?"s":""}</span>
    <span class="meta">vol ${e.v.toLocaleString("en-US")}</span>
    <span class="meta">🍎 ${e.fr}</span>
    <span class="meta pos ${posClass(e.bp)}">${e.bp?"#"+e.bp:"—"}</span>
    <span class="pill st-${e.st}">${e.st}</span>
    <span class="tools">
      <button title="Move up" data-act="up">↑</button>
      <button title="Move down" data-act="down">↓</button>
      <select title="Move to pillar" data-act="moveto"><option value="">move…</option>${pillarOpts}<option value="__hidden__">Hidden</option></select>
      <button title="Hide entry" data-act="hide">✕</button>
    </span>
    <details class="mem"><summary>${e.n>1 ? "keywords ▾" : "keyword ▾"}</summary><span>${e.m.map(esc).join(" · ")}</span></details>
  </div>`;
}

function render(){
  const board = document.getElementById("board");
  board.innerHTML = state.pillars.map(p => {
    const vol = p.entries.reduce((s,k)=>s+BYKEY[k].v,0);
    return `<div class="pillar" data-pid="${esc(p.id)}">
      <div class="phead">
        <span class="grip">${esc(p.id)}</span>
        <span class="pname" contenteditable="true" spellcheck="false" data-pid="${esc(p.id)}">${esc(p.name)}</span>
        <span class="pstat">${p.entries.length} entries · vol ${vol.toLocaleString("en-US")}</span>
        ${p.entries.length===0 ? `<button data-delp="${esc(p.id)}" title="Delete empty pillar">delete</button>` : ""}
      </div>
      <div class="pbody" data-pid="${esc(p.id)}">${p.entries.map(cardHTML).join("")}</div>
    </div>`;
  }).join("");
  document.getElementById("hiddenShelf").innerHTML = state.hidden.map(cardHTML).join("") ||
    `<p class="note" style="padding:4px 6px">Nothing hidden.</p>`;
  wire();
}

function findEntry(key){
  for(const p of state.pillars){ const i = p.entries.indexOf(key); if(i>=0) return {list:p.entries, i}; }
  const i = state.hidden.indexOf(key); if(i>=0) return {list:state.hidden, i};
  return null;
}
function moveTo(key, pid, index){
  const from = findEntry(key); if(!from) return;
  from.list.splice(from.i,1);
  const dest = pid==="__hidden__" ? state.hidden : (state.pillars.find(p=>p.id===pid)||state.pillars[0]).entries;
  if(index==null || index<0 || index>dest.length) index = dest.length;
  dest.splice(index,0,key);
  save(); render();
}

let dragKey = null;
function wire(){
  document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("dragstart", ev => {
      dragKey = card.dataset.k;
      ev.dataTransfer.effectAllowed = "move";
      ev.dataTransfer.setData("text/plain", dragKey);
      setTimeout(()=>card.classList.add("dragging"),0);
    });
    card.addEventListener("dragend", () => { card.classList.remove("dragging"); clearMarks(); });
    card.addEventListener("dragover", ev => {
      if(!dragKey || card.dataset.k===dragKey) return;
      ev.preventDefault(); ev.stopPropagation();
      const before = ev.offsetY < card.offsetHeight/2;
      clearMarks(); card.classList.add(before ? "dropbefore" : "dropafter");
    });
    card.addEventListener("drop", ev => {
      if(!dragKey || card.dataset.k===dragKey) return;
      ev.preventDefault(); ev.stopPropagation();
      const before = card.classList.contains("dropbefore");
      clearMarks();
      const pid = card.closest(".pbody").dataset.pid;
      const dest = pid==="__hidden__" ? state.hidden : state.pillars.find(p=>p.id===pid).entries;
      const from = findEntry(dragKey); from.list.splice(from.i,1);
      let idx = dest.indexOf(card.dataset.k); if(!before) idx += 1;
      dest.splice(idx,0,dragKey);
      dragKey = null; save(); render();
    });
    // per-card tools
    card.querySelectorAll("[data-act]").forEach(el => {
      const key = card.dataset.k;
      if(el.dataset.act==="moveto"){
        el.addEventListener("click", ev=>ev.stopPropagation());
        el.addEventListener("change", () => { if(el.value) moveTo(key, el.value); });
      } else el.addEventListener("click", ev => {
        ev.stopPropagation();
        const f = findEntry(key);
        if(el.dataset.act==="hide") moveTo(key, "__hidden__");
        if(el.dataset.act==="up" && f.i>0){ [f.list[f.i-1],f.list[f.i]]=[f.list[f.i],f.list[f.i-1]]; save(); render(); }
        if(el.dataset.act==="down" && f.i<f.list.length-1){ [f.list[f.i+1],f.list[f.i]]=[f.list[f.i],f.list[f.i+1]]; save(); render(); }
      });
    });
  });
  document.querySelectorAll(".pbody").forEach(zone => {
    zone.addEventListener("dragover", ev => { if(dragKey){ ev.preventDefault(); zone.classList.add("dragover"); } });
    zone.addEventListener("dragleave", () => zone.classList.remove("dragover"));
    zone.addEventListener("drop", ev => {
      if(!dragKey) return;
      ev.preventDefault(); zone.classList.remove("dragover");
      moveTo(dragKey, zone.dataset.pid); dragKey = null;
    });
  });
  document.querySelectorAll(".pname").forEach(el => {
    el.addEventListener("blur", () => {
      const p = state.pillars.find(p=>p.id===el.dataset.pid);
      const name = el.textContent.trim();
      if(p && name){ p.name = name; save(); render(); } else render();
    });
    el.addEventListener("keydown", ev => { if(ev.key==="Enter"){ ev.preventDefault(); el.blur(); } });
  });
  document.querySelectorAll("[data-delp]").forEach(b => b.addEventListener("click", () => {
    state.pillars = state.pillars.filter(p=>p.id!==b.dataset.delp); save(); render();
  }));
}
function clearMarks(){ document.querySelectorAll(".dropbefore,.dropafter").forEach(c=>c.classList.remove("dropbefore","dropafter")); }

function exportJSON(){
  return JSON.stringify({
    exported_note: "Blockchain-Ads iGaming content library arrangement (user-defined)",
    pillars: state.pillars.map(p=>({id:p.id, name:p.name, entries:p.entries})),
    hidden: state.hidden,
    publish_order: state.pillars.flatMap(p=>p.entries),
  }, null, 1);
}
document.getElementById("exportBtn").addEventListener("click", async () => {
  const data = exportJSON();
  if(window.claude && window.claude.downloads){
    try{ await window.claude.downloads.save({filename:"igaming-library-arrangement.json", data}); return; }
    catch(err){ if(err && err.code==="declined") return; }
  }
  showDialog(data);
});
document.getElementById("copyBtn").addEventListener("click", async () => {
  const data = exportJSON();
  try{ await navigator.clipboard.writeText(data);
    const el=document.getElementById("saved"); el.textContent="Copied to clipboard";
    clearTimeout(saveTimer); saveTimer=setTimeout(()=>el.textContent="",4000);
  }catch(err){ showDialog(data); }
});
function showDialog(data){
  document.getElementById("dlgText").value = data;
  document.getElementById("dlg").showModal();
}
document.getElementById("dlgClose").addEventListener("click", ()=>document.getElementById("dlg").close());
document.getElementById("addPillar").addEventListener("click", () => {
  const n = state.pillars.length+1;
  let id = "P"+n; while(state.pillars.some(p=>p.id===id)) id += "x";
  state.pillars.push({id, name:"New pillar", entries:[]}); save(); render();
});
document.getElementById("resetBtn").addEventListener("click", () => {
  if(confirm("Reset the arrangement to the computed information-gain order? Your custom arrangement in this browser will be replaced.")){
    state = defaultState(); save(); render();
  }
});
render();
</script>
"""

HTML = HTML.replace("__ENTRIES__", ENTRIES).replace("__PILLAR_NAMES__", PILLAR_NAMES)
out = f"{SCRATCH}/library-builder.html"
open(out, "w").write(HTML)
print("written", len(HTML), "bytes,", len(lib), "entries")
