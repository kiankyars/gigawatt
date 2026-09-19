export const learningContract = Object.freeze({
 driving_question: 'What lets several AI racks advance one model together?',
 fixed_boundary: 'GB300 rack scale-up is the starting point. The fabric calculations hold sixteen 400 Gb/s endpoint links fixed.',
 changed_variable: 'Uplink capacity, traffic placement, shared queues, fiber distance and the condition of a physical link.',
 primary_payoff: 'Trace a workload delay to the physical link or shared resource that constrains it.',
 misconception: 'A fast endpoint port or a healthy accelerator count establishes fast distributed training.',
 closing_question: 'Which measurement distinguishes a moved-link fault from shared-fabric congestion?',
});
const topology='d08-topology-budget',collective='d08-collective-progress',media='d08-copper-light-service';
const c=(key,label,options)=>({key,label,options});
export const initialState={uplinks:2,placement:'remote',ocsPairing:'straight',diagnosis:'',superfactoryView:'overview'};
export const scenes=[
 {id:'networking-purpose',label:'Networking and interconnects',title:'Networking and interconnects',reference:topology,pedagogical_role:'problem'},
 {id:'consumer-hardware-meme',label:'AI demand and consumer hardware',title:'AI demand and consumer hardware',reference:topology,pedagogical_role:'hook',imageOnly:true},
 {id:'three-scales',label:'Three communication scales',title:'A distributed model uses different networks at different scales.',reference:topology,pedagogical_role:'architecture'},
 {id:'microsoft-ai-superfactory',label:'Inside an AI Superfactory',title:'Inside an AI Superfactory',reference:topology,pedagogical_role:'case',imageOnly:true,controls:[c('superfactoryView','View',[['overview','Overview'],['campus','Campus scale'],['hall','Inside the data hall']])]},
 {id:'fairwater-model-scale',label:'Fairwater model scale',title:'Microsoft’s ambition for Fairwater',reference:topology,pedagogical_role:'case',imageOnly:true},
 {id:'packet-path',label:'Data hierarchy',title:'Data hierarchy for each networking paradigm',reference:topology,pedagogical_role:'mechanism'},
 {id:'shared-model',label:'A model across several GPUs',title:'Split a model across GPUs, and they must exchange results.',reference:collective,pedagogical_role:'mechanism'},
 {id:'network-hardware',label:'The adapter and the switch',title:'Scale-out networking: the adapter and the switch',reference:topology,pedagogical_role:'architecture'},
 {id:'physical-fabric',label:'A real leaf–spine path',title:'One path through a DGX H100 SuperPOD',reference:topology,pedagogical_role:'case'},
 {id:'leaf-spine',label:'Leaf–spine is common, not universal',title:'Leaf–spine is common, not universal',reference:topology,pedagogical_role:'architecture',imageOnly:true},
 {id:'copper-and-light',label:'Copper and optical links',title:'Copper for short links; optical fiber for longer runs.',reference:media,pedagogical_role:'mechanism'},
 {id:'optical-packaging',imageOnly:true,label:'Pluggable and co-packaged optics',title:'Co-packaged optics shortens the electrical path inside the switch.',reference:media,pedagogical_role:'comparison'},
 {id:'shared-uplinks',label:'Where the bandwidth narrows',title:'Cross-leaf bandwidth is shared by the servers beneath each leaf.',reference:topology,pedagogical_role:'balance',controls:[c('uplinks','Uplinks available at each leaf',[[2,'Two'],[4,'Four']])]},
 {id:'traffic-placement',label:'When oversubscription matters',title:'Traffic staying within a leaf avoids its shared uplinks.',reference:topology,pedagogical_role:'comparison',controls:[c('placement','Server placement',[['remote','Across two leaves'],['local','Under one leaf']])]},
 {id:'incast',label:'Several senders, one receiver',title:'Four fast senders can overwhelm one receiver port.',reference:topology,pedagogical_role:'mechanism'},
 {id:'ethernet-infiniband',label:'Ethernet and InfiniBand',title:'Meta built large AI clusters with both Ethernet and InfiniBand.',reference:collective,pedagogical_role:'case'},
 {id:'optical-circuits',label:'Google TPU v4: optical routing',title:'An optical circuit switch changes which fiber endpoints connect.',reference:media,pedagogical_role:'mechanism',controls:[c('ocsPairing','Circuit configuration',[['straight','A ↔ C · B ↔ D'],['crossed','A ↔ D · B ↔ C']])]},
 {id:'campus-fiber',imageOnly:true,label:'From the cluster to a carrier',title:'The campus fiber handoff connects the cluster to an external service.',reference:topology,pedagogical_role:'architecture'},
 {id:'distance-latency',label:'Distance remains in the budget',title:'100 km of fiber adds a 1 ms round trip.',reference:topology,pedagogical_role:'balance'},
 {id:'network-diagnosis',label:'Find the delayed link',title:'One server is slow. Where would you check first?',reference:collective,pedagogical_role:'transfer'},
 {id:'meta-rsc',label:'Meta Research SuperCluster',title:'Meta built storage in tiers to keep GPUs supplied',reference:'d09-storage-paths',pedagogical_role:'case'},
];
export function resolveNetworkingScene(hash){
 const index=scenes.findIndex(s=>s.id===hash);
 return index<0?0:index;
}
