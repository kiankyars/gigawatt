const rejection = 'd11-heat-rejection';
const weather = 'd11-weather-and-operating-envelope';
const water = 'd11-water-and-heat-reuse';
const c = (key, label, options) => ({key, label, options});
const s = (id, label, title, reference, objective, explanation, extra = {}) => ({
  id, label, title, reference, objective, pedagogical_role: 'mechanism',
  explanation: [explanation], ...extra,
});

export const learningContract = Object.freeze({
  driving_question: 'Where does the heat go when the weather or water supply changes?',
  fixed_boundary: 'Follow rack heat through the outdoor plant. The main operating example has a 10 MW site supply; the chiller illustration and dated Abilene case are separate.',
  changed_variable: 'Outdoor humidity, weather, computing power, water availability or customer demand.',
  primary_payoff: 'Trace the surviving heat path and explain which resource limits computing.',
  misconception: 'A closed rack loop eliminates water use, or enough cooling capacity guarantees enough electrical capacity.',
  closing_question: 'With no tower makeup water, which heat path survives and what must change?',
});
export const initialState = Object.freeze({
  humidity: 'dry', interfaceStep: 0, condition: 'cool', requestedITMW: 8,
  closedSink: 'air', mineralStage: 'evaporate', returnKnown: true,
  receiverHours: 6, choice: '', revealed: false,
});
// Keep existing bookmarks useful after folding the calculation and reuse-detail slides in.
export const sceneAliases = Object.freeze({
  'two-ceilings': 'hot-hour',
  'reuse-interface': 'heat-reuse',
});
export const scenes = Object.freeze([
  s('heat-rejection-purpose', 'Heat leaves the site', 'The Heat Still Has to Leave the Site', rejection, 'D11.1',
    'Continue the heat path from Chapter 11: chip, rack coolant, separate facility water, outdoor equipment and environment. The same rack can connect to different outdoor plants. Follow heat rather than assuming all the water is one circuit.', {pedagogical_role: 'problem'}),
  s('abilene-cooling', 'Abilene cooling', 'At Abilene, the heat goes to outdoor air.', water, 'D11.5',
    'Crusoe’s August 5, 2025 design account identifies a recirculating facility-water loop and air-cooled chillers. This dated design statement is not measured water use or performance. Initial fill and maintenance water remain. The Oracle aerial locates the campus; it does not identify cooling hardware. The following comparisons are teaching examples, not alternate Abilene operating modes.',
    {pedagogical_role: 'case-study', sources: ['https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center', 'https://www.oracle.com/data-centers/'], reviewed_on: '2026-09-16'}),
  s('rejection', 'Air or evaporation', 'Do you want your cooling wet or dry, sir?', rejection, 'D11.1',
    'A dry cooler passes outdoor air over a closed coil. In the open wet tower shown, nozzles distribute warm water over fill, which spreads it into films and droplets. Air contacts that exposed water and some water evaporates, cooling what remains. The water is not evaporating through holes in a closed coil. Most tower water recirculates; makeup replaces losses.'),
  s('bulb-definitions', 'Dry bulb and wet bulb', 'Dry bulb and wet bulb', weather, 'D11.3',
    'Dry-bulb temperature is the air temperature measured by a dry, shaded thermometer. Wet-bulb temperature is measured with a ventilated thermometer covered by a water-soaked wick. Evaporation cools that sensor. Wet bulb is lower than dry bulb in unsaturated air; the readings are equal at saturation. These are air measurements, not equipment types. The definition is course teaching text, not a quotation attributed to a manufacturer.'),
  s('weather', 'Why humidity matters', 'Humid air leaves less room for evaporative cooling.', weather, 'D11.3',
    'Hold ordinary air temperature, or dry bulb, at 35°C. A ventilated wetted sensor reads 22°C in the dry example and 28°C in the humid example. Evaporation cools it less in humid air. This wet-bulb reading describes an air condition and an evaporative opportunity; actual equipment needs a temperature gap above it.',
    {controls: [c('humidity', 'Humidity', [['dry', 'Low humidity'], ['humid', 'High humidity']])]}),
  s('approach-outdoors', 'Follow the temperatures', 'Dry coolers follow dry bulb; wet towers follow wet bulb.', weather, 'D11.3',
    'Reveal one interface at a time. This retains the reader’s separate synthetic 84 kW, fixed-approach example. Dry route: 35°C outdoor air, 40°C facility supply, 45°C rack supply. Wet route: 22°C wet bulb, 25°C tower water, 30°C facility water and 35°C rack supply. The rack limit is 35°C. Humid air raises the wet route to 41°C. Approaches are stipulated for this example, not universal ratings. The reader retains flow, return temperatures and heat-capacity assumptions.',
    {controls: [c('humidity', 'Humidity', [['dry', 'Low humidity'], ['humid', 'High humidity']])]}),
  s('chiller-balance', 'What a chiller adds', 'When do we need a chiller?', rejection, 'D11.2',
    'The CoolIT CHx2000 in Chapter 11 is a coolant distribution unit with pumps and a water-to-water heat exchanger, not a refrigeration compressor. When direct outdoor cooling cannot meet the required supply temperature, a chiller uses refrigeration to lift heat from a colder circuit to a warmer outdoor sink. This follows the outdoor-temperature comparison because it supplies the missing mechanism. Keep the separate simple chiller example: 10 MW collected plus 2 MW compressor electricity gives 12 MW condenser heat at steady state. Pumps and fans lie outside this illustration’s boundary. Air- and water-cooled chillers describe where the condenser sends heat.'),
  s('cooling-cop', 'Cooling per unit of electricity', 'COP tells us how much heat each unit of electricity moves.', rejection, 'D11.2',
    'Introduce coefficient of performance through four equal heat blocks and one electrical block. At whole-plant COP 4, one unit of electricity moves four units of heat. This includes cooling pumps and fans. It is heat transport, not electricity generation. Equipment-versus-plant boundary calculations remain in the reader; the main operating example uses whole-plant COP consistently.'),
  s('plant-options', 'Cool weather helps', 'Cool weather can let the compressor rest.', rejection, 'D11.1',
    'A waterside economizer uses a qualified outdoor cooling path to reduce or bypass compressor operation when outdoor conditions and the required supply temperature allow it. Fans and pumps still operate. Trace the bypass around the compressor; there is no universal outdoor temperature at which every plant can economize. The supplied illustration uses water from and to racks as a shortened heat-path description; a CDU may separate technology coolant from facility water.', {imageOnly:true}),
  s('adiabatic-assist', 'Water can help a dry coil', 'Wetted pads cool the air before it reaches the coil.', rejection, 'D11.1',
    'An adiabatic arrangement puts wetted pads upstream of a dry coil. Pad water evaporates while process liquid stays inside the coil. Dry air offers more evaporative benefit; humidity and equipment performance limit it. Pads add a water requirement and do not guarantee the required coolant temperature.'),
  s('hot-hour', 'Weather takes electrical headroom', 'Hot weather can leave less power for computing.', weather, 'D11.3',
    'Main synthetic operating example: 10 MW site supply, 0.4 MW other demand, initially 8 MW computing. Cool weather uses 1 MW cooling electricity, leaving the site at 9.4 MW. Hot weather uses 2 MW, taking the site to 10.4 MW even though 8 MW fits the 8.5 MW cooling capacity. Predict the weather change, then lower computing power until both checks pass. At 7.68 MW computing the hot plant uses 1.92 MW and the site totals 10 MW. COP is held constant within each supplied condition; actual load-dependent performance and controls need validation.',
    {pedagogical_role: 'counterexample', controls: [c('condition', 'Weather', [['cool', 'Cool'], ['hot', 'Hot']])]}),
  s('weather-bins', 'The difficult hours matter', 'An average can hide the hours that do not fit.', weather, 'D11.3',
    'Keep the same site and proposed 8 MW computing load. A day with twelve cool and twelve hot hours would have an average demand of 9.9 MW if that load were held, but the hot hours require 10.4 MW and cannot fit the 10 MW supply. The slide shows the hourly constraint without daily energy arithmetic. The reader retains the feasible dispatched schedule and its MWh totals.'),
  s('closed-loop-water', 'Follow the water circuit', 'A closed rack loop can still send heat to a wet tower.', water, 'D11.4',
    'Hold the closed rack and facility circuits fixed. Switch only the chiller’s outdoor arrangement: air-cooled condenser, or separate condenser water and an evaporative tower. The tower requires makeup water even though rack coolant recirculates. This generic comparison is not a claim that Abilene has both arrangements.',
    {controls: [c('closedSink', 'Outdoor arrangement', [['air', 'Air-cooled chiller'], ['tower', 'Water-cooled chiller + tower']])]}),
  s('water-ledger', 'Why replacement water is needed', 'Evaporation leaves dissolved minerals behind.', water, 'D11.4',
    'First let water evaporate: heat leaves, while dissolved minerals become more concentrated in the remaining water. Then discharge some concentrated water, called blowdown, and replace the evaporated and discharged water with makeup. Makeup water also brings minerals; treatment and water chemistry determine the feasible concentration. The picture is qualitative. Drift, leaks and the concentration-ratio derivation remain in the reader.',
    {controls: [c('mineralStage', 'Follow the water', [['evaporate', '1. Evaporate'], ['purge', '2. Discharge'], ['refill', '3. Refill']])], sources: ['https://www.energy.gov/cmei/femp/best-management-practice-10-cooling-tower-management'], reviewed_on: '2026-09-16'}),
  s('water-metrics', 'Intake and consumption', 'Water taken in and water consumed are different totals.', water, 'D11.4',
    'Use the reader’s small, separate one-day water example: 125 m³ enters, 100 m³ evaporates and 25 m³ leaves as blowdown. With verified return to the same basin, counted consumption is 100 m³. Without return evidence, do not assume that credit. No drift, leaks or storage change are included. Per-kWh water intensities, PUE and their period and boundary checks remain in the reader.',
    {controls: [c('returnKnown', 'Discharge destination', [[true, 'Same-basin return verified'], [false, 'Return unknown']])]}),
  s('heat-reuse', 'Heat needs a customer', 'The customer needs heat only part of the day.', water, 'D11.5',
    'The separate reuse example supplies 4 MW continuously; a customer can accept 2 MW for six hours, provided temperatures are compatible. A time-and-power chart shows the accepted overlap and the heat still needing outdoor rejection. If the customer closes, the full load still needs an outdoor path. A heat pump can raise delivery temperature but adds electricity; include distribution losses and pumping in a real comparison. The reader retains 12 of 96 MWh and 12.5% arithmetic.',
    {controls: [c('receiverHours', 'Customer', [[6, 'Open for 6 hours'], [0, 'Closed today']])]}),
  s('water-restriction', 'When water is unavailable', 'A water restriction can remove a cooling path.', water, 'D11.5',
    'Return to the main hot-hour site example. Tower makeup is unavailable, so sustained tower operation is unavailable. A separately qualified air-cooled alternate is supplied for this exercise. It can remove 8.5 MW of heat but consumes electricity inside the same 10 MW site limit. This is a synthetic operating brief, not Abilene performance.'),
  s('heat-rejection-check', 'Choose the surviving plan', 'Which plan keeps a complete heat path?', water, 'D11.5',
    'Choose a response to the hot day and water restriction, then explain the limiting resource before revealing numbers. The air-cooled alternate with reduced computing power fits both model limits. Keeping 8 MW exceeds site electricity. Keeping the tower ignores its missing makeup supply. The worked 7.68 MW operating point appears only after choosing and revealing; real transitions still require demonstrated flow, temperatures and controls.',
    {pedagogical_role: 'transfer'}),
]);
