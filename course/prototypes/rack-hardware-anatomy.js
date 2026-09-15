const picture = (name, alt) => `<img src="../assets/references/${name}" alt="${alt}">`;

export function renderRackHardwareAnatomy() {
  return `<div class="rack-hardware-anatomy">
    <figure class="anatomy-rack">
      <figcaption><strong>Rack</strong><span>18 compute trays</span></figcaption>
      ${picture('lenovo-gb300-rack-front.jpg', 'Front view of a Lenovo GB300 NVL72 rack, with compute trays installed in its cabinet.')}
      <a class="anatomy-credit" href="https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai" target="_blank" rel="noopener">Lenovo · GB300 NVL72</a>
    </figure>
    <span class="anatomy-zoom" aria-label="Look inside the rack">→</span>
    <figure class="anatomy-tray">
      <figcaption><strong>Compute tray</strong><span>Two CPU/GPU boards</span></figcaption>
      ${picture('nvidia-gb300-tray.png', 'One NVIDIA DGX GB300 compute tray removed from a rack. It contains two Grace Blackwell Ultra superchips, with four GPUs and two CPUs in total.')}
      <a class="anatomy-credit" href="https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html" target="_blank" rel="noopener">NVIDIA · DGX GB300 tray</a>
    </figure>
    <span class="anatomy-zoom" aria-label="Look inside the compute tray">→</span>
    <figure class="anatomy-board">
      <figcaption><strong>CPU/GPU board</strong><span>One CPU + two GPUs</span></figcaption>
      ${picture('nvidia-gb300-superchip.webp', 'NVIDIA Grace Blackwell Ultra superchip board. The manufacturer labels a Grace CPU below two Blackwell Ultra GPUs; ConnectX-8 interfaces sit below the CPU.')}
      <a class="anatomy-credit" href="https://developer.nvidia.com/blog/inside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era/" target="_blank" rel="noopener">NVIDIA · Grace Blackwell Ultra</a>
    </figure>
  </div>`;
}
