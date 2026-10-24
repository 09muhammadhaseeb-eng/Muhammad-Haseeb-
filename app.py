import base64
import pathlib

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Cosmic Tree", page_icon="🌳", layout="centered")
st.markdown(
    """<style>
    .stApp{background:#03020c}
    header,footer,#MainMenu{visibility:hidden}
    .block-container{padding:0.5rem 0.25rem 0}
    </style>""",
    unsafe_allow_html=True,
)

HERE = pathlib.Path(__file__).parent
PHOTO = "data:image/jpeg;base64," + base64.b64encode((HERE / "photo.jpg").read_bytes()).decode()
TEXT = "This meant to be continue"  # change this line to edit the message

HTML = r"""
<style>
 html,body{margin:0;background:#03020c;color:#fff;font-family:Georgia,serif}
 #c{display:block;width:100%;max-width:560px;aspect-ratio:7/9;margin:0 auto}
 button{display:block;margin:6px auto;padding:8px 22px;border:1px solid #e8c36a;border-radius:20px;
  background:transparent;color:#e8c36a;font:15px Georgia,serif}
</style>
<canvas id="c"></canvas>
<button id="r">Replay</button>
<script>
const IMG="__PHOTO__", TEXT="__TEXT__";
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const W=700,H=900,dpr=Math.min(window.devicePixelRatio||1,2);
cv.width=W*dpr;cv.height=H*dpr;ctx.scale(dpr,dpr);
let seed=11;const rnd=()=>(seed=(seed*16807)%2147483647)/2147483647;
const BX=350,BY=670,MAXD=8,segs=[],blooms=[];
const lerp=(a,b,t)=>a+(b-a)*t,clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const col=d=>{const k=d/MAXD;return k<.25?`hsl(${lerp(25,50,k/.25)},90%,52%)`:`hsl(${lerp(72,118,(k-.25)/.75)},72%,55%)`};
function grow(x,y,a,len,d,t0){
  const dur=0.25+len*0.006,x2=x+Math.cos(a)*len,y2=y-Math.sin(a)*len;
  segs.push({x,y,x2,y2,w:Math.max(1,(MAXD-d+1)*1.5),t0,dur,c:col(d)});
  const t1=t0+dur;
  if(d>=MAXD){blooms.push({x:x2,y:y2,t:t1,r:4+rnd()*4,c:rnd()<.78?'#ff7eb6':'#6fe3ff'});return}
  const n=(d>=3&&rnd()<.25)?3:2;
  for(let i=0;i<n;i++){
    let na=a+(i-(n-1)/2)*(0.5+rnd()*.25)+(rnd()-.5)*.25;
    if(d>=1)na=clamp(na,.3,Math.PI-.3);
    grow(x2,y2,na,len*(0.72+rnd()*.06),d+1,t1);
  }
}
function root(x,y,a,len,d,t0){
  const dur=0.2+len*0.008,x2=x+Math.cos(a)*len,y2=y+Math.sin(a)*len;
  segs.push({x,y,x2,y2,w:Math.max(1,3.2-d*.6),t0,dur,c:`hsl(28,90%,${52-d*4}%)`});
  if(d>=4)return;
  for(let i=0;i<2;i++)root(x2,y2,a+(i?1:-1)*(.35+rnd()*.3),len*.72,d+1,t0+dur);
}
grow(BX,BY,Math.PI/2,165,0,0);
for(let i=0;i<5;i++)root(BX,BY,Math.PI/2+(i-2)*.38,48,0,0);
const T_END=Math.max(...segs.map(s=>s.t0+s.dur))+0.7;
const stars=Array.from({length:150},()=>({x:rnd()*W,y:rnd()*H,r:rnd()*1.3+.3,p:rnd()*6.3}));
const img=new Image();img.src=IMG;
let start=performance.now();
document.getElementById('r').onclick=()=>{start=performance.now()};
function draw(t){
  ctx.fillStyle='#03020c';ctx.fillRect(0,0,W,H);
  for(const s of stars){ctx.globalAlpha=.3+.5*Math.abs(Math.sin(t*.9+s.p));ctx.fillStyle='#cfe3ff';
    ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,6.3);ctx.fill()}
  const oa=clamp(t/1.2);
  for(let i=0;i<5;i++){const rx=90+i*48;ctx.globalAlpha=oa*(.65-i*.08);
    ctx.strokeStyle=`hsl(${35+i*40},80%,55%)`;ctx.lineWidth=1.2;
    ctx.beginPath();ctx.ellipse(BX,BY+6,rx,rx*.17,0,0,6.3);ctx.stroke()}
  ctx.globalAlpha=1;ctx.lineCap='round';
  for(const s of segs){const p=clamp((t-s.t0)/s.dur);if(p<=0)continue;
    ctx.strokeStyle=s.c;ctx.lineWidth=s.w;ctx.beginPath();ctx.moveTo(s.x,s.y);
    ctx.lineTo(lerp(s.x,s.x2,p),lerp(s.y,s.y2,p));ctx.stroke()}
  for(const b of blooms){const p=clamp((t-b.t)/.6);if(p<=0)continue;const r=b.r*p;
    ctx.globalAlpha=.25*p;ctx.fillStyle=b.c;ctx.beginPath();ctx.arc(b.x,b.y,r*2.2,0,6.3);ctx.fill();
    ctx.globalAlpha=.95;
    for(let k=0;k<5;k++){const an=k*1.2566+b.x;ctx.beginPath();
      ctx.arc(b.x+Math.cos(an)*r*.8,b.y+Math.sin(an)*r*.8,r*.55,0,6.3);ctx.fill()}
    ctx.fillStyle='#fff3b0';ctx.beginPath();ctx.arc(b.x,b.y,r*.4,0,6.3);ctx.fill()}
  ctx.globalAlpha=1;
  const q=clamp((t-T_END)/1.4);
  if(q>0&&img.complete){const e=1-Math.pow(1-q,3),R=104*(.55+.45*e),cx=BX,cy=290;
    ctx.globalAlpha=e;
    const g=ctx.createRadialGradient(cx,cy,R*.9,cx,cy,R*1.9);
    g.addColorStop(0,'rgba(255,200,110,.55)');g.addColorStop(1,'rgba(255,200,110,0)');
    ctx.fillStyle=g;ctx.beginPath();ctx.arc(cx,cy,R*1.9,0,6.3);ctx.fill();
    ctx.save();ctx.beginPath();ctx.arc(cx,cy,R,0,6.3);ctx.clip();
    ctx.drawImage(img,cx-R,cy-R,R*2,R*2);ctx.restore();
    ctx.strokeStyle='#e8c36a';ctx.lineWidth=5;ctx.beginPath();ctx.arc(cx,cy,R,0,6.3);ctx.stroke();
    ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(cx,cy,R+11,0,6.3);ctx.stroke();ctx.globalAlpha=1}
  const ts=T_END+1.2,n=clamp(Math.floor((t-ts)/.09)+1,0,TEXT.length);
  if(t>ts){ctx.font='italic 600 38px Georgia,serif';ctx.textAlign='left';
    const full=ctx.measureText(TEXT).width,x0=(W-full)/2;
    const gr=ctx.createLinearGradient(x0,0,x0+full,0);gr.addColorStop(0,'#ffe29a');gr.addColorStop(1,'#ff9ccf');
    ctx.fillStyle=gr;ctx.shadowColor='rgba(255,190,120,.7)';ctx.shadowBlur=16;
    const shown=TEXT.slice(0,n);ctx.fillText(shown,x0,90);
    if(Math.floor(t*2)%2===0)ctx.fillRect(x0+ctx.measureText(shown).width+4,58,3,40);
    ctx.shadowBlur=0}
}
function loop(now){draw((now-start)/1000);requestAnimationFrame(loop)}
requestAnimationFrame(loop);
</script>
""".replace("__PHOTO__", PHOTO).replace("__TEXT__", TEXT)

components.html(HTML, height=780)
