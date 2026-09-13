import { renderGeneration, generationScenes } from './siting-generation.js';
import { renderProcurement } from './siting-procurement.js';
import { renderSitingCase } from './siting-case-visuals.js';
import { renderEconomics } from './siting-economics.js';

export function renderSiting(id,state,compact=false){
 const scene=renderSitingCase(id,state,compact);
 if(scene)return scene;
 const economics=renderEconomics(id,state,compact);
 if(economics)return economics;
 if(generationScenes.some(scene=>scene.id===id))return renderGeneration(id,state,compact);
 if(['procurement-route','transport-current'].includes(id))return renderProcurement(id,state,compact);
 throw new RangeError(`Unknown siting scene: ${id}`);
}
