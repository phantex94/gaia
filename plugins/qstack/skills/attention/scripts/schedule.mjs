function textOK(x){return typeof x==="string"&&x.trim().length>0}

function numberOK(x){return typeof x==="number"&&Number.isFinite(x)&&x>=0}

function equal(a,b){return JSON.stringify(a)===JSON.stringify(b)}

function question(r){return ["intent","semantic","design"].includes(r.kind)}

function target(r){const t=r.target;return [t.machine,t.project,t.task,t.phase,t.revision,t.wait_token]}

function binding(r){return [r.id,r.version,r.kind,r.owner,r.mode,r.severity,r.required,r.question,r.options,target(r),r.intake_id??null,r.share??null,r.depends_on]}

function sharedKey(r){return r.mode==="medium"&&["intent","semantic"].includes(r.kind)&&r.share?.verified===true&&r.required&&r.severity!=="authority"?[r.kind,r.owner,r.severity,r.share.scope,r.share.key,r.share.revision,r.share.evidence,r.question,r.options]:null}

function value(r,w){return numberOK(r.evsi)&&numberOK(r.delay_min)&&numberOK(r.human_cost)?r.evsi+w*r.delay_min-r.human_cost:null}

function validateRequest(r){
  if(!r||!["id","version","owner","question"].every(k=>textOK(r[k])))throw Error("missing request identity");
  if(!["intent","semantic","design","gate1","plan","merge","permission","auth","failure","pick","unknown"].includes(r.kind))throw Error("invalid kind: "+r.id);
  if(!["fast","medium"].includes(r.mode)||!["red","yellow","green","authority"].includes(r.severity)||!["pending","closed","answered"].includes(r.status)||typeof r.observed!=="boolean"||typeof r.required!=="boolean")throw Error("invalid state: "+r.id);
  if(!r.target||!["machine","project","task","phase","revision","wait_token"].every(k=>textOK(r.target[k])))throw Error("incomplete target: "+r.id);
  if(!Array.isArray(r.options)||!r.options.every(textOK)||new Set(r.options).size!==r.options.length||(!r.options.length&&r.kind!=="unknown"))throw Error("invalid options: "+r.id);
  if(!Array.isArray(r.depends_on)||!r.depends_on.every(textOK)||!numberOK(r.created_min)||typeof r.urgent!=="boolean"||typeof r.critical!=="boolean")throw Error("invalid timing/dependencies: "+r.id);
  for(const k of ["deadline_min","evsi","delay_min","human_cost"])if(r[k]!==null&&!numberOK(r[k]))throw Error("invalid cost/deadline: "+r.id);
  if((!question(r)||r.severity!=="green")&&!r.required)throw Error("mandatory decision cannot be optional: "+r.id);
  if(r.mode==="fast"&&(r.ambiguity!=null||r.intake_id!=null||r.kind==="intent"||r.kind==="gate1"||!r.required))throw Error("Fast Path must remain unscored and outside intake: "+r.id);
  if(["intent","gate1"].includes(r.kind)&&(!textOK(r.intake_id)||r.mode!=="medium"))throw Error("missing intake binding: "+r.id);
  if(r.intake_id!=null&&!["intent","gate1"].includes(r.kind))throw Error("invalid intake kind: "+r.id);
  if(r.share!=null&&(!["scope","key","revision","evidence"].every(k=>textOK(r.share[k]))||typeof r.share.verified!=="boolean"))throw Error("invalid sharing evidence: "+r.id);
}

function priority(r,now,maxWait,w){
  const age=now-r.created_min;
  let tier=4;
  if(r.required){
    if(r.urgent||(r.deadline_min!==null&&r.deadline_min<=now))tier=0;
    else if(age>=maxWait||(r.severity==="red"&&r.critical))tier=1;
    else if(question(r)||["permission","auth","failure","unknown"].includes(r.kind))tier=2;
    else tier=3;
  }
  return {tier,deadline:r.deadline_min??Infinity,age,net:value(r,w)};
}

function rank(a,b){
  return a.tier-b.tier||(a.deadline===b.deadline?0:a.deadline-b.deadline)||(b.net??-Infinity)-(a.net??-Infinity)||b.age-a.age||a.id.localeCompare(b.id);
}

function schedule(input){
  const {requests,now_min:now,batch_limit:limit,max_wait_min:maxWait,delay_weight:w,intakes}=input;
  if(!Array.isArray(requests)||!numberOK(now)||!Number.isInteger(limit)||limit<1||limit>4||!numberOK(maxWait)||maxWait===0||!numberOK(w)||!intakes||typeof intakes!=="object"||Array.isArray(intakes))throw Error("invalid schedule snapshot/config");
  requests.forEach(validateRequest);
  if(new Set(requests.map(r=>r.id)).size!==requests.length)throw Error("duplicate request id");
  for(const [k,b] of Object.entries(intakes)){
    if(!textOK(k)||!b||!Number.isInteger(b.batches_used)||b.batches_used<0||b.batches_used>2||!Number.isInteger(b.questions_used)||b.questions_used<0||b.questions_used>8||b.questions_used>4*b.batches_used||typeof b.confirmation_ready!=="boolean"||typeof b.confirmation_used!=="boolean")throw Error("invalid intake budget: "+k);
  }
  const blocked=[],deferred=[],eligible=[];
  const open=requests.filter(r=>r.status==="pending");
  const closed=requests.filter(r=>r.status==="closed"&&r.observed);
  for(const r of open){
    const k=r.intake_id??null,b=k!==null&&Object.hasOwn(intakes,k)?intakes[k]:null;
    let why=null;
    if(!r.observed||r.created_min>now)why="UNVERIFIED_SNAPSHOT";
    else if(r.depends_on.some(d=>!closed.some(c=>c.id===d)))why="DEPENDENCY_OPEN";
    else if(r.kind==="unknown")why="UNKNOWN_BLOCKER";
    else if(k!==null&&!b)why="INTAKE_BUDGET_UNKNOWN";
    else if(r.kind==="intent"&&(b.batches_used>=2||b.questions_used>=8||b.confirmation_used))why="INTAKE_BUDGET_EXHAUSTED";
    else if(r.kind==="gate1"&&(!b.confirmation_ready||b.confirmation_used||open.some(x=>x.intake_id===k&&x.kind==="intent"&&x.required)))why="GATE1_NOT_READY";
    else if(r.mode==="fast"&&question(r))why="FAST_BLOCKED_NO_INTERVIEW";
    else if(sharedKey(r)!==null&&open.some(x=>x.id!==r.id&&sharedKey(x)!==null&&x.share.scope===r.share.scope&&x.share.key===r.share.key&&x.share.revision===r.share.revision&&!equal(sharedKey(x),sharedKey(r))))why="SHARED_DEFINITION_CONFLICT";
    if(why){blocked.push({id:r.id,reason:why});continue}
    const p=priority(r,now,maxWait,w);
    if(!r.required&&(p.net===null||p.net<=0)){deferred.push({id:r.id,reason:p.net===null?"OPTIONAL_VALUE_UNKNOWN":"OPTIONAL_VALUE_NONPOSITIVE"});continue}
    eligible.push({r,...p,id:r.id});
  }
  eligible.sort(rank);
  const groups=[];
  for(const x of eligible){
    const key=sharedKey(x.r),g=key===null?null:groups.find(y=>equal(y.share,key));
    if(g){g.members.push(x.r);continue}
    groups.push({id:x.id,kind:x.r.kind,owner:x.r.owner,question:x.r.question,options:x.r.options,tier:x.tier,deadline:x.deadline===Infinity?null:x.deadline,age:x.age,net:x.net,share:key,members:[x.r]});
  }
  const selected=[],remaining=[],used=[],owner=groups[0]?.owner??null;
  for(const g of groups){
    const keys=[...new Set(g.members.filter(r=>r.kind==="intent").map(r=>r.intake_id))];
    const capped=keys.some(k=>used.filter(x=>x===k).length>=Math.min(4,8-intakes[k].questions_used));
    const gateConflict=g.members.some(r=>r.intake_id!=null&&selected.some(s=>s.members.some(y=>y.intake_id===r.intake_id&&(y.kind==="gate1"||r.kind==="gate1"))));
    if(selected.length>=limit||g.owner!==owner||capped||gateConflict){remaining.push({...g,reason:g.owner!==owner?"OTHER_DECISION_OWNER":capped?"INTAKE_QUESTION_CAP":gateConflict?"SEPARATE_GATE1":"BATCH_CAP"});continue}
    selected.push(g);used.push(...keys);
  }
  return {selected,remaining,blocked,deferred,owner,intake_questions:[...new Set(used)].map(k=>({intake_id:k,questions:used.filter(x=>x===k).length,batches:1})),advisory_only:true};
}

function validateAnswer(presented,live,reply){
  validateRequest(presented);validateRequest(live);
  const reject=reason=>({ok:false,reason,action:"NONE"});
  if(!reply||reply.source!=="human"||reply.explicit!==true||reply.owner!==presented.owner||reply.id!==presented.id||reply.version!==presented.version||!textOK(reply.receipt_id)||!Array.isArray(reply.delivered_receipts))return reject("EXPLICIT_HUMAN_BINDING_REQUIRED");
  if(reply.delivered_receipts.includes(reply.receipt_id))return reject("ALREADY_DELIVERED_RECONCILE");
  if(!presented.observed||!live.observed||presented.status!=="pending"||live.status!=="pending"||!equal(binding(presented),binding(live)))return reject("STALE_OR_CHANGED_TARGET");
  if(!presented.options.includes(reply.choice))return reject("CHOICE_NOT_OFFERED");
  if(["defer","decline"].includes(reply.choice))return {ok:true,action:"HOLD",reason:"HUMAN_DEFERRED_OR_DECLINED"};
  if(live.mode==="fast"&&question(live))return {ok:true,action:"HUMAN_DIRECT",reason:"FAST_BLOCKED_NO_INTERVIEW"};
  if(["intent","gate1"].includes(live.kind))return {ok:true,action:"INTAKE_RECORD_ONLY",reason:"RECHECK_ALL_GATE_PREREQUISITES"};
  if(["plan","merge"].includes(live.kind))return {ok:true,action:"NATIVE_APPROVAL_REVIEW",reason:"HUMAN_MUST_APPROVE_CURRENT_BOARD_OBJECT"};
  if(["permission","auth","pick","failure","unknown"].includes(live.kind))return {ok:true,action:"HUMAN_DIRECT",reason:"NO_GENERIC_TELL_OR_AUTO_APPROVAL"};
  return {ok:true,action:"QUESTION_TELL_CANDIDATE",reason:"RECHECK_BOARD_KIND_SCOPE_AND_NATIVE_AUTHORITY"};
}

export { schedule, validateAnswer };
