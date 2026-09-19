import {electricityPerBilledHour} from './capacity-model.js';

export function renderEnergyCost(){
  return `<div class="ke-energy">
    <p class="ke-context">Example · 100 hours · site power allocated to one GPU</p>
    <div class="ke-columns">
      <section class="ke-calculation" aria-label="Energy used during rented and idle hours">
        <div class="ke-state"><h2>Rented</h2><p>80 h × 1 kW = <b>80 kWh</b></p></div>
        <div class="ke-state"><h2>Powered, idle</h2><p>20 h × 0.2 kW = <b>4 kWh</b></p></div>
        <p class="ke-total"><b>84 kWh</b> ÷ <b>80 billed hours</b></p>
      </section>
      <section class="ke-payoff" aria-label="Electricity per billed GPU-hour">
        <div class="ke-per-hour"><strong>1.05</strong><span>kWh per billed GPU-hour</span></div>
        <div class="ke-tariffs" aria-label="Electricity cost per billed GPU-hour">
          <div><span>$80/MWh</span><b>$${electricityPerBilledHour().toFixed(3)}</b></div>
          <div><span>$160/MWh</span><b>$${electricityPerBilledHour({tariffPerMWh:160}).toFixed(3)}</b></div>
        </div>
        <p class="ke-cost-unit">Electricity cost per billed GPU-hour</p>
      </section>
    </div>
  </div>`;
}

export function renderEnergyPassThrough(source){
  const increase=(electricityPerBilledHour({tariffPerMWh:160})-electricityPerBilledHour()).toFixed(3);
  return `<div class="ke-pass-through">
    <p class="ke-context">From the previous example: electricity costs $${increase} more per billed GPU-hour</p>
    <div class="ke-contracts">
      <section><h2>Fixed all-in price</h2><p class="ke-risk-owner">Provider absorbs it</p><p class="ke-contract-impact">Margin −$${increase} / GPU-hour</p></section>
      <section><h2>Electricity pass-through</h2><p class="ke-risk-owner">Customer reimburses it</p><p class="ke-contract-impact">Bill +$${increase} / GPU-hour</p></section>
    </div>
    <div class="ke-real-contract"><p><b>Core Scientific → CoreWeave</b><br>Power billed separately, without markup</p><p class="k-credit"><a href="${source}" target="_blank" rel="noreferrer">Core Scientific · Q2 2026 filing · Electricity Costs</a></p></div>
  </div>`;
}
