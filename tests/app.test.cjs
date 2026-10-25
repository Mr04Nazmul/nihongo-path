const {test}=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');const vm=require('node:vm');const path=require('node:path');
const root=path.resolve(__dirname,'../dist');
async function app(url,stored={}){
 const elements=new Map(),saved=new Map([['nihongo-path',JSON.stringify(stored)]]),calls=[];
 function el(key){if(!elements.has(key))elements.set(key,{innerHTML:'',textContent:'',value:'',classList:{toggle(){}},showModal(){this.open=true},close(){this.open=false},closest(){return el('card')},querySelector(s){return el(key+s)},insertAdjacentHTML(_,s){this.innerHTML+=s}});return elements.get(key)}
 const c=vm.createContext({document:{querySelector:el,querySelectorAll:()=>[],documentElement:{},body:{classList:{toggle(){}}}},location:{pathname:url.split('?')[0],search:url.includes('?')?'?'+url.split('?')[1]:''},localStorage:{getItem:k=>saved.get(k),setItem:(k,v)=>saved.set(k,v)},URLSearchParams,Date,console,window:{NihongoSpeech:{play:(...args)=>calls.push(args)}},fetch:async u=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.join(root,u.split('?')[0]),'utf8'))})});
 vm.runInContext(fs.readFileSync(path.join(root,'app.js'),'utf8'),c);await new Promise(setImmediate);return {c,el,saved,calls,run:s=>vm.runInContext(s,c)};
}
test('all five routes load the complete grammar, vocabulary and Kanji sets',async()=>{
 for(const n of [5,4,3,2,1])for(const section of ['grammar','vocab','kanji']){
  const a=await app(`/nihongo-path/n${n}.html?section=${section}`);assert.equal(a.run('page'),'level');assert.equal(a.run('state.level'),'N'+n);assert.equal(a.run('kind'),section);assert.equal(a.run('Object.keys(db).length'),5);assert.match(a.el('#main').innerHTML,new RegExp(`n${n}\\.html\\?section=vocab`));assert.equal(a.run('entries().length'),a.run(`db.N${n}.${section}.length`));
 }
});
test('catalog links include N1 and review can select and reveal N1',async()=>{
 const a=await app('/lessons.html');assert.match(a.el('#main').innerHTML,/href="n1.html"/);
 const r=await app('/review.html');await r.el('#reviewLevel').onchange({target:{value:'N1'}});assert.equal(r.run('state.level'),'N1');r.el('#flip').onclick();assert.equal(r.run('flipped'),true);assert.match(r.el('#main').innerHTML,/source-line/);
});
test('N1 search, authored glosses, existing bookmarks and speech stay connected',async()=>{
 const a=await app('/n1.html');assert.equal(a.run("db.N1.grammar.find(e=>e.id==='gatera').locales.bn.meaning"),'কোনো কাজে যাওয়ার সুযোগে আরেকটি কাজ করা');
 a.run("query='がてら'");assert.ok(a.run('entries().length')>0);a.run("query='';openEntry(db.N1.grammar[0])");a.el('#save').onclick();assert.ok(JSON.parse(a.saved.get('nihongo-path')).saved.includes('grammar:N1:gatera'));a.el('#listen').onclick({currentTarget:{}});assert.equal(a.calls.length,1);
 a.run("kind='vocab';query=db.N1.vocab.find(e=>e.other_forms?.length).other_forms[0]");assert.ok(a.run('entries().length')>0);
 const old=await app('/n5.html',{saved:['grammar:N5:desu']});assert.ok(old.run("state.saved.includes('grammar:N5:desu')"));
});

test('index supports catalog counts without fetching all five large datasets',async()=>{const a=await app('/n5.html');assert.equal(a.run('Array.isArray(db.N5.vocab)'),true);assert.equal(a.run('Array.isArray(db.N1.vocab)'),false);assert.ok(a.run('db.N1.vocab.length')>3000)});
test('extra reference words are labeled and filterable',async()=>{const a=await app('/n1.html?section=vocab');a.run("filter='extra'");assert.ok(a.run('entries().length')>4000);assert.ok(a.run("entries().every(e=>e.curriculum_status==='supplementary')"));a.run('openEntry(entries()[0])');assert.match(a.el('#detailBody').innerHTML,/যাচাইকৃত JLPT level নয়/)});
