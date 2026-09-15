export const learningContract = Object.freeze({
 driving_question: 'What lets several AI racks advance one model together?',
 fixed_boundary: 'GB300 rack scale-up is the starting point. The fabric calculations hold sixteen 400 Gb/s endpoint links fixed.',
 changed_variable: 'Uplink capacity, traffic placement, message size, shared queues and exposed communication time.',
 primary_payoff: 'Trace a workload delay to the physical link or shared resource that constrains it.',
 misconception: 'A fast endpoint port or a healthy accelerator count establishes fast distributed training.',
 closing_question: 'Which intervention restores progress when a collective is slowed by one congested uplink?',
});
const topology='d08-topology-budget',collective='d08-collective-progress',media='d08-copper-light-service';
const c=(key,label,options)=>({key,label,options});
export const initialState={transfer:'local',uplinks:2,placement:'remote',message:'large',ringRound:0,collectiveRate:50,ocsPairing:'straight',diagnosis:'',showDiagnosis:false};
export const scenes=[
 {id:'networking-purpose',label:'Networking and interconnects',title:'Networking and interconnects',reference:topology,pedagogical_role:'problem'},
 {id:'consumer-hardware-meme',label:'AI demand and consumer hardware',title:'AI demand and consumer hardware',reference:topology,pedagogical_role:'hook',imageOnly:true},
 {id:'three-scales',label:'Three communication scales',title:'A distributed model uses different networks at different scales.',reference:topology,pedagogical_role:'architecture'},
 {id:'packet-path',label:'From local memory to a peer GPU',title:'Where does the data need to go?',reference:topology,pedagogical_role:'mechanism',controls:[c('transfer','Follow the data',[['local','GPU memory'],['rack','Inside the rack'],['cluster','Across racks']])]},
 {id:'shared-model',label:'A model across several GPUs',title:'Split a model across GPUs, and they must exchange results.',reference:collective,pedagogical_role:'mechanism'},
 {id:'network-hardware',label:'The adapter and the switch',title:'A network adapter connects a server; a switch connects many adapters.',reference:topology,pedagogical_role:'architecture'},
 {id:'copper-and-light',label:'Copper and optical links',title:'Optical links convert between electrical signals and light at their endpoints.',reference:media,pedagogical_role:'mechanism'},
 {id:'optical-packaging',label:'Pluggable and co-packaged optics',title:'Co-packaged optics shortens the electrical path inside the switch.',reference:media,pedagogical_role:'comparison'},
 {id:'leaf-spine',label:'Build a leaf–spine fabric',title:'Leaf switches connect the servers; spine switches connect the leaves.',reference:topology,pedagogical_role:'architecture'},
 {id:'shared-uplinks',label:'Where the bandwidth narrows',title:'Cross-leaf bandwidth is shared by the servers beneath each leaf.',reference:topology,pedagogical_role:'balance',controls:[c('uplinks','Uplinks available at each leaf',[[2,'Two'],[4,'Four']])]},
 {id:'traffic-placement',label:'When oversubscription matters',title:'Traffic staying within a leaf avoids its shared uplinks.',reference:topology,pedagogical_role:'comparison',controls:[c('placement','Place the communicating servers',[['remote','Across two leaves'],['local','Under one leaf']])]},
 {id:'message-time',label:'Bandwidth and latency',title:'Small messages expose latency; large messages occupy the link.',reference:topology,pedagogical_role:'comparison'},
 {id:'incast',label:'Several senders, one receiver',title:'Traffic queues at the switch port leading to a shared receiver.',reference:topology,pedagogical_role:'mechanism'},
 {id:'all-reduce',label:'What an all-reduce returns',title:'Training workers combine their gradients before the next update.',reference:collective,pedagogical_role:'mechanism'},
 {id:'ring-collective',label:'Watch a ring all-reduce',title:'A ring first combines gradient chunks, then distributes the results.',reference:collective,pedagogical_role:'mechanism',controls:[c('ringRound','Communication phase',[[0,'Input'],[3,'After reduction'],[6,'After distribution']])]},
 {id:'collective-time',label:'Communication on the critical path',title:'Only communication that remains exposed extends the training step.',reference:collective,pedagogical_role:'comparison',controls:[c('collectiveRate','Payload bandwidth on each ring edge',[[50,'50 GB/s'],[25,'25 GB/s']])]},
 {id:'ethernet-infiniband',label:'Ethernet and InfiniBand',title:'Meta built large AI clusters with both Ethernet and InfiniBand.',reference:collective,pedagogical_role:'case'},
 {id:'tpu-interconnect',label:'Google TPU v4',title:'TPU v4 connects 4,096 chips through a reconfigurable inter-chip network.',reference:collective,pedagogical_role:'case'},
 {id:'optical-circuits',label:'What an optical circuit switch changes',title:'An optical circuit switch changes which fiber endpoints connect.',reference:media,pedagogical_role:'mechanism',controls:[c('ocsPairing','Circuit configuration',[['straight','A ↔ C · B ↔ D'],['crossed','A ↔ D · B ↔ C']])]},
 {id:'campus-fiber',label:'From the cluster to a carrier',title:'The campus fiber handoff connects the cluster to an external service.',reference:topology,pedagogical_role:'architecture'},
 {id:'distance-latency',label:'Distance remains in the budget',title:'A faster port cannot remove the propagation time between facilities.',reference:topology,pedagogical_role:'balance'},
 {id:'fabric-failure',label:'A degraded link delays the collective',title:'A fabric can remain connected while the training step gets slower.',reference:collective,pedagogical_role:'failure'},
 {id:'network-diagnosis',label:'Chapter 9 knowledge check',title:'Chapter 9 · Find the source of the collective delay',reference:collective,pedagogical_role:'transfer'},
 {id:'storage-handoff',label:'The network’s other traffic',title:'Dataset reads and checkpoints also use the network.',reference:topology,pedagogical_role:'transfer'},
];
