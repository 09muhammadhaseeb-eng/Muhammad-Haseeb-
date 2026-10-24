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
const BX=350,BY=775,CX=350,CY=410,R=235;
const stars=Array.from({length:160},()=>({x:rnd()*W,y:rnd()*H,r:rnd()*1.3+.3,p:rnd()*6.3}));
const mk=()=>{const c=document.createElement('canvas');c.width=W*dpr;c.height=H*dpr;
  const x=c.getContext('2d');x.scale(dpr,dpr);return [c,x]};
const [LC,lx]=mk(),[PC,px]=mk();
const L=[],C=[];let li=0,ci=0,T_LINE=6,T_END=10,ready=false,recent=[];
const img=new Image();
function grab(m){const o=document.createElement('canvas');o.width=o.height=m;
  const x=o.getContext('2d');x.drawImage(img,0,0,m,m);return x.getImageData(0,0,m,m).data}
img.onload=()=>{
  // ---- 1. pencil outline: edge detect, then trace into strokes
  const n=235,sc=2*R/n,d=grab(n),g=new Float32Array(n*n),b=new Float32Array(n*n),mag=new Float32Array(n*n),gxs=new Float32Array(n*n),gys=new Float32Array(n*n);
  for(let i=0;i<n*n;i++)g[i]=.3*d[i*4]+.59*d[i*4+1]+.11*d[i*4+2];
  for(let y=1;y<n-1;y++)for(let x=1;x<n-1;x++){let s=0;
    for(let a=-1;a<=1;a++)for(let c=-1;c<=1;c++)s+=g[(y+a)*n+x+c];b[y*n+x]=s/9}
  for(let y=1;y<n-1;y++)for(let x=1;x<n-1;x++){const i=y*n+x;
    const gx=-b[i-n-1]-2*b[i-1]-b[i+n-1]+b[i-n+1]+2*b[i+1]+b[i+n+1];
    const gy=-b[i-n-1]-2*b[i-n]-b[i-n+1]+b[i+n-1]+2*b[i+n]+b[i+n+1];
    gxs[i]=gx;gys[i]=gy;mag[i]=Math.hypot(gx,gy)}
  const th=Float32Array.from(mag).sort()[Math.floor(n*n*.9)],E=new Uint8Array(n*n);
  for(let y=2;y<n-2;y++)for(let x=2;x<n-2;x++){const i=y*n+x,m=mag[i];if(m<th)continue;
    const st=Math.abs(gxs[i])>Math.abs(gys[i])?1:n;if(m<mag[i-st]||m<mag[i+st])continue;
    if(((x+.5)*sc-R)**2+((y+.5)*sc-R)**2>(R-4)**2)continue;E[i]=1}
  const dirs=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]];
  for(let y=0;y<n;y++)for(let x=0;x<n;x++){if(E[y*n+x]!==1)continue;
    let cx=x,cy=y;E[cy*n+cx]=2;const pts=[[cx,cy]];
    for(;;){let nx=-1,ny=-1;for(const[a,c]of dirs){const X=cx+a,Y=cy+c;
      if(X>=0&&Y>=0&&X<n&&Y<n&&E[Y*n+X]===1){nx=X;ny=Y;break}}
      if(nx<0)break;E[ny*n+nx]=2;pts.push([nx,ny]);cx=nx;cy=ny}
    if(pts.length<7)continue;
    const t0=.8+y/n*4.2+rnd()*.3;
    for(let k=1;k<pts.length;k++)L.push({t:t0+k*.006,x1:CX-R+(pts[k-1][0]+.5)*sc,y1:CY-R+(pts[k-1][1]+.5)*sc,
      x2:CX-R+(pts[k][0]+.5)*sc,y2:CY-R+(pts[k][1]+.5)*sc})}
  L.sort((a,b)=>a.t-b.t);T_LINE=L.length?L[L.length-1].t:5;
  // ---- 2. colour fill: paint rises from the bottom like liquid
  const m=79,S=2*R/m,dd=grab(m);
  for(let j=0;j<m;j++)for(let i=0;i<m;i++){const x=CX-R+(i+.5)*S,y=CY-R+(j+.5)*S;
    if((x-CX)**2+(y-CY)**2>(R+3)**2)continue;const k=(j*m+i)*4;
    C.push({t:T_LINE-1.2+(1-j/m)*3.2+rnd()*.5,x,y,c:`rgb(${dd[k]},${dd[k+1]},${dd[k+2]})`})}
  C.sort((a,b)=>a.t-b.t);T_END=C[C.length-1].t+.4;ready=true;
};
img.src=IMG;
let start=performance.now();
document.getElementById('r').onclick=()=>{start=performance.now();li=ci=0;recent=[];
  lx.clearRect(0,0,W,H);px.clearRect(0,0,W,H)};
function draw(t){
  ctx.fillStyle='#03020c';ctx.fillRect(0,0,W,H);
  for(const s of stars){ctx.globalAlpha=.3+.5*Math.abs(Math.sin(t*.9+s.p));ctx.fillStyle='#cfe3ff';
    ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,6.3);ctx.fill()}
  const oa=clamp(t/1.2);
  for(let i=0;i<6;i++){const rx=110+i*50;ctx.globalAlpha=oa*(.7-i*.08);
    ctx.strokeStyle=`hsl(${35+i*38},80%,55%)`;ctx.lineWidth=1.3;
    ctx.beginPath();ctx.ellipse(BX,BY+6,rx,rx*.17,0,0,6.3);ctx.stroke()}
  ctx.globalAlpha=.7;ctx.strokeStyle='#e8c36a';ctx.lineWidth=1.2;ctx.setLineDash([6,8]);
  ctx.beginPath();ctx.arc(CX,CY,R+12,-1.5708,-1.5708+6.283*clamp(t/1.4));ctx.stroke();ctx.setLineDash([]);
  ctx.globalAlpha=1;
  if(!ready)return;
  lx.lineCap='round';lx.strokeStyle='#ffe9a8';lx.lineWidth=1.8;lx.shadowColor='#ffb84d';lx.shadowBlur=6;
  const pen=[];
  while(li<L.length&&L[li].t<=t){const e=L[li++];lx.beginPath();lx.moveTo(e.x1,e.y1);lx.lineTo(e.x2,e.y2);lx.stroke();
    if(t-e.t<.05)pen.push(e)}
  lx.shadowBlur=0;
  while(ci<C.length&&C[ci].t<=t){const e=C[ci++];px.fillStyle=e.c;px.beginPath();px.arc(e.x,e.y,4.7,0,6.3);px.fill();
    if(rnd()<.25)recent.push(e)}
  const k=clamp((t-T_END)/1.6),e3=1-Math.pow(1-k,3);
  ctx.save();ctx.beginPath();ctx.arc(CX,CY,R+2,0,6.3);ctx.clip();ctx.drawImage(PC,0,0,W,H);
  if(k>0){ctx.globalAlpha=e3;ctx.drawImage(img,CX-R,CY-R,R*2,R*2);ctx.globalAlpha=1}ctx.restore();
  ctx.globalAlpha=1-.85*e3;ctx.drawImage(LC,0,0,W,H);ctx.globalAlpha=1;
  for(const p of pen.slice(-12)){ctx.fillStyle='#fff';ctx.shadowColor='#ffd27a';ctx.shadowBlur=14;
    ctx.beginPath();ctx.arc(p.x2,p.y2,3,0,6.3);ctx.fill()}ctx.shadowBlur=0;
  recent=recent.filter(r=>t-r.t<.4);
  for(const r of recent){const a=(t-r.t)/.4;ctx.globalAlpha=1-a;ctx.fillStyle='#fff8d0';
    ctx.beginPath();ctx.arc(r.x,r.y,4*(1-a)+1,0,6.3);ctx.fill()}ctx.globalAlpha=1;
  if(k>0){ctx.globalAlpha=e3;
    const g=ctx.createRadialGradient(CX,CY,R*.97,CX,CY,R*1.5);
    g.addColorStop(0,'rgba(255,200,110,.45)');g.addColorStop(1,'rgba(255,200,110,0)');
    ctx.fillStyle=g;ctx.beginPath();ctx.arc(CX,CY,R*1.5,0,6.3);ctx.fill();
    ctx.strokeStyle='#e8c36a';ctx.lineWidth=5+Math.sin(t*3)*1.2;ctx.beginPath();ctx.arc(CX,CY,R+2,0,6.3);ctx.stroke();
    ctx.globalAlpha=1}
  const ts=T_END+.8,n=clamp(Math.floor((t-ts)/.09)+1,0,TEXT.length);
  if(t>ts){ctx.font='italic 600 38px Georgia,serif';ctx.textAlign='left';
    const full=ctx.measureText(TEXT).width,x0=(W-full)/2;
    const gr=ctx.createLinearGradient(x0,0,x0+full,0);gr.addColorStop(0,'#ffe29a');gr.addColorStop(1,'#ff9ccf');
    ctx.fillStyle=gr;ctx.shadowColor='rgba(255,190,120,.7)';ctx.shadowBlur=16;
    const sh=TEXT.slice(0,n);ctx.fillText(sh,x0,70);
    if(Math.floor(t*2)%2===0)ctx.fillRect(x0+ctx.measureText(sh).width+4,38,3,40);
    ctx.shadowBlur=0}
}
function loop(now){draw((now-start)/1000);requestAnimationFrame(loop)}
requestAnimationFrame(loop);
</script>
""".replace("__PHOTO__", PHOTO).replace("__TEXT__", TEXT)

components.html(HTML, height=780)
