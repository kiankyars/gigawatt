const C = {
  text: 'var(--text)', muted: 'var(--muted)', line: 'var(--line)',
  panel: 'var(--panel)', surface: 'var(--surface)',
  power: 'var(--power)', heat: 'var(--heat)',
};
const esc = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const text = (x, y, value, size = 22, color = C.text, anchor = 'start') =>
  `<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}">${esc(value)}</text>`;
const line = (x, y, xx, yy, color = C.line, width = 2) =>
  `<path d="M${x} ${y}L${xx} ${yy}" stroke="${color}" stroke-width="${width}" fill="none"/>`;
const rect = (x, y, width, height, color = C.panel, stroke = C.line, radius = 12) =>
  `<rect x="${x}" y="${y}" width="${width}" height="${height}" rx="${radius}" fill="${color}" stroke="${stroke}"/>`;
const link = (x, y, label, url, size = 16, anchor = 'start') =>
  `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${text(x, y, label, size, C.muted, anchor)}</a>`;
const money = dollars => `$${(dollars / 1e6).toFixed(1)}M`;

export const economicSources = Object.freeze({
  anthropic: 'https://content.spacex.com/cms-assets/FINAL_Documents%20and%20Updates/SpaceX%20-%20EU%20Prospectus%20%28Approved%20by%20Bafin%29%20-%20June%205%2C%202026.pdf#page=77',
  google: 'https://www.sec.gov/Archives/edgar/data/1181412/000162828026041150/spacexagreementfwp.htm',
  forecast: 'https://newsletter.semianalysis.com/p/spacex-10gw-in-2027-why-its-real',
});

/**
 * Original sensitivity calculation. No contract fees or inferred site MW enter
 * this model. Contribution excludes the incremental fuel penalty measured here,
 * so that penalty is subtracted once, over the stated comparison horizon.
 */
export function speedPremium({
  outputMW = 100,
  fastEfficiency = 0.4,
  efficientEfficiency = 0.6,
  fuelPricePerMWh = 20,
  annualHours = 8760,
  earlierMonths = 1,
  fasterBuildPremium = 0,
  contributionPerMonth = null,
} = {}) {
  for (const [name, value] of Object.entries({ outputMW, fuelPricePerMWh, annualHours, fasterBuildPremium })) {
    if (!Number.isFinite(value) || value < 0) throw new RangeError(`${name} must be finite and nonnegative`);
  }
  for (const value of [fastEfficiency, efficientEfficiency]) {
    if (!Number.isFinite(value) || value <= 0 || value > 1) throw new RangeError('Efficiency must be greater than zero and at most one');
  }
  if (fastEfficiency > efficientEfficiency) throw new RangeError('The efficient option must have at least the fast option’s efficiency');
  if (annualHours > 8760) throw new RangeError('Annual duty exceeds this 365-day example');
  if (!Number.isFinite(earlierMonths) || earlierMonths <= 0) throw new RangeError('Earlier months must be finite and positive');
  if (contributionPerMonth !== null && !Number.isFinite(contributionPerMonth)) throw new RangeError('Contribution must be finite or unknown');

  const outputMWh = outputMW * annualHours;
  const fastFuelMWh = outputMWh / fastEfficiency;
  const efficientFuelMWh = outputMWh / efficientEfficiency;
  const fastFuelCost = fastFuelMWh * fuelPricePerMWh;
  const efficientFuelCost = efficientFuelMWh * fuelPricePerMWh;
  const annualFuelPenalty = fastFuelCost - efficientFuelCost;
  const requiredEarlierContribution = annualFuelPenalty + fasterBuildPremium;
  const earlierContribution = contributionPerMonth === null ? null : earlierMonths * contributionPerMonth;
  return Object.freeze({
    outputMW, outputMWh, annualHours, earlierMonths, fastEfficiency,
    efficientEfficiency, fuelPricePerMWh, fasterBuildPremium,
    fastFuelMWh, efficientFuelMWh, fastFuelCost, efficientFuelCost,
    annualFuelPenalty, requiredEarlierContribution,
    requiredMonthlyContribution: requiredEarlierContribution / earlierMonths,
    earlierContribution,
    advantage: earlierContribution === null ? null : earlierContribution - requiredEarlierContribution,
  });
}

function contracts(compact) {
  let out = '';
  const cards = [
    ['Anthropic', '$1.25B', 'Full fees after May–June ramp', 'Colossus + Colossus II'],
    ['Google', '$920M', 'Full fees from October 2026', 'Committed compute capacity'],
  ];
  out += text(compact ? 24 : 48, compact ? 30 : 32, 'DISCLOSED MONTHLY SERVICE FEES', compact ? 15 : 18, C.muted);
  cards.forEach(([name, fee, timing, scope], i) => {
    const x = compact ? 24 : 48 + 536 * i;
    const y = compact ? 54 + 168 * i : 58;
    const width = compact ? 342 : 488;
    out += rect(x, y, width, compact ? 152 : 204);
    out += text(x + 20, y + (compact ? 33 : 43), name, compact ? 24 : 30);
    out += text(x + 20, y + (compact ? 84 : 112), fee, compact ? 43 : 55, C.power);
    out += text(x + 20, y + (compact ? 112 : 151), timing, compact ? 15 : 19, C.muted);
    out += text(x + 20, y + (compact ? 135 : 180), scope, compact ? 15 : 19, C.muted);
  });
  if (compact) {
    out += text(195, 426, '$2.17B / month', 37, C.power, 'middle');
    out += text(195, 456, 'Both at full service · before costs', 17, C.muted, 'middle');
    out += text(195, 485, '90-day termination rights', 17, C.text, 'middle');
    out += text(195, 507, 'after initial commitments', 15, C.muted, 'middle');
    out += line(24, 528, 366, 528);
    out += text(195, 557, '“That pays back the capex', 21, C.text, 'middle');
    out += text(195, 585, 'in less than a year.”', 21, C.text, 'middle');
    out += link(195, 612, 'SemiAnalysis · early-compute forecast', economicSources.forecast, 14, 'middle');
    out += link(24, 654, 'Anthropic filing ↗', economicSources.anthropic, 14);
    out += link(366, 654, 'Google filing ↗', economicSources.google, 14, 'end');
  } else {
    out += text(560, 309, '$2.17B / month', 43, C.power, 'middle');
    out += text(560, 343, 'Both at full service · before costs', 21, C.muted, 'middle');
    out += text(560, 377, '90-day termination rights after initial commitments', 19, C.muted, 'middle');
    out += line(48, 399, 1072, 399);
    out += text(560, 441, '“That pays back the capex in less than a year.”', 27, C.text, 'middle');
    out += link(560, 474, 'SemiAnalysis · early-compute pricing forecast · August 2026', economicSources.forecast, 18, 'middle');
    out += link(48, 518, 'Anthropic: SpaceX prospectus, p. 64 ↗', economicSources.anthropic);
    out += link(1072, 518, 'Google: SEC agreement disclosure ↗', economicSources.google, 16, 'end');
  }
  return {
    markup: `<g data-economics-scene="contract-economics" data-fee-basis="conditional-monthly-service-fees">${out}</g>`,
    description: 'SpaceX disclosed Anthropic service fees of $1.25 billion per month after the May–June 2026 ramp, across Colossus and Colossus II. Google agreed to $920 million monthly from October 2026, after reduced ramp fees and subject to delivery. The sum, $2.17 billion, is a conditional full-service monthly fee level before costs, not profit or cash already collected. Anthropic has 90-day termination rights after an initial three-month period; Google has 90-day rights after December 31, 2026. Below, a separately attributed SemiAnalysis projection describes sub-year capex recovery. This is not evidence these two contracts have already repaid their capex. The article’s 3–5 months refers to delivery lead time.',
  };
}

function speed(compact) {
  const model = speedPremium();
  let out = '';
  const fuelRows = [
    ['Simple cycle · 40%', model.fastFuelCost, C.heat],
    ['Combined cycle · 60%', model.efficientFuelCost, C.power],
  ];
  if (compact) {
    out += text(195, 29, '100 MW delivered · 24/7', 21, C.text, 'middle');
    out += text(195, 55, '$20/MWh of fuel · original assumptions', 15, C.muted, 'middle');
    fuelRows.forEach(([label, cost, color], i) => {
      const y = 95 + 104 * i;
      out += text(24, y, label, 20);
      out += rect(24, y + 15, 342 * cost / model.fastFuelCost, 26, color, color, 2);
      out += text(24, y + 67, `${money(cost)} fuel / year`, 21, color);
    });
    out += line(24, 294, 366, 294);
    out += text(195, 337, `${money(model.annualFuelPenalty)} extra fuel`, 29, C.heat, 'middle');
    out += text(195, 365, 'over one year', 19, C.muted, 'middle');
    out += text(195, 419, 'Open one month earlier when…', 21, C.text, 'middle');
    out += text(195, 461, 'Earlier-service contribution', 23, C.power, 'middle');
    out += text(195, 486, 'Fees less all other service costs', 16, C.muted, 'middle');
    out += text(195, 529, '>', 37, C.text, 'middle');
    out += text(195, 569, '$14.6M + faster-build costs', 23, C.heat, 'middle');
    out += text(195, 616, 'One year of extra fuel; add capital costs.', 15, C.muted, 'middle');
    out += text(195, 640, 'No contract revenue assigned to this site.', 15, C.muted, 'middle');
  } else {
    out += text(48, 34, '100 MW delivered · 24/7 · $20/MWh of fuel', 22);
    out += text(1072, 34, 'Original assumptions', 18, C.muted, 'end');
    fuelRows.forEach(([label, cost, color], i) => {
      const y = 89 + 116 * i;
      out += text(48, y, label, 25);
      out += rect(48, y + 19, 634 * cost / model.fastFuelCost, 34, color, color, 3);
      out += text(48, y + 85, `${money(cost)} fuel / year`, 26, color);
    });
    out += rect(745, 72, 327, 229);
    out += text(908.5, 122, 'EXTRA FUEL', 20, C.muted, 'middle');
    out += text(908.5, 192, money(model.annualFuelPenalty), 49, C.heat, 'middle');
    out += text(908.5, 239, 'over one year', 23, C.muted, 'middle');
    out += line(48, 327, 1072, 327);
    out += text(560, 369, 'Open one month earlier when…', 25, C.text, 'middle');
    out += text(285, 425, 'Earlier-service contribution', 29, C.power, 'middle');
    out += text(285, 459, 'Fees less all other service costs', 18, C.muted, 'middle');
    out += text(568, 431, '>', 44, C.text, 'middle');
    out += text(848, 425, '$14.6M + faster-build costs', 29, C.heat, 'middle');
    out += text(848, 459, 'One year of extra fuel, plus capital costs', 18, C.muted, 'middle');
    out += text(560, 517, 'A sensitivity example: no disclosed contract revenue is assigned to this 100 MW site.', 17, C.muted, 'middle');
  }
  return {
    markup: `<g data-economics-scene="speed-premium" data-extra-annual-fuel="${model.annualFuelPenalty}" data-revenue-assumed="false">${out}</g>`,
    description: `Original comparison at ${model.outputMW} MW delivered for ${model.annualHours} hours: fuel price is $20 per MWh of fuel energy, and efficiencies are 40% versus 60% on the same lower-heating-value basis. Annual fuel costs are ${money(model.fastFuelCost)} and ${money(model.efficientFuelCost)}. The faster, less efficient option spends ${money(model.annualFuelPenalty)} more on fuel over the assumed year. One month of earlier-service contribution must exceed that penalty plus added faster-build costs to win this simplified comparison. Contribution means fees minus all other service costs, before the incremental fuel penalty accounted for on the right. No revenue or profit from the disclosed contracts is assigned to this hypothetical 100 MW site. The chosen comparison horizon is one year of extra fuel; longer operation requires including further fuel penalties and applicable project costs.`,
  };
}

export function renderEconomics(id, state, compact = false) {
  if (id === 'contract-economics') return contracts(compact);
  if (id === 'speed-premium') return speed(compact);
  return null;
}
