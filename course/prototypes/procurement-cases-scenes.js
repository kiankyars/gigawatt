import {rapidBuildScenes} from './rapid-build-cases.js';
const delivery='d13-delivery-dependencies', interfaces='d13-interface-contracts', acceptance='d13-commissioning-complete-paths';
const c=(key,label,options)=>({key,label,options});
const s=(id,label,title,reference,objective,explanation,extra={})=>({id,label,title,reference,objective,pedagogical_role:'mechanism',explanation:[explanation],...extra});
export const learningContract=Object.freeze({driving_question:'How does a design become a tested, usable service?',fixed_boundary:'A 20 MW IT phase in ten 2 MW zones, ending at integrated service acceptance.',changed_variable:'Rack density, delivery bottlenecks, factory assembly and acceptance scope.',primary_payoff:'Connect equipment choices and factory work to the date at which tested racks can operate.',misconception:'Unchanged total MW means unchanged interfaces and delivery dates.',closing_question:'How can the next phase connect while the first stays online?'});
export const initialState={intervention:'baseline',factoryWeeks:6,approvalWeek:0,factorySlotWeek:0,boundary:'coolant',rackKW:200,action:'unconfirmed',testPhase:'fault',coolingStart:21,electrical:false,hydraulic:false,geometry:false,logistics:false,controls:false,resources:false};
export const scenes=[
 s('epc-and-prefab','EPC','Engineering, Procurement and Construction (EPC)',delivery,'D13.2','For a prefabricated electrical plant, engineering sets the topology and connections, procurement orders the switchgear-transformer package, and construction prepares the foundations and installs the package. Prefabrication is a construction strategy, not a replacement for those responsibilities.'),
 s('rack-case-brief','Case study: the rack changes','Case study: the rack design changes during construction',interfaces,'D13.2','A 20 MW IT phase is under construction. The rack design changes from 100 kW to 200 kW while total IT duty remains fixed.',{pedagogical_role:'problem'}),
 s('rack-change','Twenty megawatts, new racks','The same 20 MW is concentrated into half as many racks.',interfaces,'D13.2','Ten 2 MW zones change from twenty 100 kW racks per zone to ten 200 kW racks. The following three slides track what this change does to each electrical branch, coolant branch and support position.',{pedagogical_role:'comparison'}),
 s('electrical-interface','Rack change: electrical','The new rack exceeds its existing electrical branch rating.',interfaces,'D13.2','Continue the same 20 MW case. Balanced 480 V three-phase, PF 1, one full-duty supply path: 120.3 A at 100 kW becomes 240.6 A at 200 kW, exceeding the old allowable continuous 160 A. The rack count falls, but branch cables, terminals and protection must change.'),
 s('hydraulic-interface','Rack change: coolant','Doubling rack flow can require four times the pressure difference.',interfaces,'D13.2','Continue the same 20 MW case. All IT heat enters water, cp 4.18 kJ/(kg·K), rise at most 10 K. Flow rises from 2.39 to 4.78 kg/s. Reused hardware with quadratic pressure-flow behavior requires an inlet-to-outlet pressure difference of 80 rather than 20 kPa, above the available 60 kPa. This difference is the pressure lost through the branch; the pump must overcome it along with the remaining circuit losses. Whole-zone heat and flow remain unchanged.'),
 s('spatial-interface','Rack change: supports','The rack change concentrates the floor load at fewer positions.',interfaces,'D13.2','Continue the same 20 MW case. The vendor drawing stipulates twice the installed mass on the same four feet, equally shared. Half as many racks preserves zone mass but doubles occupied-position and foot loads. Check supports and anchorage against the revised drawing.'),
 s('factory-and-site','Assemble while the site is prepared','Prefabrication overlaps factory assembly with site construction.',delivery,'D13.2','Electrical and cooling components can arrive as tested assemblies with their internal distribution, manifolds, wiring and controls already installed. Civil works, utility access and foundations can proceed in parallel with this factory assembly. Site scope includes placement, field connections and integrated commissioning.',{imageOnly:true}),
 {...rapidBuildScenes.find(item=>item.id==='aws-houdini-prefab'),title:'Project Houdini moves data-hall assembly into factories.',objective:'D13.1'},
 s('compass-package','A real electrical skid','Siemens and Compass combine switchgear and a transformer on one skid.',interfaces,'D13.2','Siemens and Compass co-developed a medium-voltage skid with 8DJH 36 switchgear and a transformer. Factory assembly consolidates the connection between these components into a repeatable package. The photograph shows its switchgear portion; the transformer is outside the frame.',{pedagogical_role:'case-study',sources:['https://www.siemens.com/en-us/company/insights/compass-datacenters-case-study/']}),
 s('interface-owner','Open Compute Project','Open Compute Project defines the interfaces between suppliers.',interfaces,'D13.2','The Open Compute Project publishes specifications for shared equipment interfaces. UQD-compliant couplings of the same nominal size interoperate, but the rack still needs sufficient branch flow and pressure. A common connector specification does not establish a complete rack cooling performance rating.',{pedagogical_role:'case-study',sources:['https://www.opencompute.org/documents/open-rack-base-specification-version-3-pdf','https://www.opencompute.org/documents/ocp-universal-quick-disconnect-uqd-specification-rev-1-0-2-pdf']}),
 s('ocp-rack-example','An Open Rack example','An Open Rack example',interfaces,'D13.2','User-supplied Open Compute Project Basics diagram compares conventional server-level PSUs with consolidated rack-level PSUs in an open-source rack. It illustrates a rack architecture choice; it is not a current GB300 equipment specification.',{imageOnly:true}),
 s('factory-acceptance','Factory acceptance tests','Prefabrication moves acceptance testing into the factory.',acceptance,'D13.3','FAT means factory acceptance test. Testing internal wiring, plumbing and controls before shipment can reduce on-site troubleshooting. Site connections and integrated operation still need acceptance testing.'),
 s('accepted-paths','Count complete paths','Which racks have power, cooling and networking ready?',acceptance,'D13.3','Continue with the revised 100 racks at 200 kW, totaling 20 MW. Electrical acceptance covers A01–A80, cooling A21–A100 and network A01–A60. Their overlap is 40 racks, or 8 MW, assuming all other acceptance criteria met. Cooling extended to A01 gives 60 racks and 12 MW.',{controls:[c('coolingStart','Cooling acceptance',[[21,'A21–A100'],[1,'A01–A100']])]}),
 s('phase-boundary','Connect the next phase','Connect the next 50 MW while keeping the first 50 MW online.',acceptance,'D13.4','Return to Applied Digital’s Polaris Forge 1 in Ellendale, leased to CoreWeave: the first 50 MW reached ready-for-service on October 27, 2025, followed by another 50 MW on November 24. The two October presentation photographs repeat the earlier case study. Phased delivery introduces an additional design requirement: connecting the next phase must preserve the infrastructure serving the operating phase. The public releases establish the delivery milestones; they do not document a specific shared topology or outage.',{pedagogical_role:'case-study',sources:['https://ir.applieddigital.com/news-events/press-releases/detail/133/applied-digital-achieves-ready-for-service-for-phase-1-at','https://ir.applieddigital.com/news-events/press-releases/detail/137/applied-digital-completes-phase-ii-ready-for-service-at']}),
];

export const sceneAliases=Object.freeze({
 'delivery-purpose':'epc-and-prefab',
 'schedule-case-brief':'factory-and-site',
 'critical-path':'factory-and-site',
 'delivery-paths':'factory-and-site',
 'service-requirements':'factory-acceptance',
 'parallel-schedules':'factory-and-site',
 'manufacturing-release':'interface-owner',
 'module-transport':'factory-and-site',
 'release-holds':'electrical-interface',
 'approval-delay':'factory-and-site',
 'site-checks':'factory-acceptance',
 'handover-records':'phase-boundary',
 'release-decision':'phase-boundary',
});
export function resolveProcurementScene(hash){
 const id=sceneAliases[hash]||hash;
 const index=scenes.findIndex(scene=>scene.id===id);
 return index<0?0:index;
}
