/**
 * One transport component for every presentation.
 *
 * A deck keeps ownership of its scene state and navigation handlers. This
 * component moves its existing buttons/select into a shared layout. The legacy
 * numbered-button renderer (800 V) is adapted to the same accessible selector.
 * New decks need #previous (or #back), #next, and a select or #steps in a footer.
 */
export function installSlideNavigation(doc = document) {
  const previous = doc.querySelector('#previous, #back');
  const next = doc.getElementById('next');
  const footer = previous?.closest('footer');
  if (!footer || !next || next.closest('footer') !== footer) return null;
  if (footer.dataset.slideNavigation === 'ready') return footer;

  const existingSelect = footer.querySelector('select');
  const sequence = footer.querySelector('#sequence');
  const steps = footer.querySelector('#steps');
  if (!existingSelect && !steps) return null;

  const choice = doc.createElement('div');
  choice.className = 'course-slide-choice';
  const counter = footer.querySelector('#progress') || doc.createElement('span');
  counter.classList.add('course-slide-progress');
  counter.setAttribute('aria-live', 'polite');
  counter.setAttribute('aria-atomic', 'true');

  let select = existingSelect;
  if (sequence) {
    // UPS replaces the contents of #sequence when it renders. Retain the host,
    // so its new selector and original handler remain part of this component.
    choice.append(sequence);
  } else if (select) {
    choice.append(select);
  } else {
    select = doc.createElement('select');
    select.id = 'course-slide-picker';
    choice.append(select);
    steps.hidden = true;
    steps.inert = true;
    steps.setAttribute('aria-hidden', 'true');
    choice.append(steps);
    select.addEventListener('change', () => {
      // Click the live button after any rerender; never duplicate deck state.
      steps.querySelectorAll('button[data-step]')[select.selectedIndex]?.click();
    });
  }

  previous.classList.add('course-slide-previous');
  next.classList.add('course-slide-next');
  previous.setAttribute('aria-label', 'Previous slide');
  next.setAttribute('aria-label', 'Next slide');
  previous.title = 'Previous slide';
  next.title = 'Next slide';
  footer.classList.add('course-slide-navigation');
  footer.setAttribute('aria-label', 'Slide navigation');
  footer.dataset.slideNavigation = 'ready';
  footer.replaceChildren(previous, choice, counter, next);

  const synchronize = () => {
    select = choice.querySelector('select');
    if (!select) return;
    if (steps) {
      const buttons = [...steps.querySelectorAll('button[data-step]')];
      const labels = buttons.map(button => button.getAttribute('aria-label') || button.textContent.trim());
      if (labels.length !== select.options.length || labels.some((label, i) => select.options[i]?.text !== label)) {
        select.replaceChildren(...labels.map((label, i) => {
          const option = doc.createElement('option');
          option.value = String(i);
          option.textContent = label;
          return option;
        }));
      }
      const current = buttons.findIndex(button => button.hasAttribute('aria-current'));
      if (current !== -1) select.selectedIndex = current;
    }
    if (select.getAttribute('aria-label') !== 'Choose slide') select.setAttribute('aria-label', 'Choose slide');
    const label = select.selectedOptions[0]?.text || '';
    if (select.title !== label) select.title = label;
    const position = `${select.selectedIndex + 1} / ${select.options.length}`;
    if (counter.textContent !== position) counter.textContent = position;
    // Some renderers write "End" or wrap these words in spans on each render.
    // Disabled state remains the deck's own boundary check; the controls stay
    // visually identical on first, middle, and final slides.
    if (previous.textContent !== '←') previous.textContent = '←';
    if (next.textContent !== '→') next.textContent = '→';
  };
  synchronize();
  new MutationObserver(synchronize).observe(footer, {
    childList: true, subtree: true, characterData: true,
    attributes: true, attributeFilter: ['aria-current', 'selected', 'disabled'],
  });
  // Setting a select's value does not create a DOM mutation. User changes and
  // hash navigation still synchronize immediately, even in a lightweight deck.
  choice.addEventListener('change', synchronize);
  doc.defaultView?.addEventListener('hashchange', synchronize);
  return footer;
}
