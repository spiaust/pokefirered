const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const root=path.resolve(__dirname,'../strategy-guide/dist');
class Element{constructor(){this.children=[];this.value='';this.innerHTML='';this.textContent='';this.attrs={};this.handlers={};this.classList={add(){},remove(){},toggle(){return true}}}append(e){this.children.push(e)}addEventListener(k,f){this.handlers[k]=f}setAttribute(k,v){this.attrs[k]=v}querySelector(q){return elements[q]||(elements[q]=new Element())}showModal(){this.open=true}close(){this.open=false}}
const elements={},storage={},events={};const document={title:'',querySelector(q){return elements[q]||(elements[q]=new Element())},createElement(){return new Element()}};
const context={document,location:{hash:''},localStorage:{getItem:k=>storage[k]||null,setItem:(k,v)=>storage[k]=v},confirm:()=>true,window:{addEventListener:(k,f)=>events[k]=f,scrollTo(){},print(){}},console};vm.createContext(context);vm.runInContext(fs.readFileSync(root+'/guide-data.js','utf8'),context);vm.runInContext(fs.readFileSync(root+'/guide.js','utf8'),context);
assert(elements['#page'].innerHTML.includes('Your tour.'));
const chapters=context.window.GUIDE;assert.equal(chapters.length,41);assert.equal(new Set(chapters.map(c=>c.id)).size,41);
for(const c of chapters){context.location.hash='#'+c.id;events.hashchange();assert(elements['#page'].innerHTML.includes(c.title),c.id);assert(c.html.length>100,c.id);for(const [src] of c.images)assert(fs.existsSync(root+'/images/'+src),src)}
context.location.hash='#european-council-complete-championship-walkthrough';events.hashchange();elements['#chapter-check'].handlers.change({target:{checked:true}});assert(storage['europe-tour-guide-v33'].includes('true'));assert(elements['#progress-label'].textContent.startsWith('1 of'));
elements['#search'].value='gastly';elements['#search'].handlers.input();assert(/matching chapters/.test(elements['#results'].textContent));
vm.runInContext('printBook()',context);assert.equal((elements['#print-book'].innerHTML.match(/class="print-chapter"/g)||[]).length,42);
const p=JSON.parse(fs.readFileSync(root+'/images/provenance.json','utf8'));assert(p.length>=35);for(const row of p)assert(fs.existsSync(root+'/images/'+row.image));
console.log('PASS: all 41 chapters render, unique anchors, screenshot assets, search, saved reader completion and full 42-section print book');
console.log('PASS:',p.length,'new native screenshot capture records and packaged guide sources');
