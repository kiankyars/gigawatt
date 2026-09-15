export const transformerOperatingEvidence = Object.freeze({
  model: 'Schneider Electric Phaseo ABL6TS25B',
  datasheet: 'https://iportal.se.com/Contents/docs/SQD-ABL6TS25B_DATASHEET.PDF',
  nominalInputV: 400,
  lowerInputV: 360,
  upperInputV: 440,
  alternateNominalInputV: 230,
  alternateLowerInputV: 207,
  alternateUpperInputV: 253,
  lowerFrequencyHz: 47,
  upperFrequencyHz: 63,
  ratingVA: 250,
  outputV: 24,
  image: '../assets/references/transformer-operating-abl6ts25b.png',
});

const styles = `<style>
  .transformer-operating-example{display:grid;grid-template-columns:minmax(180px,.8fr) minmax(0,1.6fr);gap:clamp(24px,4vw,64px);align-items:center;width:100%;color:var(--text)}
  .transformer-operating-example figure{margin:0;text-align:center}
  .transformer-operating-example img{display:block;width:min(100%,288px);height:auto;margin:auto;background:#fff;border-radius:12px}
  .transformer-operating-example figcaption{margin-top:12px;font-size:clamp(13px,1.1vw,17px);color:var(--muted)}
  .transformer-operating-example .toe-content{display:grid;gap:clamp(22px,3vw,36px)}
  .transformer-operating-example .toe-model{margin:0;font-size:clamp(19px,2.2vw,28px);font-weight:650}
  .transformer-operating-example .toe-rating{display:flex;flex-wrap:wrap;gap:8px 24px;margin-top:9px;font-size:clamp(16px,1.6vw,22px);color:var(--muted)}
  .transformer-operating-example .toe-check{font-size:clamp(17px,1.8vw,24px);margin:0 0 18px}
  .transformer-operating-example .toe-scale{display:grid;grid-template-columns:1fr 1fr 1fr;font-size:clamp(22px,3vw,40px);font-weight:650;gap:8px}
  .transformer-operating-example .toe-scale span:nth-child(2){text-align:center;color:var(--power)}
  .transformer-operating-example .toe-scale span:last-child{text-align:right}
  .transformer-operating-example .toe-band{height:20px;border:2px solid var(--power);border-radius:5px;margin:12px 0;position:relative;background:color-mix(in srgb,var(--power) 14%,transparent)}
  .transformer-operating-example .toe-band::after{content:'';position:absolute;left:50%;top:-8px;bottom:-8px;border-left:3px solid var(--power)}
  .transformer-operating-example .toe-labels{display:grid;grid-template-columns:1fr 1fr 1fr;font-size:clamp(14px,1.5vw,20px);color:var(--muted)}
  .transformer-operating-example .toe-labels span:nth-child(2){text-align:center}
  .transformer-operating-example .toe-labels span:last-child{text-align:right}
  .transformer-operating-example .toe-frequency{border-top:1px solid var(--line);padding-top:18px;display:flex;flex-wrap:wrap;gap:12px 24px;align-items:baseline;font-size:clamp(16px,1.6vw,22px)}
  .transformer-operating-example .toe-frequency strong{color:var(--power);font-size:clamp(22px,2.2vw,30px)}
  @media(max-width:700px){.transformer-operating-example{grid-template-columns:1fr;gap:20px}.transformer-operating-example figure{display:flex;gap:16px;align-items:center;justify-content:center}.transformer-operating-example img{width:115px;margin:0}.transformer-operating-example figcaption{margin:0;max-width:140px;text-align:left}.transformer-operating-example .toe-content{gap:22px}.transformer-operating-example .toe-scale{font-size:28px}.transformer-operating-example .toe-rating{gap:7px 16px}}
</style>`;

const e = transformerOperatingEvidence;

export const transformerOperatingExample = Object.freeze({
  title: 'This 400 V transformer permits a 360–440 V input',
  markup: `${styles}<div class="transformer-operating-example">
    <figure><img src="${e.image}" width="288" height="288" alt="Schneider Electric Phaseo ABL6TS25B controls transformer, from the manufacturer’s datasheet."><figcaption>Phaseo ABL6TS25B<br>Photo: Schneider Electric</figcaption></figure>
    <div class="toe-content">
      <div><p class="toe-model">250 VA controls transformer</p><div class="toe-rating"><span>24 V AC output rating</span></div></div>
      <div role="img" aria-label="The manufacturer specifies input voltage limits of 360 to 440 volts for the nominal 400 volt connection.">
        <p class="toe-check">Published input-voltage limits</p>
        <div class="toe-scale"><span>${e.lowerInputV} V</span><span>${e.nominalInputV} V</span><span>${e.upperInputV} V</span></div>
        <div class="toe-band" aria-hidden="true"></div>
        <div class="toe-labels"><span>−10%</span><span>Nominal</span><span>+10%</span></div>
      </div>
    </div>
  </div>`,
  description: 'Schneider Electric’s Phaseo ABL6TS25B is a 250 VA controls transformer with a nominal 400 V AC input and a 24 V AC output rating. Its manufacturer permits 360–440 V on the 400 V input connection. The input can vary within that range; a fixed-ratio transformer’s output also varies with its input. The 24 V output rating is not a promise of constant output across the input range.',
  reference: e.datasheet,
  sources: Object.freeze([e.datasheet]),
});
