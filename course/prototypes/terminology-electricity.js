/* Primer diagrams. Ideal teaching circuits, not installation layouts. */
const esc = (value) => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;");
const text = (x, y, value, size = 22, color = "text", anchor = "middle") =>
  `<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}" fill="var(--${color})">${esc(value)}</text>`;
const path = (d, color = "power", width = 4, extra = "") =>
  `<path d="${d}" fill="none" stroke="var(--${color})" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" ${extra}/>`;
const arrow = (d, color = "power", width = 4) =>
  path(d, color, width, `marker-end="url(#primer-${color}-arrow)"`);
const rect = (x, y, w, h, color = "line", fill = "surface", radius = 12) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="var(--${fill})" stroke="var(--${color})" stroke-width="2"/>`;
const dot = (x, y, color = "power") => `<circle cx="${x}" cy="${y}" r="5" fill="var(--${color})"/>`;
const defs = `<defs>${["power", "heat", "data", "muted"].map((color) =>
  `<marker id="primer-${color}-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.4" markerHeight="3.4" orient="auto"><path d="M1 1L9 5L1 9Z" fill="var(--${color})"/></marker>`).join("")}</defs>`;

function circuit(compact, mode = "circuit", state = {}) {
  const left = compact ? 70 : 200, right = compact ? 252 : 820;
  const top = compact ? 180 : 155, bottom = compact ? 420 : 435, cy = (top + bottom) / 2;
  const r = compact ? 35 : 48, lw = compact ? 66 : 104, lh = compact ? 108 : 130;
  const numeric = mode !== "circuit", power = mode === "power", open = !numeric && state.circuit === "open";
  const middle = (left+right)/2, gap = compact ? 27 : 42;
  let out = path(`M${left} ${cy-r}V${top}H${middle-gap}M${middle+gap} ${top}H${right}V${cy-lh/2}`) +
    path(`M${right} ${cy+lh/2}V${bottom}H${left}V${cy+r}`);
  if (numeric) {
    if (mode === "voltage-current") {
      out += `<circle cx="${middle}" cy="${top}" r="${gap}" fill="var(--surface)" stroke="var(--power)" stroke-width="2"/>` + text(middle, top+7, "A", 21, "power");
    } else out += path(`M${middle-gap} ${top}H${middle+gap}`);
  } else {
    out += dot(middle-gap, top) + dot(middle+gap, top);
    out += path(`M${middle-gap} ${top}L${middle+gap-4} ${open ? top-32 : top}`, "power", 3);
  }
  out += `<circle cx="${left}" cy="${cy}" r="${r}" fill="var(--surface)" stroke="var(--power)" stroke-width="3"/>`;
  out += text(left, cy - 10, "+", 25, "power") + text(left, cy + 25, "−", 25, "power");
  out += rect(right-lw/2, cy-lh/2, lw, lh, "power");
  out += text(right, cy+7, power ? "24 W" : numeric ? "6 Ω" : "Load", compact ? 19 : 25);
  if (!open) {
    out += arrow(`M${right} ${top+12}V${cy-lh/2-9}`, "power", 3);
    out += arrow(`M${right-35} ${bottom}H${left+50}`);
  }
  out += text(left, bottom+48, numeric ? "12 V DC source" : "DC source", compact ? 17 : 23);
  if (mode === "circuit") {
    out += text(middle, top-55, open ? "No steady current" : "Conventional current", compact ? 20 : 25, "power");
    out += text(middle, bottom+100, open ? "Open path · I = 0 A" : "Source → load → return", compact ? 20 : 24);
    out += text(middle, bottom+134, open ? "Voltage can remain across the gap" : "Complete loop · ideal DC", compact ? 17 : 19, "muted");
  } else {
    out += text((left+right)/2, mode === "voltage-current" ? top-gap-20 : top-30, "2 A through this path", compact ? 18 : 24, "power");
    if (power) {
      out += text(compact ? 195 : 1010, compact ? 558 : 255, "1 W = 1 joule / second", compact ? 23 : 21);
      out += text(compact ? 195 : 1010, compact ? 602 : 306, "P = V × I", 26, "power");
      out += text(compact ? 195 : 1010, compact ? 644 : 350, "12 V × 2 A = 24 W", compact ? 22 : 21);
      out += text(compact ? 195 : 1010, compact ? 680 : 391, "Ideal, steady DC", 17, "muted");
    } else {
      const vx = compact ? 337 : 1030, vtop = cy-lh/2, vbottom = cy+lh/2;
      out += path(`M${right} ${vtop}H${vx}V${cy-27}M${vx} ${cy+27}V${vbottom}H${right}`, "data", 2, 'stroke-dasharray="5 6"');
      out += dot(right, vtop, "data") + dot(right, vbottom, "data");
      out += `<circle cx="${vx}" cy="${cy}" r="${compact ? 27 : 32}" fill="var(--surface)" stroke="var(--data)" stroke-width="2"/>`;
      out += text(vx, cy+5, "12 V", compact ? 17 : 21, "data");
      out += text(compact ? 195 : 850, compact ? 550 : 505, "Voltage V: between two points", compact ? 20 : 24, "data");
      out += text(compact ? 195 : 850, compact ? 592 : 543, "Current I: through a path", compact ? 20 : 24, "power");
      out += text(compact ? 195 : 850, compact ? 642 : 580, "V = volts   ·   A = amperes", compact ? 19 : 21, "muted");
    }
  }
  return out;
}

function resistance(compact, state) {
  const volts = Number(state.resistanceVoltage) === 24 ? 24 : 12, amps = volts/6, watts = amps*amps*6;
  const left = compact ? 65 : 200, right = compact ? 290 : 760, top = compact ? 145 : 125, bottom = compact ? 405 : 435;
  const cy = (top+bottom)/2;
  let out = text(compact ? 195 : 580, compact ? 52 : 49, "Fixed resistor: R = 6 Ω", 25);
  out += path(`M${left} ${cy-35}V${top}H${right}V${cy-55}M${right} ${cy+55}V${bottom}H${left}V${cy+35}`);
  out += `<circle cx="${left}" cy="${cy}" r="35" fill="var(--surface)" stroke="var(--power)" stroke-width="3"/>`;
  out += text(left, cy-8, "+", 24, "power") + text(left, cy+25, "−", 24, "power");
  out += text(left, bottom+43, `${volts} V DC`, compact ? 20 : 24, "power");
  out += arrow(`M${left+55} ${top}H${right-40}`) + text((left+right)/2, top-26, `${amps} A`, 25, "power");
  out += arrow(`M${right-35} ${bottom}H${left+55}`);
  out += rect(right-42, cy-55, 84, 110, "heat") + text(right, cy+8, "6 Ω", 24, "heat");
  out += Array.from({length: amps === 2 ? 1 : 4}, (_, i) => {
    const yy = cy+(i-(amps === 2 ? 0 : 1.5))*22;
    return compact ? arrow(`M${right-49} ${yy}H${right-120}`, "heat", 3) : arrow(`M${right+49} ${yy}H${right+140}`, "heat", 3);
  }).join("");
  if (compact) {
    out += text(195, 526, `I = ${volts} V ÷ 6 Ω = ${amps} A`, 24, "power");
    out += text(195, 582, `P = ${amps}² × 6 = ${watts} W`, 26, "heat");
    out += text(195, 627, "Resistor heating · I²R", 21, "heat");
    out += text(195, 676, "Ideal source and wires", 18, "muted");
  } else {
    out += text(964, 370, `${watts} W of heat`, 26, "heat");
    out += text(355, 522, `I = ${volts} V ÷ 6 Ω = ${amps} A`, 26, "power");
    out += text(840, 522, `P = ${amps}² × 6 = ${watts} W`, 26, "heat");
    out += text(580, 576, "Ideal source and wires · resistor heating is I²R", 21, "muted");
  }
  return `<g data-volts="${volts}" data-amps="${amps}" data-heat-watts="${watts}">${out}</g>`;
}

function energy(compact, state) {
  const hours = Number(state.hours) === 1 ? 1 : 2;
  const x = compact ? 38 : 180, w = compact ? 314 : 800, y = compact ? 166 : 170;
  let out = text(compact ? 195 : 580, compact ? 48 : 57, "Energy = power × time", 26);
  out += text(compact ? 195 : 580, compact ? 92 : 105, `Constant 1 kW load for ${hours} ${hours === 1 ? "hour" : "hours"}`, compact ? 20 : 24, "power");
  out += rect(x, y, w, compact ? 165 : 170, "line", "surface", 0);
  out += rect(x, y, w*hours/2, compact ? 165 : 170, "power", "panel", 0);
  out += path(`M${x+w/2} ${y}V${y+(compact ? 165 : 170)}`, "line", 2, 'stroke-dasharray="5 6"');
  out += text(x+w/4, y+94, "1 kWh", compact ? 24 : 26, "power");
  if (hours === 2) out += text(x+3*w/4, y+94, "1 kWh", compact ? 24 : 26, "power");
  [0, 1, 2].forEach((h) => { out += text(x+h*w/2, y+207, `${h} h`, compact ? 19 : 23, "muted"); });
  out += text(compact ? 195 : 580, compact ? 430 : 450, `1 kW × ${hours} h = ${hours} kWh`, 26, "power");
  if (compact) {
    out += text(195, 511, "kilo (k) = 1,000", 21) + text(195, 552, "mega (M) = 1,000,000", 21) + text(195, 593, "giga (G) = 1,000,000,000", 21);
    out += text(195, 655, "kW is power · kWh is energy", 20, "muted");
  } else {
    out += text(260, 534, "k = 1,000", 23) + text(580, 534, "M = 1,000,000", 23) + text(940, 534, "G = 1,000,000,000", 23);
  }
  return `<g data-hours="${hours}" data-energy-kwh="${hours}">${out}</g>`;
}

const wave = (x, mid, width, amplitude, phase = 0, cycles = 2) =>
  Array.from({length: 181}, (_, i) => `${i ? "L" : "M"}${(x+width*i/180).toFixed(2)} ${(mid-amplitude*Math.sin(i/180*Math.PI*2*cycles+phase)).toFixed(2)}`).join("");
function axes(x, mid, width, amplitude, compact) {
  return path(`M${x} ${mid-amplitude-16}V${mid+amplitude+16}`, "line", 2) +
    arrow(`M${x} ${mid}H${x+width+8}`, "muted", 2) +
    text(x-11, mid+6, "0", 17, "muted") +
    text(x+width, mid+amplitude+44, "time →", compact ? 17 : 19, "muted", "end");
}
function acdc(compact, state) {
  const angle = [90,180,270].includes(Number(state.angle)) ? Number(state.angle) : 90;
  const selectedSign = angle === 90 ? 1 : angle === 270 ? -1 : 0;
  let out = "";
  ["DC", "AC"].forEach((kind, i) => {
    const top = compact ? i*350 : 0, x = compact ? 55 : 110+i*550;
    const width = compact ? 280 : 400, cx = x+width/2;
    const mid = top+(compact ? 112 : 180), amp = compact ? 40 : 63;
    const sign = kind === "DC" ? 1 : selectedSign;
    out += text(cx, top+(compact ? 27 : 45), `${kind} voltage`, compact ? 24 : 29);
    out += text(cx, top+(compact ? 55 : 88), "Left terminal relative to right", compact ? 17 : 21, "muted");
    out += axes(x, mid, width, amp, compact);
    out += text(x-13, mid-amp+8, "+", 18, "muted") + text(x-13, mid+amp, "−", 18, "muted");
    out += kind === "DC"
      ? path(`M${x} ${mid-amp}H${x+width}`, "power", 4, 'data-dc-trace="constant"')
      : path(wave(x, mid, width, amp, 0, 1), "data", 4);
    if (kind === "AC") {
      const sampleX = x+width*angle/360, sampleY = mid-amp*Math.sin(angle*Math.PI/180);
      out += path(`M${sampleX} ${mid-amp-8}V${sampleY}`, "data", 2, 'stroke-dasharray="4 5"') + dot(sampleX, sampleY, "data");
    }
    const terminalY = top+(compact ? 264 : 414), left = x+10, right = x+width-10;
    const nameY = terminalY-(compact ? 45 : 50), signY = terminalY-(compact ? 11 : 15);
    out += text(left, nameY, "Left", compact ? 18 : 23) + text(right, nameY, "Right", compact ? 18 : 23);
    if (sign) out += text(left, signY, sign>0 ? "+" : "−", compact ? 25 : 29, "data") + text(right, signY, sign>0 ? "−" : "+", compact ? 25 : 29, "data");
    else out += text(cx, terminalY-41, "Same voltage", compact ? 18 : 23, "data");
    out += path(`M${left} ${terminalY}H${cx-61}M${cx+61} ${terminalY}H${right}`, "power", 3);
    out += dot(left, terminalY, "power") + dot(right, terminalY, "power");
    out += rect(cx-55, terminalY-25, 110, 50, "power") + text(cx, terminalY+7, "Resistor", compact ? 18 : 21);
    const arrowY = terminalY+(compact ? 45 : 67);
    if (sign) out += arrow(sign>0 ? `M${cx-48} ${arrowY}H${cx+48}` : `M${cx+48} ${arrowY}H${cx-48}`, "power", 4);
    out += text(cx, arrowY+(compact ? 28 : 41), sign>0 ? "Current flows right" : sign<0 ? "Current flows left" : "No current at this instant", compact ? 20 : 25, "power");
  });
  return `<g data-phase-angle="${angle}" data-ac-voltage-sign="${selectedSign}" data-ac-current-sign="${selectedSign}">${out}</g>`;
}

function acShapes(compact) {
  let out = "";
  const names = ["Sine", "Square", "Triangle (zigzag)", "Sawtooth"];
  names.forEach((name, i) => {
    const x = compact ? 53 : 125+(i%2)*555, width = compact ? 280 : 365;
    const mid = compact ? 130+i*135 : 183+Math.floor(i/2)*205, amp = compact ? 36 : 50;
    out += text(x+width/2, mid-amp-20, name, compact ? 21 : 24);
    out += path(`M${x} ${mid-amp-8}V${mid+amp+8}`, "line", 2) + arrow(`M${x} ${mid}H${x+width+8}`, "muted", 2);
    out += text(x-14, mid+6, "0", 16, "muted") + text(x-14, mid-amp+6, "+", 16, "muted") + text(x-14, mid+amp+6, "−", 16, "muted");
    let d = "";
    if (i === 0) d = wave(x, mid, width, amp, 0, 2);
    if (i === 1) d = `M${x} ${mid-amp}H${x+width/4}V${mid+amp}H${x+width/2}V${mid-amp}H${x+width*3/4}V${mid+amp}H${x+width}`;
    if (i === 2) d = `M${x} ${mid}L${x+width/8} ${mid-amp}L${x+width*3/8} ${mid+amp}L${x+width*5/8} ${mid-amp}L${x+width*7/8} ${mid+amp}L${x+width} ${mid}`;
    if (i === 3) d = `M${x} ${mid+amp}L${x+width/2} ${mid-amp}V${mid+amp}L${x+width} ${mid-amp}V${mid+amp}`;
    out += path(d, "data", 3);
    out += text(x+width, mid+amp+25, "time →", 16, "muted", "end");
  });
  if (compact) {
    out += text(195, 625, "Voltage between the same two points", 17, "muted");
    out += text(195, 668, "Utility AC is approximately sinusoidal.", 17, "muted");
  } else {
    out += text(580, 505, "Voltage between the same two points", 22, "muted");
    out += text(580, 551, "Utility AC is approximately sinusoidal.", 22, "muted");
  }
  return out;
}

function voltageVariation(compact, state) {
  const factor = ['0.9','1','1.1'].includes(String(state.supplyLevel)) ? Number(state.supplyLevel) : 1;
  const volts = Number((12*factor).toFixed(1));
  let out = '';
  ['DC','AC'].forEach((kind,i) => {
    const x = compact ? 55 : 125+i*550, width = compact ? 280 : 385;
    const top = compact ? i*330 : 0, mid = top+(compact ? 166 : 280), amp = compact ? 55 : 90;
    out += text(x+width/2, top+(compact ? 39 : 59), `${kind} voltage`, compact ? 25 : 29);
    out += text(x+width/2, top+(compact ? 78 : 109), kind==='DC' ? 'Nominal: 12 V DC' : 'Nominal: 12 V peak', compact ? 21 : 25, 'muted');
    out += axes(x, mid, width, amp*1.1, compact);
    const reference = kind==='DC' ? `M${x} ${mid-amp}H${x+width}` : wave(x,mid,width,amp,0,2);
    const actual = kind==='DC' ? `M${x} ${mid-amp*factor}H${x+width}` : wave(x,mid,width,amp*factor,0,2);
    out += path(reference,'muted',2,'stroke-dasharray="6 6"')+path(actual,kind==='DC'?'power':'data',4);
    out += text(x+width/2, top+(compact ? 294 : 481), kind==='DC' ? `${volts} V DC` : `${volts} V peak`, compact ? 27 : 32,kind==='DC'?'power':'data');
  });
  return `<g data-supply-factor="${factor}" data-dc-volts="${volts}" data-ac-peak-volts="${volts}">${out}</g>`;
}

function threePhase(compact) {
  const x = compact ? 46 : 120, width = compact ? 300 : 930;
  let out = "";
  const amps = compact ? 32 : 90;
  const phases = [0, -2*Math.PI/3, -4*Math.PI/3];
  if (compact) {

    ["A", "B", "C"].forEach((label, i) => {
      const mid = 155+i*140, color = ["power", "data", "heat"][i];
      out += text(x, mid-50, `Phase ${label}`, 20, color, "start");
      out += axes(x, mid, width, amps, true) + path(wave(x, mid, width, amps, phases[i], 1), color, 3);
    });
    out += text(195, 548, "120° apart · common voltage reference", 18, "muted");
    out += text(195, 635, "RMS: effective AC voltage", 21);
  } else {

    const mid = 279;
    out += axes(x, mid, width, amps, false);
    phases.forEach((phase, i) => {
      const color = ["power", "data", "heat"][i];
      out += path(wave(x, mid, width, amps, phase, 1), color, 4);
      out += path(`M${275+i*280} 112H${315+i*280}`, color, 4) + text(330+i*280, 119, `Phase ${["A", "B", "C"][i]}`, 23, color, "start");
    });
    out += text(580, 448, "120° apart · common voltage reference", 22, "muted");
    out += text(580, 525, "RMS: effective AC voltage", 24);
  }
  return out;
}

function threePhasePower(compact, state) {
  const degrees = [0,30,60].includes(Number(state.phasePowerAngle)) ? Number(state.phasePowerAngle) : 0;
  const phases = [0,-2*Math.PI/3,-4*Math.PI/3], colors = ['power','data','heat'];
  const powers = phases.map(phase => 20*Math.sin(degrees*Math.PI/180+phase)**2);
  const x = compact ? 57 : 120, width = compact ? 285 : 900, bottom = compact ? 375 : 382, scale = compact ? 7 : 7.4;
  let out = text(compact ? 195 : 580, 32, 'Balanced sine waves · equal resistive loads', compact ? 16 : 23, 'muted');
  out += text(x, compact ? 92 : 95, 'Instantaneous power (kW)', compact ? 18 : 24, 'text', 'start');
  [0,10,20,30].forEach(kw => {
    const y = bottom-kw*scale;
    out += path(`M${x} ${y}H${x+width}`,'line',1.5)+text(x-12,y+6,String(kw),compact ? 17 : 21,'muted','end');
  });
  out += arrow(`M${x} ${bottom}H${x+width+8}`,'muted',2)+text(x+width,bottom+30,'time →',compact ? 17 : 20,'muted','end');
  phases.forEach((phase,i) => {
    const d = Array.from({length:361},(_,j) => `${j?'L':'M'}${(x+width*j/360).toFixed(2)} ${(bottom-scale*20*Math.sin(j*Math.PI/180+phase)**2).toFixed(2)}`).join('');
    out += path(d,colors[i],3.5,`data-phase-power="${i}"`);
  });
  const totalY = bottom-30*scale, cursorX = x+width*degrees/360;
  out += path(`M${x} ${totalY}H${x+width}`,'text',4,'data-total-power-kw="30"');
  out += text(x+width,totalY-14,'Total: 30 kW',compact ? 20 : 26,'text','end');
  out += path(`M${cursorX} ${totalY-7}V${bottom}`,'muted',1.5,'stroke-dasharray="4 5"');
  powers.forEach((kw,i) => {
    out += dot(cursorX,bottom-kw*scale,colors[i]);
    out += text(compact ? 195 : 285+i*295,compact ? 461+i*44 : 472,`Phase ${['A','B','C'][i]}: ${Math.round(kw)} kW`,compact ? 23 : 26,colors[i]);
  });
  out += text(compact ? 195 : 580,compact ? 626 : 549,`${powers.map(Math.round).join(' + ')} = 30 kW`,compact ? 29 : 37);
  return `<g data-power-angle="${degrees}" data-phase-powers-kw="${powers.join(',')}" data-power-sum-kw="${powers.reduce((sum,p)=>sum+p,0)}">${out}</g>`;
}

function powerFactor(compact) {
  let out = text(compact ? 195 : 580, 28, "Same single-phase supply", compact ? 20 : 23, "muted");
  [1, .8].forEach((pf, i) => {
    const x = compact ? 57 : 110+i*540, width = compact ? 280 : 400;
    const cx = x+width/2, top = compact ? 55+i*325 : 55;
    const voltageMid = top+117, currentMid = top+(compact ? 245 : 345);
    const amplitude = compact ? 29 : 56, currentRatio = 1/pf, lag = Math.acos(pf);
    // The plots have separate voltage/current scales. Each scale is identical
    // between cases, so increasing the current amplitude represents higher RMS
    // current, never a change in the supply voltage. Equal V_rms I_rms cos(phi)
    // gives the same real power for these ideal sinusoidal loads.
    out += `<g data-power-factor="${pf}" data-real-kw="8" data-apparent-kva="${8/pf}" data-voltage-rms-relative="1" data-current-rms-relative="${currentRatio}" data-current-lag-radians="${lag}" data-phase-arrangement="single-phase">`;
    out += text(cx, top+28, i ? "Current lags · PF 0.8" : "In sync · PF 1", compact ? 23 : 29);
    [voltageMid, currentMid].forEach((mid) => {
      const extent = amplitude*1.25+6;
      [0, .25, .5, .75, 1].forEach((fraction) => {
        out += path(`M${x+width*fraction} ${mid-extent}V${mid+extent}`, "line", 1.5, 'stroke-dasharray="3 5"');
      });
      out += arrow(`M${x} ${mid}H${x+width+8}`, "muted", 1.5);
      out += text(x-13, mid+6, "0", 16, "muted");
    });
    out += text(cx, top+70, "Voltage", compact ? 21 : 24, "data");
    out += path(wave(x, voltageMid, width, amplitude, 0, 1), "data", compact ? 3.5 : 4);
    out += dot(x+width/4, voltageMid-amplitude, "data");
    out += text(x+width, top+(compact ? 174 : 207), "time →", 16, "muted", "end");
    out += text(cx, top+(compact ? 198 : 250), i ? "Current · 1.25× RMS (+25%)" : "Current · 1× RMS", compact ? 19 : 24, "power");
    out += path(wave(x, currentMid, width, amplitude*currentRatio, -lag, 1), "power", compact ? 3.5 : 4);
    out += dot(x+width*(.25+lag/(2*Math.PI)), currentMid-amplitude*currentRatio, "power");
    out += text(cx, top+(compact ? 306 : 480), "8 kW delivered", compact ? 23 : 29);
    out += "</g>";
  });
  return out;
}

function acSymbol(x, y, width, color = "power") {
  return path(wave(x, y, width, 10, 0, 1.5), color, 3);
}
function dcSymbol(x, y, width) {
  return path(`M${x} ${y-5}H${x+width}`, "power", 3) + path(`M${x} ${y+5}H${x+width}`, "power", 2, 'stroke-dasharray="5 5"');
}
function conversion(compact) {
  const rows = [
    ["Transformer", "AC", "AC", "Changes AC voltage"],
    ["Rectifier", "AC", "DC", "AC → DC"],
    ["Inverter", "DC", "AC", "DC → AC"],
    ["Power supply (PSU)", "AC", "DC", "Regulated DC for electronics"],
  ];
  let out = "";
  rows.forEach(([name, input, output, job], i) => {
    const y = compact ? 64+i*165 : 68+i*139;
    if (compact) {
      out += text(195, y, name, 23);
      out += rect(120, y+20, 150, 65, "power");
      if (i === 0) {
        out += path(`M153 ${y+33}c18 0 18 12 0 12c18 0 18 12 0 12c18 0 18 12 0 12M237 ${y+33}c-18 0 -18 12 0 12c-18 0 -18 12 0 12c-18 0 -18 12 0 12M192 ${y+29}v46M198 ${y+29}v46`, "power", 2);
      } else out += text(195, y+61, i === 3 ? "AC/DC example" : `${input} → ${output}`, 18, "power");
      out += text(54, y+34, input, 18) + text(336, y+34, output, 18);
      out += arrow(`M70 ${y+54}H112`, "power", 3) + arrow(`M278 ${y+54}H320`, "power", 3);
      out += text(195, y+119, job, 19, "muted");
    } else {
      out += text(70, y+37, name, 24, "text", "start");
      out += text(400, y+7, input, 20, "muted");
      out += (input === "AC" ? acSymbol(371, y+40, 58) : dcSymbol(371, y+40, 58));
      out += arrow(`M446 ${y+40}H491`, "power", 3);
      out += rect(505, y+7, 170, 65, "power");
      if (i === 0) out += path(`M547 ${y+22}c18 0 18 12 0 12c18 0 18 12 0 12c18 0 18 12 0 12M633 ${y+22}c-18 0 -18 12 0 12c-18 0 -18 12 0 12c-18 0 -18 12 0 12M587 ${y+17}v46M593 ${y+17}v46`, "power", 2);
      else out += text(590, y+49, i === 3 ? "AC/DC example" : `${input} → ${output}`, 21, "power");
      out += arrow(`M689 ${y+40}H734`, "power", 3);
      out += text(780, y+7, output, 20, "muted");
      out += (output === "AC" ? acSymbol(751, y+40, 58) : dcSymbol(751, y+40, 58));
      out += text(850, y+47, job, 21, "muted", "start");
    }
  });
  return out;
}

export function renderElectricity(id, state = {}, compact = false) {
  const renderers = {
    circuit: () => circuit(compact, "circuit", state),
    "voltage-current": () => circuit(compact, "voltage-current"),
    resistance: () => resistance(compact, state),
    power: () => circuit(compact, "power"),
    energy: () => energy(compact, state),
    "ac-dc": () => acdc(compact, state),
    "ac-shapes": () => acShapes(compact),
    "voltage-variation": () => voltageVariation(compact, state),
    "three-phase": () => threePhase(compact),
    "three-phase-power": () => threePhasePower(compact, state),
    "power-factor": () => powerFactor(compact),
    conversion: () => conversion(compact),
  };
  return renderers[id] ? `<g data-electricity-scene="${id}">${defs}${renderers[id]()}</g>` : "";
}
