export const learningContract=Object.freeze({
 driving_question:'How do storage and recovery turn powered GPUs into useful work that survives failures?',
 fixed_boundary:'One training job, its input data, saved progress and replacement resources.',
 changed_variable:'Checkpoint survival, save frequency, available placement and the completion deadline.',
 primary_payoff:'Connect storage and recovery choices to lost computation, energy and usable capacity.',
 misconception:'A saved file or enough free GPUs guarantees that a failed job can resume.',
 closing_question:'Which saved version and resource allocation can restore correct progress?',
});
const paths='d09-storage-paths',timeline='d09-checkpoint-timeline',service='d09-service-acceptance';
const c=(key,label,options)=>({key,label,options});
export const initialState={durability:'incomplete',replicaFault:'device',placement:'fragmented',failure:35,shift:true,deadline:20,diagnosis:'',showDiagnosis:false};
export const scenes=[
 {id:'llama-recovery',label:'Llama 3: 466 interruptions',title:'Llama 3 kept training through 466 interruptions',reference:timeline,pedagogical_role:'problem'},
 {id:'hardware-prices-meme',label:'RAM, GPUs, SSDs and CPUs',title:'RAM, GPUs, SSDs and CPUs',reference:paths,pedagogical_role:'transition',imageOnly:true},
 {id:'meta-rsc',label:'Meta Research SuperCluster',title:'Meta built storage in tiers to keep GPUs supplied',reference:paths,pedagogical_role:'architecture'},
 {id:'storage-roles',label:'Dataset, cache and checkpoint',title:'Feed the GPUs. Save their progress.',reference:paths,pedagogical_role:'architecture'},
 {id:'durability-boundary',label:'What survives a node failure',title:'Which save survives the failed worker?',reference:paths,pedagogical_role:'counterexample',controls:[c('durability','Newest save',[['incomplete','Incomplete shared copy'],['local','Complete local copy'],['remote','Complete shared copy']])]},
 {id:'replication-and-backup',label:'Replication and recovery copies',title:'A replica can copy the mistake, too',reference:timeline,pedagogical_role:'counterexample',controls:[c('replicaFault','What failed',[['device','One storage device'],['write','A bad application write']])]},
 {id:'tray-repair',label:'From tray repair to training',title:'Replacing hardware is only part of recovery',reference:service,pedagogical_role:'mechanism'},
 {id:'recovery-placement',label:'Free GPUs and usable allocations',title:'32 free GPUs. Can the job restart?',reference:service,pedagogical_role:'counterexample',controls:[c('placement','Free nodes',[['fragmented','Two in each group'],['together','Four in Group A']])]},
 {id:'checkpoint-policy',label:'Saving progress and repeating work',title:'Saving more often can reduce repeated work',reference:timeline,pedagogical_role:'comparison',controls:[c('failure','One failure at wall-clock minute',[[35,'35'],[55,'55'],[null,'No failure']])]},
 {id:'google-demand-response',label:'Google demand response',title:'Google deferred work to help the grid',reference:service,pedagogical_role:'architecture'},
 {id:'deadline-scheduling',label:'Move the work. Meet the deadline.',title:'Can we reduce demand and still finish on time?',reference:service,pedagogical_role:'balance',controls:[c('shift','Execution plan',[[false,'Continue through event'],[true,'Pause for grid event']]),c('deadline','Completion deadline',[[20,'20:00'],[17,'17:00']])]},
 {id:'recovery-diagnosis',label:'Choose a recovery plan',title:'Which recovery plan works?',reference:service,pedagogical_role:'transfer'},
];
