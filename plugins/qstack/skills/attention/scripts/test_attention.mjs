import { schedule, validateAnswer } from "./schedule.mjs";

function fixture(id,over={}){
  return {id,version:"v1",kind:"semantic",owner:"human",mode:"medium",severity:"red",required:true,status:"pending",observed:true,question:"Choose label horizon",options:["5d","10d"],target:{machine:"mac",project:"alpha",task:id,phase:"build",revision:"intent-v1",wait_token:"wait-1"},created_min:0,deadline_min:null,urgent:false,critical:false,depends_on:[],evsi:10,delay_min:5,human_cost:1,...over};
}

function config(requests,over={}){return {requests,now_min:10,batch_limit:4,max_wait_min:30,delay_weight:1,intakes:{},...over}}

function share(){return {verified:true,scope:"alpha-model-contract",key:"label",revision:"v1",evidence:"ADR-12-v1"}}

function reply(r,over={}){return {source:"human",explicit:true,owner:r.owner,id:r.id,version:r.version,choice:r.options[0],receipt_id:"decision-"+r.id+"-1",delivered_receipts:[],...over}}

function check(x,msg){if(!x)throw Error(msg)}

function throws(f){try{f()}catch{return}throw Error("expected rejection")}

function budget(batches=0,questions=0,ready=false,used=false){return {batches_used:batches,questions_used:questions,confirmation_ready:ready,confirmation_used:used}}

function runTests(){
  const tests=[
    ["same verified scope merges",()=>{const s=schedule(config([fixture("a",{share:share()}),fixture("b",{share:share()})]));check(s.selected.length===1&&s.selected[0].members.length===2,"merge")}],
    ["different scope separate",()=>check(schedule(config([fixture("a",{share:share()}),fixture("b",{share:{...share(),scope:"other"}})])).selected.length===2,"scope")],
    ["conflicting options block",()=>check(schedule(config([fixture("a",{share:share()}),fixture("b",{share:share(),options:["1d","5d"]})])).blocked.length===2,"conflict")],
    ["unverified reuse separate",()=>check(schedule(config([fixture("a",{share:{...share(),verified:false}}),fixture("b",{share:share()})])).selected.length===2,"unverified")],
    ["approvals never merge",()=>{for(const kind of ["permission","merge","plan","auth","pick"])check(schedule(config([fixture("a",{kind,share:share()}),fixture("b",{kind,share:share()})])).selected.length===2,kind)}],
    ["urgent then critical then ordinary",()=>{const s=schedule(config([fixture("ordinary"),fixture("critical",{critical:true}),fixture("urgent",{kind:"permission",urgent:true})]));check(s.selected.map(x=>x.id).join(",")==="urgent,critical,ordinary","priority")}],
    ["expired deadline becomes urgent",()=>check(schedule(config([fixture("a"),fixture("b",{deadline_min:9})])).selected[0].id==="b","deadline")],
    ["aging promotes mandatory",()=>check(schedule(config([fixture("b",{created_min:40,critical:true}),fixture("a",{kind:"merge"})],{now_min:45})).selected[0].id==="a","age")],
    ["mandatory not dropped for negative value",()=>check(schedule(config([fixture("a",{evsi:0,delay_min:0,human_cost:20})])).selected.length===1,"mandatory")],
    ["negative optional deferred",()=>check(schedule(config([fixture("a",{required:false,severity:"green",evsi:0,delay_min:0})])).deferred[0].reason==="OPTIONAL_VALUE_NONPOSITIVE","optional")],
    ["unknown optional deferred",()=>check(schedule(config([fixture("a",{required:false,severity:"green",evsi:null})])).deferred[0].reason==="OPTIONAL_VALUE_UNKNOWN","unknown")],
    ["unknown mandatory shown",()=>check(schedule(config([fixture("a",{evsi:null})])).selected.length===1,"mandatory")],
    ["fast semantic blocked and no score",()=>{const a=fixture("a",{mode:"fast"});check(schedule(config([a])).blocked[0].reason==="FAST_BLOCKED_NO_INTERVIEW","fast");throws(()=>schedule(config([{...a,ambiguity:{score:1}}])))}],
    ["fast permission visible unscored",()=>check(schedule(config([fixture("a",{mode:"fast",kind:"permission",severity:"authority"})])).selected.length===1,"fast permission")],
    ["duplicate ids rejected",()=>throws(()=>schedule(config([fixture("a"),fixture("a")])))],
    ["unknown dependency blocked",()=>check(schedule(config([fixture("a",{depends_on:["missing"]})])).blocked[0].reason==="DEPENDENCY_OPEN","dependency")],
    ["closed dependency unlocks",()=>check(schedule(config([fixture("b",{status:"closed"}),fixture("a",{depends_on:["b"]})])).selected[0].id==="a","dependency")],
    ["unverified and future blocked",()=>check(schedule(config([fixture("a",{observed:false}),fixture("b",{created_min:11})])).blocked.length===2,"snapshot")],
    ["intake exhausted blocks",()=>check(schedule(config([fixture("a",{kind:"intent",intake_id:"i"})],{intakes:{i:budget(2,8)}})).blocked[0].reason==="INTAKE_BUDGET_EXHAUSTED","budget")],
    ["batch cap and intake count",()=>{const rs=Array.from({length:6},(_,i)=>fixture("q"+i,{kind:"intent",intake_id:"i"}));const s=schedule(config(rs,{intakes:{i:budget(1,4)}}));check(s.selected.length===4&&s.remaining.length===2&&s.intake_questions[0].questions===4,"cap")}],
    ["open Red prevents Gate1",()=>{const s=schedule(config([fixture("a",{kind:"intent",intake_id:"i"}),fixture("b",{kind:"gate1",intake_id:"i"})],{intakes:{i:budget(0,0,true)}}));check(s.blocked.some(x=>x.id==="b"&&x.reason==="GATE1_NOT_READY"),"gate")}],
    ["ready confirmation separate after budget",()=>{const s=schedule(config([fixture("a",{kind:"gate1",intake_id:"i"})],{intakes:{i:budget(2,8,true)}}));check(s.selected.length===1&&s.intake_questions.length===0,"confirm")}],
    ["different owners separate",()=>check(schedule(config([fixture("a"),fixture("b",{owner:"other"})])).selected.length===1,"owner")],
    ["valid human answer candidate only",()=>{const a=fixture("a");check(validateAnswer(a,a,reply(a)).action==="QUESTION_TELL_CANDIDATE","candidate")}],
    ["autopilot or vague yes rejected",()=>{const a=fixture("a");check(!validateAnswer(a,a,reply(a,{source:"autopilot"})).ok&&!validateAnswer(a,a,reply(a,{explicit:false})).ok,"source")}],
    ["stale revision or wait rejected",()=>{const a=fixture("a");for(const k of ["revision","wait_token"])check(!validateAnswer(a,{...a,target:{...a.target,[k]:"changed"}},reply(a)).ok,k)}],
    ["wrong machine or recipient rejected",()=>{const a=fixture("a");check(!validateAnswer(a,{...a,target:{...a.target,machine:"other"}},reply(a)).ok&&!validateAnswer(a,a,reply(a,{id:"b"})).ok,"identity")}],
    ["changed options rejects",()=>{const a=fixture("a");check(!validateAnswer(a,{...a,options:["5d","20d"]},reply(a)).ok,"options")}],
    ["duplicate receipt rejected",()=>{const a=fixture("a");check(!validateAnswer(a,a,reply(a,{delivered_receipts:["decision-a-1"]})).ok,"duplicate")}],
    ["closed cannot receive reply",()=>{const a=fixture("a");check(!validateAnswer(a,{...a,status:"closed"},reply(a)).ok,"closed")}],
    ["invalid choice rejected",()=>{const a=fixture("a");check(!validateAnswer(a,a,reply(a,{choice:"20d"})).ok,"choice")}],
    ["plan merge manual native review",()=>{for(const kind of ["plan","merge"]){const a=fixture("a",{kind,options:["approve","decline"]});check(validateAnswer(a,a,reply(a)).action==="NATIVE_APPROVAL_REVIEW",kind)}}],
    ["permission auth failure pick manual",()=>{for(const kind of ["permission","auth","failure","pick"]){const a=fixture("a",{kind});check(validateAnswer(a,a,reply(a)).action==="HUMAN_DIRECT",kind)}}],
    ["decline holds",()=>{const a=fixture("a",{kind:"permission",options:["approve","decline"]});check(validateAnswer(a,a,reply(a,{choice:"decline"})).action==="HOLD","decline")}],
    ["Gate1 record only",()=>{const a=fixture("a",{kind:"gate1",intake_id:"i",options:["confirm","decline"]});check(validateAnswer(a,a,reply(a)).action==="INTAKE_RECORD_ONLY","no dispatch")}],
    ["optional authority refused",()=>throws(()=>schedule(config([fixture("a",{kind:"permission",required:false,severity:"green"})])))],
    ["changed permission class refused",()=>{const a=fixture("a");check(!validateAnswer(a,{...a,kind:"permission"},reply(a)).ok,"kind")}]
  ];
  return tests.map(([name,f])=>{try{f();return {name,pass:true}}catch(e){return {name,pass:false,error:String(e)}}});
}

function simulationCases(){
  const mk=(id,t,tail,extra={})=>fixture(id,{created_min:t,tail,delay_min:tail,...extra});
  return [
    {name:"shared contract burst",offline:[],requests:[mk("a",0,60,{share:share(),critical:true}),mk("b",0,90,{share:share(),critical:true}),mk("c",1,20)]},
    {name:"staggered same scope",offline:[],requests:[mk("a",0,45,{share:share()}),mk("b",3,60,{share:share()}),mk("c",4,30)]},
    {name:"different scopes",offline:[],requests:[mk("a",0,60,{share:share()}),mk("b",0,60,{share:{...share(),scope:"other"}})]},
    {name:"urgent permission",offline:[],requests:[mk("a",0,20),mk("b",0,90,{kind:"permission",urgent:true}),mk("c",0,10)]},
    {name:"human offline",offline:[[0,25]],requests:[mk("a",0,30,{share:share()}),mk("b",5,60,{share:share()}),mk("c",12,90,{critical:true})]},
    {name:"late critical",offline:[],requests:[mk("a",0,20),mk("b",1,10),mk("c",2,120,{critical:true})]},
    {name:"independent approvals",offline:[],requests:[mk("a",0,60,{kind:"plan",share:share()}),mk("b",0,50,{kind:"merge",share:share()}),mk("c",0,30,{kind:"merge",share:share()})]},
    {name:"eight decisions",offline:[],requests:Array.from({length:8},(_,i)=>mk("q"+i,0,10*i,{critical:i===7}))},
    {name:"single urgent",offline:[],requests:[mk("a",1,80,{urgent:true,kind:"permission"})]},
    {name:"two owners",offline:[],requests:[mk("a",0,30),mk("b",0,60,{owner:"other"}),mk("c",0,10)]},
    {name:"long offline shared",offline:[[0,45]],requests:Array.from({length:6},(_,i)=>mk("q"+i,5*i,30+i*10,{share:i<4?share():null,critical:i===5}))},
    {name:"sparse arrivals",offline:[],requests:[mk("a",1,30),mk("b",14,40),mk("c",28,50)]}
  ];
}

function replay(c,policy){
  let t=0,batches=0,questions=0,human=0,wait=0,finish=0;
  const answered=[],all=c.requests;
  while(answered.length<all.length&&t<1000){
    if(c.offline.some(([a,b])=>a<=t&&t<b)){t++;continue}
    const pending=all.filter(r=>r.created_min<=t&&!answered.includes(r.id));
    if(!pending.length){t++;continue}
    let groups;
    if(policy==="immediate")groups=[{members:[pending[0]]}];
    else if(policy==="fixed"){
      if(t%10!==0){t++;continue}
      groups=pending.filter(r=>r.owner===pending[0].owner).slice(0,4).map(r=>({members:[r]}));
    }else groups=schedule(config(policy==="priority"?pending.map(r=>({...r,share:null})):pending,{now_min:t})).selected;
    check(groups.length>0,"stalled "+c.name);
    const duration=2+groups.length;
    if(c.offline.some(([a,b])=>t<b&&t+duration>a)){t++;continue}
    batches++;questions+=groups.length;human+=duration;t+=duration;
    for(const g of groups)for(const r of g.members){check(!answered.includes(r.id),"duplicate simulation delivery");answered.push(r.id);wait+=t-r.created_min;finish=Math.max(finish,t+r.tail)}
  }
  check(answered.length===all.length,"unanswered "+c.name);
  return {scenario:c.name,policy,batches,questions,human_minutes:human,decision_wait_minutes:wait,project_finish_min:finish,answered:answered.length};
}

function benchmark(){
  const cases=simulationCases(),policies=["immediate","fixed","priority","adaptive"];
  const rows=cases.flatMap(c=>policies.map(p=>replay(c,p)));
  const totals=policies.map(policy=>{const rs=rows.filter(x=>x.policy===policy);return {policy,...Object.fromEntries(["batches","questions","human_minutes","decision_wait_minutes","project_finish_min","answered"].map(k=>[k,rs.reduce((s,r)=>s+r[k],0)]))}});
  return {assumptions:"12 synthetic scenarios; mandatory answerable requests; 2 min batch overhead + 1 min/question; fixed on 10-min grid; no cross-owner batch; priority/adaptive event-driven, priority disables grouping; project finish=max(answer time + independent tail); no actual LLM or Herdr",rows,totals};
}

const tests=runTests();
const failures=tests.filter(t=>!t.pass);
console.log(JSON.stringify({tests,passed:tests.length-failures.length,failed:failures.length},null,2));
if(failures.length)process.exitCode=1;
else console.log(JSON.stringify(benchmark(),null,2));
