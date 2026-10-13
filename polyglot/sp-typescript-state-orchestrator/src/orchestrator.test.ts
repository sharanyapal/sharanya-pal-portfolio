const assert = { equal(a:unknown,b:unknown){if(a!==b)throw Error('not equal')}, deepEqual(a:unknown[],b:unknown[]){if(JSON.stringify(a)!==JSON.stringify(b))throw Error('not deeply equal')}, throws(fn:()=>unknown){let threw=false;try{fn()}catch{threw=true}if(!threw)throw Error('did not throw')} };
import {ready,replay,type Event} from './orchestrator.js';
const task=(id:string,deps:string[]=[])=>({kind:'enqueue' as const,task:{id,deps,state:'pending' as const,attempts:0}});
const events:Event[]=[task('parse'),task('train',['parse']),{kind:'started',id:'parse'},{kind:'succeeded',id:'parse'}, {kind:'started',id:'train'},{kind:'succeeded',id:'train'}];
const state=replay(events);
assert.equal(state.tasks.get('train')?.state,'succeeded');assert.deepEqual(ready(state),[]);
assert.throws(()=>replay([task('a'),task('b',['a']),{kind:'started',id:'b'}]));
console.log('event sourcing DAG assertions passed');
