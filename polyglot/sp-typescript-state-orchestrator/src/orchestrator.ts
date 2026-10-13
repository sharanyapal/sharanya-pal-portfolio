export type Status = 'pending' | 'running' | 'succeeded' | 'failed';
export type Task = {id: string; deps: string[]; state: Status; attempts: number};
export type Event = {kind:'enqueue'; task:Task} | {kind:'started'|'succeeded'|'failed'; id:string};
export type State = {tasks: ReadonlyMap<string, Task>; events:readonly Event[]};
export function reduce(state: State, event: Event): State {
 const tasks = new Map(state.tasks);
 if(event.kind === 'enqueue'){
  if(tasks.has(event.task.id))throw new Error('duplicate task');
  tasks.set(event.task.id,{...event.task,deps:[...event.task.deps]});
 } else {
  const task = tasks.get(event.id); if(!task)throw new Error('unknown task');
  if(event.kind==='started'){
    if(task.state!=='pending')throw new Error('not pending');
    if(!task.deps.every(d=>tasks.get(d)?.state==='succeeded'))throw new Error('dependency not satisfied');
    tasks.set(event.id,{...task,state:'running',attempts:task.attempts+1});
  }else{
    if(task.state!=='running')throw new Error('task not running');
    tasks.set(event.id,{...task,state:event.kind==='succeeded'?'succeeded':'failed'});
  }
 }
 return {tasks,events:[...state.events,event]};
}
export function ready(state:State):string[]{return [...state.tasks.values()].filter(t=>t.state==='pending'&&t.deps.every(d=>state.tasks.get(d)?.state==='succeeded')).map(t=>t.id)}
export function replay(events:Event[]):State{return events.reduce(reduce,{tasks:new Map<string,Task>(),events:[]})}
