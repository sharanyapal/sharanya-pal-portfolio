'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const projects=['sp-banktrace-fraud-network','sp-creditsense-underwriting','sp-market-regime-radar','sp-growthlift-studio'];
for(const name of projects){
 test(name+' computes stable, finite model outputs',()=>{
   const src=fs.readFileSync(path.join(__dirname,name,'model.js'),'utf8');
   const context={window:{},Math,Set,Map};
   vm.runInNewContext(src,context,{timeout:1500});
   const app=context.window.SPModel;
   assert.ok(app?.name&&app.fields?.length>=3);
   const input=Object.fromEntries(app.fields.map(x=>[x.id,Number(x.value)]));
   const result=app.run(input);
   assert.equal(result.metrics.length,3);
   assert.ok(result.series.length>10);
   assert.ok(Array.from(result.series).every(Number.isFinite),'series contains nonfinite values');
   assert.ok(result.metrics.every(([k,v])=>String(k).length>0&&String(v).length>0));
 });
}