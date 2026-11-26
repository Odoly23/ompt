/**
 * v-reveal — fades an element in when it scrolls into view.
 *
 *   <section v-reveal>                  single element
 *   <ul v-reveal.stagger>               each child appears one after another
 *   <div v-reveal="{ from: 'left' }">   direction: up (default), left, right, scale
 *
 * Respects prefers-reduced-motion: elements are shown immediately.
 */
const reduced = () => typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

let observer = null
function getObserver() {
  if (observer || typeof IntersectionObserver === 'undefined') return observer
  observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue
      entry.target.classList.add('is-revealed')
      observer.unobserve(entry.target)
    }
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 })
  return observer
}

function prepare(el, from, delay) {
  el.dataset.reveal = from
  if (delay) el.style.transitionDelay = `${delay}ms`
  const io = getObserver()
  if (!io || reduced()) el.classList.add('is-revealed')
  else io.observe(el)
}

function apply(el, binding) {
  const from = binding.value?.from || 'up'
  if (binding.modifiers.stagger) {
    const step = binding.value?.step ?? 90
    Array.from(el.children).forEach((child, i) => {
      if (child.dataset.reveal) return
      prepare(child, from, Math.min(i, 8) * step)
    })
  } else if (!el.dataset.reveal) {
    prepare(el, from, binding.value?.delay || 0)
  }
}

export default {
  mounted: apply,
  // Lists rendered after data loads: pick up the new children.
  updated: (el, binding) => { if (binding.modifiers.stagger) apply(el, binding) },
  unmounted(el) {
    observer?.unobserve(el)
    Array.from(el.children).forEach((c) => observer?.unobserve(c))
  },
}
