// ===== Date du jour (dateline du journal) =====
(function(){
  const d = new Date();
  const mois = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"];
  const jours = ["dimanche","lundi","mardi","mercredi","jeudi","vendredi","samedi"];
  const txt = `${jours[d.getDay()]} ${d.getDate()} ${mois[d.getMonth()]} ${d.getFullYear()}`;
  const el = document.getElementById('dateline');
  if(el) el.textContent = txt;
})();

// ===== Reveal subtil au scroll (pas de setTimeout en cascade) =====
(function(){
  const items = document.querySelectorAll('.article, .lead, .toc');
  if(!('IntersectionObserver' in window)){ items.forEach(i=>i.classList.add('in')); return; }
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} });
  },{threshold:0.12});
  items.forEach(i=>io.observe(i));
})();
