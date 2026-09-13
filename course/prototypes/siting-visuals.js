import { renderGeneration, generationScenes } from './siting-generation.js';
import { renderProcurement } from './siting-procurement.js';
import { renderSitingCase } from './siting-case-visuals.js';

export function renderSiting(id,state,compact=false){
 const scene=renderSitingCase(id,state,compact);
 if(scene)return scene;
 if(generationScenes.some(scene=>scene.id===id))return renderGeneration(id,state,compact);
 if(['procurement-route','transport-current','parallel-circuits','procurement-decision'].includes(id))return renderProcurement(id,state,compact);
 throw new RangeError(`Unknown siting scene: ${id}`);
}
