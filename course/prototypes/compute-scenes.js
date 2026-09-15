export const learningContract = Object.freeze({
  driving_question: 'What inside an AI rack determines the useful work it can deliver?',
  fixed_boundary: 'NVIDIA GB300 NVL72 is the physical anchor. Operation-rate and allocation experiments use their explicitly supplied resources and job rules.',
  changed_variable: 'Data location, reuse, limiting resource, and fault placement change independently.',
  primary_payoff: 'Identify the physical resource or job dependency that an upgrade or repair must restore.',
  misconception: 'Aggregate memory, peak FLOPS or a healthy GPU count establish application throughput.',
  closing_question: 'Which intervention changes the limiting dependency for the same job?',
});
const data='d07-data-path', bound='d07-bottleneck-model', rack='d07-rack-as-system';
const c=(key,label,options)=>({key,label,options});
export const initialState={path:'load',tokens:1,intensity:10,jobSize:8,diagnosis:'',showDiagnosis:false};
export const scenes=[
 {id:'compute-purpose',label:'Compute, memory and the rack',title:'Compute, memory and the rack',reference:data,pedagogical_role:'problem'},
 {id:'consumer-hardware-meme',label:'AI data centers and consumer hardware',title:'AI data centers and consumer hardware',reference:data,pedagogical_role:'transition',imageOnly:true},
 {id:'rack',label:'One GB300 NVL72',title:'One GB300 NVL72 connects 72 GPUs in a rack.',reference:rack,pedagogical_role:'architecture'},
 {id:'tray',label:'Inside the compute tray',title:'Each compute tray contains four GPUs and two CPUs.',reference:rack,pedagogical_role:'architecture'},
 {id:'superchip',label:'CPU and GPU roles',title:'A Grace CPU coordinates two Blackwell Ultra GPUs.',reference:data,pedagogical_role:'mechanism'},
 {id:'data-path',label:'Follow the data',title:'The data’s location determines which interface carries it.',reference:data,pedagogical_role:'mechanism',controls:[c('path','Trace a transfer',[['load','Load from storage'],['local','Read local HBM'],['peer','Exchange a result']])]},
 {id:'hbm-package',label:'HBM beside the GPU',title:'High-bandwidth memory connects to the GPU through an interposer.',reference:data,pedagogical_role:'mechanism'},
 {id:'memory-locality',label:'Coherent memory and locality',title:'A shared address space still contains physically different memories.',reference:data,pedagogical_role:'comparison'},
 {id:'capacity-bandwidth',label:'Capacity versus bandwidth',title:'288 GB describes storage capacity; 8 TB/s describes a transfer rate.',reference:bound,pedagogical_role:'comparison'},
 {id:'weight-read',label:'Time one memory transfer',title:'Reading 144 GB takes at least 18 ms at 8 TB/s.',reference:bound,pedagogical_role:'balance'},
 {id:'operand-reuse',label:'Reuse a weight tile',title:'A weight tile can serve several token vectors before leaving on-chip memory.',reference:bound,pedagogical_role:'mechanism',controls:[c('tokens','Token vectors using the tile',[[1,'One'],[8,'Eight']])]},
 {id:'peak-flops',label:'Read a performance specification',title:'A FLOPS number depends on the operation, precision and sparsity.',reference:bound,pedagogical_role:'counterexample'},
 {id:'operation-bounds',label:'Two different bottlenecks',title:'Faster arithmetic helps only when arithmetic is the limiting work.',reference:bound,pedagogical_role:'comparison'},
 {id:'roofline',label:'The roofline model',title:'Data reuse moves an operation from the memory limit toward the compute limit.',reference:bound,pedagogical_role:'mechanism',controls:[c('intensity','Work per HBM byte',[[1,'1 FLOP/B'],[10,'10 FLOP/B'],[25,'25 FLOP/B'],[100,'100 FLOP/B']])]},
 {id:'switched-rack',label:'Inside the NVLink domain',title:'NVSwitch carries GPU-to-GPU traffic across the rack.',reference:rack,pedagogical_role:'architecture'},
 {id:'model-placement',label:'Place the model across GPUs',title:'Partitioning a layer creates communication inside every model step.',reference:data,pedagogical_role:'mechanism'},
 {id:'rack-interfaces',label:'Data, power and coolant',title:'The rack’s rear connects three different physical systems.',reference:rack,pedagogical_role:'architecture'},
 {id:'tray-repair',label:'The unit being repaired',title:'Removing a compute tray takes its four GPUs out of service.',reference:rack,pedagogical_role:'mechanism'},
 {id:'fault-placement',label:'Healthy GPUs versus runnable jobs',title:'The location of a failure can matter more than the number of failed GPUs.',reference:rack,pedagogical_role:'comparison',controls:[c('jobSize','Job requires GPUs within one group',[[8,'Eight GPUs'],[4,'Four GPUs']])]},
 {id:'recover-work',label:'Return the job to service',title:'A replacement tray must pass checks before the job resumes.',reference:rack,pedagogical_role:'mechanism'},
 {id:'diagnose-upgrade',label:'Choose the useful upgrade',title:'Chapter 9 · Diagnose the limiting resource',reference:bound,pedagogical_role:'transfer'},
 {id:'network-handoff',label:'From one rack to a cluster',title:'Networking and interconnects',reference:data,pedagogical_role:'transfer'},
];
