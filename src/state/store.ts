export interface Store<S extends object> {
  get(): S;
  set(patch: Partial<S> | ((s: S) => Partial<S>)): void;
  subscribe<T>(select: (s: S) => T, cb: (next: T, prev: T) => void, eq?: (a: T, b: T) => boolean): () => void;
}

export function setEq<T>(a: ReadonlySet<T>, b: ReadonlySet<T>): boolean {
  if (a === b) return true;
  if (a.size !== b.size) return false;
  for (const x of a) if (!b.has(x)) return false;
  return true;
}

export function shallowEq(a: unknown, b: unknown): boolean {
  if (Object.is(a, b)) return true;
  if (typeof a !== 'object' || typeof b !== 'object' || !a || !b) return false;
  const ka = Object.keys(a as object); const kb = Object.keys(b as object);
  if (ka.length !== kb.length) return false;
  for (const k of ka) if (!Object.is((a as Record<string, unknown>)[k], (b as Record<string, unknown>)[k])) return false;
  return true;
}

export function createStore<S extends object>(initial: S): Store<S> {
  let state = initial;
  const subs = new Set<(s: S) => void>();
  let notifying = false;
  let pending = false;
  return {
    get: () => state,
    set(patch) {
      const p = typeof patch === 'function' ? patch(state) : patch;
      let changed = false;
      for (const k in p) if (!Object.is((state as Record<string, unknown>)[k], (p as Record<string, unknown>)[k])) { changed = true; break; }
      if (!changed) return;
      state = { ...state, ...p };
      // A set made from inside a subscriber is folded into the running pass: the subscribers not yet visited
      // see the newer state, and the ones already visited get another pass afterwards, so nobody misses a
      // change because of where they sit in the subscription order. Each subscriber compares against what
      // it last saw, so the extra pass only calls the ones whose selection actually moved.
      if (notifying) { pending = true; return; }
      notifying = true;
      try {
        let passes = 0;
        do {
          pending = false;
          for (const fn of Array.from(subs)) fn(state);
          if (++passes > 50) { console.error('store: subscribers keep changing state in response to each other; giving up after 50 passes'); break; }
        } while (pending);
      } finally { notifying = false; pending = false; }
    },
    subscribe(select, cb, eq = Object.is) {
      let prev = select(state);
      const fn = (s: S) => { const next = select(s); if (!eq(next, prev)) { const p = prev; prev = next; cb(next, p); } };
      subs.add(fn);
      return () => { subs.delete(fn); };
    },
  };
}
