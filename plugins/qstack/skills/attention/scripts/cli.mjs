import { readFileSync } from "node:fs";
import { schedule, validateAnswer } from "./schedule.mjs";

try {
  const [command,path] = process.argv.slice(2);
  if (!["schedule","validate"].includes(command) || !path || process.argv.length !== 4) throw Error("usage: node cli.mjs schedule|validate <snapshot.json|->");
  const input=JSON.parse(readFileSync(path==="-"?0:path,"utf8"));
  const result=command==="schedule"?schedule(input):validateAnswer(input.presented,input.live,input.reply);
  console.log(JSON.stringify(result,null,2));
} catch (error) {
  console.error("Refusal: "+error.message);
  process.exitCode=2;
}
