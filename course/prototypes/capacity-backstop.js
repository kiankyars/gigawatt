const reference='d15-cost-per-service';
const source={
 coreweave:'https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm',
 nvidia:'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm',
 program:'https://blogs.nvidia.com/blog/nvidia-unlocks-ai-compute-at-scale-capital-partners-to-power-ai-infrastructure-buildout/',
 july:'https://newsletter.semianalysis.com/p/nvidia-gpu-debt-backstop-unleashes',
 september:'https://newsletter.semianalysis.com/p/nvidias-backstop-universe-heads-i'
};
const scene=(id,label,title,explanation,sources)=>({id,label,title,reference,objective:'D15.4',pedagogical_role:'case-study',explanation:[explanation],sources});
export const backstopScenes=[
 scene('nvidia-coreweave-backstop','NVIDIA buys unsold capacity','NVIDIA agreed to buy CoreWeave’s unsold capacity.','On September 9, 2025, CoreWeave signed an order with an initial value of $6.3 billion. NVIDIA must buy the covered capacity left unsold to other customers through April 13, 2032, subject to delivery, availability and termination terms. The graphic divides the contracted pool conceptually; its widths do not represent reported occupancy. This is a cloud-capacity purchase obligation, not an unconditional guarantee of every CoreWeave loan.',[source.coreweave]),
 scene('nvidia-backstop-financing','Long support, shorter rentals','A six-year backstop supports shorter customer rentals.','NVIDIA’s July 2026 model supports clouds serving multiple customers. Its filing describes commitments typically lasting six years. SemiAnalysis explains how lenders can underwrite contracted fallback revenue while operators rent on shorter terms. The short rental blocks are illustrative, not disclosed contracts. NVIDIA’s capacity commitment is reduced as customers use that capacity. Each contract still has delivery and operating conditions. Keep this 2026 model distinct from the preceding CoreWeave agreement.',[source.july,source.program,source.nvidia]),
 scene('nvidia-backstop-risk','Who carries the downside?','NVIDIA earns a share of the upside and takes capacity risk.','SemiAnalysis describes a trade: the operator gains a revenue floor but shares some revenue above it with NVIDIA. The floor can support debt without ensuring an attractive equity return. NVIDIA reported $36 billion of AI-cloud commitments as of July 26, 2026. Its filing says lower demand can leave it purchasing capacity it cannot use or resell. These are commitments, not reported losses or cash already spent. The separately disclosed hardware-supply and property-lease obligations are excluded from this figure.',[source.september,source.july,source.nvidia])
];
const credit=(url,label)=>`<a href="${url}" target="_blank" rel="noreferrer">${label}</a>`;
const wrap=body=>`<div class="k-stack kb-stack">${body}</div>`;
function coreweave(){return wrap(`
 <div class="kb-deal"><div><span>Agreement · September 2025</span><strong>$6.3 billion</strong><span>Initial contract value</span></div><div><span>Capacity commitment through</span><strong>April 2032</strong></div></div>
 <div class="kb-capacity" role="img" aria-label="Covered CoreWeave capacity: customers buy capacity, and NVIDIA purchases the remaining unsold capacity."><section><span class="kb-racks" aria-hidden="true">▥ ▥ ▥</span><h2>Customers rent capacity</h2></section><section><span class="kb-racks" aria-hidden="true">▥ ▥</span><h2>NVIDIA buys the unsold remainder</h2></section></div>
 <p class="k-credit">${credit(source.coreweave,'CoreWeave · September 15, 2025 filing')}</p>`);}
function financing(){return wrap(`
 <div class="kb-tenor" role="img" aria-label="Illustrative short customer rentals above a six-year NVIDIA backstop. The contracted fallback revenue helps the operator obtain financing for the cluster.">
  <div class="kb-year-axis"><span></span><div>${[1,2,3,4,5,6].map(y=>`<span>Year ${y}</span>`).join('')}</div></div>
  <div class="kb-tenor-row"><h2>Customer rentals</h2><div class="kb-short-terms"><span>Short contracts</span><span>Renew or replace</span><span>Renew or replace</span></div></div>
  <div class="kb-tenor-row"><h2>NVIDIA backstop</h2><div class="kb-long-term">Six-year capacity commitment</div></div>
 </div>
 <div class="kb-bank-flow"><b>Contracted fallback revenue</b><span aria-hidden="true">→</span><b>Cluster financing</b></div>
 <p class="k-credit">${credit(source.july,'SemiAnalysis · July 6, 2026')} · ${credit(source.nvidia,'NVIDIA · July 2026 filing')}</p>`);}
function risk(){return wrap(`
 <div class="kb-risk-grid"><section><h2>Customers rent the GPUs</h2><div class="kb-risk-arrow" aria-hidden="true">↓</div><strong>Cloud earns market revenue</strong><div class="kb-share">NVIDIA receives an agreed share of the upside</div></section><section><h2>Capacity goes unsold</h2><div class="kb-risk-arrow" aria-hidden="true">↓</div><strong>NVIDIA buys the capacity</strong><div class="kb-share">NVIDIA may be unable to use or resell it</div></section></div>
 <div class="kb-exposure"><strong>$36 billion</strong><span>NVIDIA AI-cloud commitments<br>July 26, 2026</span></div>
 <p class="k-credit">${credit(source.september,'SemiAnalysis · September 11, 2026')} · ${credit(source.nvidia,'NVIDIA · commitments and risks')}</p>`);}
export function backstopVisual(id){switch(id){case 'nvidia-coreweave-backstop':return coreweave();case 'nvidia-backstop-financing':return financing();case 'nvidia-backstop-risk':return risk();default:return null;}}
