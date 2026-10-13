// Run using: mongosh --file pipeline.js
// Synthetic ecommerce fixture with cohort-aware funnel attribution and indexes.
const dbx = db.getSiblingDB('sp_analytics_demo');
dbx.orders.drop(); dbx.events.drop();
const users=['u1','u2','u3','u4','u5','u6'];
const cohort=['paid','organic','paid','social','organic','social'];
dbx.events.insertMany(users.flatMap((id,i)=>[
 {user_id:id,channel:cohort[i],type:'visit',at:new Date(`2026-09-${String(i+1).padStart(2,'0')}T00:00:00Z`)},
 ...(i!==3?[{user_id:id,channel:cohort[i],type:'add_to_cart',at:new Date(`2026-09-${String(i+1).padStart(2,'0')}T00:10:00Z`)}]:[]),
 ...(i%3!==2?[{user_id:id,channel:cohort[i],type:'purchase',at:new Date(`2026-09-${String(i+1).padStart(2,'0')}T00:20:00Z`)}]:[])
]));
dbx.orders.insertMany(users.filter((_,i)=>i%3!==2).map((u,i)=>({user_id:u,amount:100+i*35,currency:'USD',createdAt:new Date('2026-09-12T00:00:00Z')})));
dbx.events.createIndex({user_id:1,at:1});dbx.events.createIndex({channel:1,type:1});
const result=dbx.events.aggregate([
 {$group:{_id:{user:'$user_id',channel:'$channel'},types:{$addToSet:'$type'}}},
 {$project:{channel:'$_id.channel',visited:{$in:['visit','$types']},cart:{$in:['add_to_cart','$types']},converted:{$in:['purchase','$types']}}},
 {$group:{_id:'$channel',visitors:{$sum:{$cond:['$visited',1,0]}},carts:{$sum:{$cond:['$cart',1,0]}},buyers:{$sum:{$cond:['$converted',1,0]}}}},
 {$addFields:{conversionRate:{$cond:[{$gt:['$visitors',0]},{$divide:['$buyers','$visitors']},0]}}},
 {$sort:{conversionRate:-1}}
]).toArray();
printjson(result);
if (result.reduce((sum,x)=>sum+x.visitors,0)!==6)throw Error('fixture funnel assertion failed');
