import base64
import pathlib

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Cosmic Portrait", page_icon="✨", layout="centered")
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
TEXT = "It meant to be played"  # change this line to edit the message

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
let seed=5;const rnd=()=>(seed=(seed*16807)%2147483647)/2147483647;
const lerp=(a,b,t)=>a+(b-a)*t,clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const BX=350,BY=775,CX=350,CY=410,R=235,S=7;
const stars=Array.from({length:160},()=>({x:rnd()*W,y:rnd()*H,r:rnd()*1.3+.3,p:rnd()*6.3}));
const P=[];let T_END=9,ready=false;
const img=new Image();
img.onload=()=>{
  const n=Math.ceil(2*R/S),oc=document.createElement('canvas');oc.width=oc.height=n;
  const o=oc.getContext('2d');o.drawImage(img,0,0,n,n);const d=o.getImageData(0,0,n,n).data;
  for(let j=0;j<n;j++)for(let i=0;i<n;i++){
    const x=CX-R+(i+.5)*S,y=CY-R+(j+.5)*S;
    if((x-CX)**2+(y-CY)**2>R*R)continue;
    const k=(j*n+i)*4,dx=x-BX,dy=y-BY,L=Math.hypot(dx,dy)||1,sw=(rnd()-.5)*280;
    P.push({x,y,qx:(BX+x)/2-dy/L*sw,qy:(BY+y)/2+dx/L*sw,t:1.2+(1-j/n)*4.6+rnd()*.9,
      dur:1.3+rnd()*.7,c:`rgb(${d[k]},${d[k+1]},${d[k+2]})`});
  }
  T_END=Math.max(...P.map(p=>p.t+p.dur))+.3;ready=true;
};
img.src=IMG;
let start=performance.now(),wipe=true;
document.getElementById('r').onclick=()=>{start=performance.now();wipe=true};
function draw(t){
  ctx.globalAlpha=wipe?1:.2;ctx.fillStyle='#03020c';ctx.fillRect(0,0,W,H);wipe=false;
  for(const s of stars){ctx.globalAlpha=.3+.5*Math.abs(Math.sin(t*.9+s.p));ctx.fillStyle='#cfe3ff';
    ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,6.3);ctx.fill()}
  const oa=clamp(t/1.2);
  for(let i=0;i<6;i++){const rx=110+i*50;ctx.globalAlpha=oa*(.7-i*.08);
    ctx.strokeStyle=`hsl(${35+i*38},80%,55%)`;ctx.lineWidth=1.3;
    ctx.beginPath();ctx.ellipse(BX,BY+6,rx,rx*.17,0,0,6.3);ctx.stroke()}
  ctx.globalAlpha=1;
  if(!ready)return;
  for(const q of P){const p=clamp((t-q.t)/q.dur);if(p<=0)continue;
    if(p<1){const u=1-Math.pow(1-p,3),a=(1-u)*(1-u),b=2*(1-u)*u,c=u*u;
      ctx.fillStyle=`hsl(${lerp(28,125,p)},90%,${lerp(52,62,p)}%)`;
      ctx.beginPath();ctx.arc(a*BX+b*q.qx+c*q.x,a*BY+b*q.qy+c*q.y,2.6,0,6.3);ctx.fill()}
    else{const f=Math.max(0,1-(t-q.t-q.dur)/.4);
      ctx.fillStyle=f>0?'#fff3b0':q.c;ctx.beginPath();ctx.arc(q.x,q.y,S*.62*(1+.8*f),0,6.3);ctx.fill();
      if(f>0){ctx.fillStyle=q.c;ctx.beginPath();ctx.arc(q.x,q.y,S*.5,0,6.3);ctx.fill()}}}
  const k=clamp((t-T_END)/1.6);
  if(k>0){const e=1-Math.pow(1-k,3);ctx.globalAlpha=e;
    const g=ctx.createRadialGradient(CX,CY,R*.95,CX,CY,R*1.5);
    g.addColorStop(0,'rgba(255,200,110,.5)');g.addColorStop(1,'rgba(255,200,110,0)');
    ctx.fillStyle=g;ctx.beginPath();ctx.arc(CX,CY,R*1.5,0,6.3);ctx.fill();
    ctx.save();ctx.beginPath();ctx.arc(CX,CY,R,0,6.3);ctx.clip();
    ctx.drawImage(img,CX-R,CY-R,R*2,R*2);ctx.restore();
    ctx.strokeStyle='#e8c36a';ctx.lineWidth=5+Math.sin(t*3)*1.2;
    ctx.beginPath();ctx.arc(CX,CY,R,0,6.3);ctx.stroke();
    ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(CX,CY,R+12,0,6.3);ctx.stroke();ctx.globalAlpha=1}
  const ts=T_END+.8,n=clamp(Math.floor((t-ts)/.09)+1,0,TEXT.length);
  if(t>ts){ctx.font='italic 600 38px Georgia,serif';ctx.textAlign='left';
    const full=ctx.measureText(TEXT).width,x0=(W-full)/2;
    const gr=ctx.createLinearGradient(x0,0,x0+full,0);gr.addColorStop(0,'#ffe29a');gr.addColorStop(1,'#ff9ccf');
    ctx.fillStyle=gr;ctx.shadowColor='rgba(255,190,120,.7)';ctx.shadowBlur=16;
    const sh=TEXT.slice(0,n);ctx.fillText(sh,x0,95);
    if(Math.floor(t*2)%2===0)ctx.fillRect(x0+ctx.measureText(sh).width+4,63,3,40);
    ctx.shadowBlur=0}
}
function loop(now){draw((now-start)/1000);requestAnimationFrame(loop)}
requestAnimationFrame(loop);
</script>
""".replace("__PHOTO__", PHOTO).replace("__TEXT__", TEXT)

components.html(HTML, height=780)
