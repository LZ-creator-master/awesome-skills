/* Record real browser frames. Requires playwright and ffmpeg; no model calls. */
const { chromium } = require('playwright');
const { spawn } = require('node:child_process');
const { once } = require('node:events');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'dist/pages');

async function run() {
  if (!process.env.DEMO_BROWSER || !process.env.DEMO_FFMPEG) throw Error('Set DEMO_BROWSER and DEMO_FFMPEG');
  const server = http.createServer((request, response) => {
    let relative;
    try { relative = decodeURIComponent(new URL(request.url, 'http://localhost').pathname); } catch { response.writeHead(400).end(); return; }
    let file = path.resolve(SITE, '.' + relative);
    if (!file.startsWith(SITE + path.sep) && file !== SITE) { response.writeHead(403).end(); return; }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    if (!fs.existsSync(file)) { response.writeHead(404).end(); return; }
    const types = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8'};
    response.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
    fs.createReadStream(file).pipe(response);
  });
  server.listen(0, '127.0.0.1'); await once(server, 'listening');
  const base = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch({headless:true, executablePath:process.env.DEMO_BROWSER});
  const context = await browser.newContext({viewport:{width:1280,height:720},permissions:['clipboard-read','clipboard-write']});
  const page = await context.newPage();
  const errors=[]; page.on('pageerror', e=>errors.push(e.message));
  fs.mkdirSync(path.join(ROOT, 'media'), {recursive:true});
  const encoder = spawn(process.env.DEMO_FFMPEG, ['-y','-f','image2pipe','-vcodec','png','-framerate','10','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',path.join(ROOT,'media/skills-demo.mp4')], {windowsHide:true,stdio:['pipe','ignore','pipe']});
  let encoderError=''; encoder.stderr.on('data', chunk=>encoderError+=chunk); encoder.stdin.on('error',()=>{});
  const completed=once(encoder,'close');
  async function caption(text) { await page.evaluate(text=>{let el=document.getElementById('recording-caption');if(!el){el=document.createElement('div');el.id='recording-caption';el.style.cssText='position:fixed;bottom:12px;left:50%;transform:translateX(-50%);z-index:99999;background:#153c34;color:white;padding:10px 22px;border-radius:9px;font:18px Microsoft YaHei,system-ui;white-space:nowrap;box-shadow:0 2px 12px #0003';document.body.append(el)}el.textContent=text;}, text); }
  try {
    for(let frame=0;frame<300;frame++){
      if(frame===0){await page.goto(base);await page.locator('#start').scrollIntoViewIfNeeded();await caption('选择任务，获得对应安装命令与提示词');}
      if(frame===18)await page.locator('#quick-task').selectOption('edit');
      if(frame===33)await page.locator('#quick-task').selectOption('read');
      if(frame===50){await page.goto(base+'/examples/attention-is-all-you-need/');await caption('基础版：先看直观解释与结果');}
      if(frame===80){await page.getByLabel('进阶版',{exact:true}).check();await caption('进阶版：展开公式与源码对应');}
      if(frame===110){await page.locator('#try').scrollIntoViewIfNeeded();await caption('拖动查询，观察注意力权重变化');}
      if(frame>=120&&frame<140){await page.locator('#query').focus();await page.locator('#query').press('ArrowRight');}
      if(frame===145){await page.locator('#mask').check();await caption('开启遮罩：未来位置归零，剩余位置重新归一化');}
      if(frame===172)await page.locator('#reset').click();
      if(frame===190){await page.locator('#code').scrollIntoViewIfNeeded();await caption('方法与代码：固定版本，逐项核对');}
      if(frame===230){await page.locator('#prompt').scrollIntoViewIfNeeded();await caption('复制提示词，换成自己的论文');}
      if(frame===246){await page.locator('#copy').click();}
      if(frame===270){await page.goto(base+'/examples/lightgcn/#meeting');await page.locator('#meeting').scrollIntoViewIfNeeded();await caption('LightGCN：从论文解读到10分钟组会提纲');}
      const buffer=await page.screenshot({type:'png'});
      if(frame===115)fs.writeFileSync(path.join(ROOT,'media/demo-poster.png'),buffer);
      if(!encoder.stdin.write(buffer))await once(encoder.stdin,'drain');
    }
    encoder.stdin.end();const [code]=await completed;if(code!==0)throw Error(encoderError.slice(-2000));
    if(errors.length)throw Error(errors.join('\n'));
    console.log('Recorded 300 real browser frames: 30 seconds at 1280x720, 10 fps.');
  } finally {if(!encoder.stdin.destroyed)encoder.stdin.end();await browser.close();server.close();}
}
run().catch(error=>{console.error(error);process.exit(1)});
