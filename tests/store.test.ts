import { describe, expect, it } from 'vitest';
import { createStore } from '../src/state/store.ts';

describe('store', () => {
  it('a set made inside a subscriber reaches the subscribers already visited in that pass', () => {
    const store = createStore({ a: 0, b: 0 });
    const seenB: number[] = [];
    // subscribed first, so it has already run by the time the second subscriber changes b
    store.subscribe((s) => s.b, (b) => seenB.push(b));
    store.subscribe((s) => s.a, (a) => { if (a === 1) store.set({ b: 1 }); });
    store.set({ a: 1 });
    expect(store.get()).toEqual({ a: 1, b: 1 });
    expect(seenB).toEqual([1]);
  });
  it('the extra pass only calls subscribers whose selection moved, and nothing is called twice for one change', () => {
    const store = createStore({ a: 0, b: 0, c: 0 });
    let aCalls = 0; let cCalls = 0;
    store.subscribe((s) => s.a, () => aCalls++);
    store.subscribe((s) => s.c, () => cCalls++);
    store.subscribe((s) => s.a, (a) => { if (a === 1) store.set({ b: 1 }); });
    store.set({ a: 1 });
    expect(aCalls).toBe(1);
    expect(cCalls).toBe(0);
  });
  it('subscribers that keep changing state in response to each other cannot hang the page', () => {
    const store = createStore({ n: 0 });
    store.subscribe((s) => s.n, (n) => store.set({ n: n + 1 }));
    const err = console.error; const logged: string[] = [];
    console.error = (m: string) => logged.push(String(m));
    try { store.set({ n: 1 }); } finally { console.error = err; }
    expect(logged.some((m) => /giving up/.test(m))).toBe(true);
    expect(store.get().n).toBeGreaterThan(1);
    // and the store is usable afterwards
    store.set({ n: -1 });
    expect(store.get().n).toBeGreaterThanOrEqual(-1);
  });
  it('unchanged patches do not notify', () => {
    const store = createStore({ a: 1 });
    let calls = 0;
    store.subscribe((s) => s.a, () => calls++);
    store.set({ a: 1 });
    expect(calls).toBe(0);
  });
});
