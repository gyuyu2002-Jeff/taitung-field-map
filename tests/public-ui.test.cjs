const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const script = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(match => match[1]).join('\n');
const data = JSON.parse(html.match(/const TAITUNG_DB = (.*?);\s*\n/)[1]);

// Exercise the actual generated script with DOM/Leaflet doubles; no network or user data.
function setup() {
  const elements = new Map();
  const storage = new Map();
  const map = { on() {}, getZoom: () => 11, invalidateSize() {}, flyTo(position, zoom) { this.lastFlight = { position, zoom }; } };
  const layer = { markers: [], addTo() { return this; }, clearLayers() { this.markers = []; }, addLayer(marker) { this.markers.push(marker); } };
  const callbacks = {};
  let exported;
  function element() {
    return {
      value: '', textContent: '', style: {}, dataset: {}, children: [],
      classList: { toggle() {}, add() {}, remove() {} },
      set innerHTML(value) { this.html = value; this.children = []; },
      get innerHTML() { return this.html || ''; },
      appendChild(child) { this.children.push(child); }, removeChild() {},
      addEventListener() {}, setAttribute(key, value) { this[key] = value; },
      click() {}, scrollIntoView() {}
    };
  }
  const document = {
    getElementById(id) { if (!elements.has(id)) elements.set(id, element()); return elements.get(id); },
    querySelectorAll: () => [], querySelector: () => null,
    createElement: element, body: element()
  };
  const context = vm.createContext({
    document, window: { addEventListener(event, callback) { callbacks[event] = callback; } },
    localStorage: { getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value) },
    L: {
      map: () => map, tileLayer: () => ({ addTo() {} }), layerGroup: () => layer,
      divIcon: config => config,
      marker(position) { return { position, handlers: {}, on(event, fn) { this.handlers[event] = fn; }, bindTooltip(text) { this.tooltip = text; }, bindPopup(content) { this.popup = content; } }; }
    },
    Blob, URL: { createObjectURL(blob) { exported = blob; return 'blob:test'; } },
    console: { log() {}, warn() {}, error() {} }, setTimeout() {}
  });
  vm.runInContext(script, context);
  callbacks.DOMContentLoaded();
  return { context, document, elements, layer, map, storage, exported: () => exported };
}

test('startup renders 701 directory entries as 16 township markers', () => {
  const { document, layer } = setup();
  assert.equal(document.getElementById('filteredCount').textContent, 701);
  assert.equal(layer.markers.length, 16);
  assert.equal(document.getElementById('cardsContainer').children.length, 60);
  for (const marker of layer.markers) {
    assert.match(marker.popup.textContent, /並非單位所在地/);
    assert.equal(marker.position[0], Math.round(marker.position[0] * 100) / 100);
    assert.equal(marker.position[1], Math.round(marker.position[1] * 100) / 100);
  }
});

test('township, category and search filters work with the reduced schema', () => {
  const { context, layer } = setup();
  const first = data.units[0];
  vm.runInContext(`selectTownship(${JSON.stringify(first.township)})`, context);
  assert.equal(layer.markers.length, 1);
  vm.runInContext(`currentCategory=${JSON.stringify(first.category)}; currentSearch=${JSON.stringify(first.name.toLowerCase())}; filterAndRender()`, context);
  assert.equal(vm.runInContext('filterUnits().length', context), 1);
  assert.equal(vm.runInContext('filterUnits()[0].id', context), first.id);
});

test('focusing a unit uses the shared township location without unit coordinates', () => {
  const { context, map } = setup();
  vm.runInContext('focusUnit(TAITUNG_DB.units[0])', context);
  assert.deepEqual(Array.from(map.lastFlight.position), [data.township_coords[data.units[0].township].lat, data.township_coords[data.units[0].township].lng]);
  assert.equal(map.lastFlight.zoom, 11);
});

test('CSV export works without removed contact, address or street fields', async () => {
  const app = setup();
  app.document.getElementById('exportBtn').onclick();
  const csv = await app.exported().text();
  const lines = csv.trimEnd().split('\n');
  assert.equal(lines.length, 702);
  assert.doesNotMatch(lines[0], /會址|負責人|聯絡電話|主要路段/);
  assert.doesNotMatch(csv, /undefined/);
  assert.equal(lines[0].split(',').length, 10);
});

test('existing local notes survive and new units do not prefill a public contact', () => {
  const { context, document, storage } = setup();
  vm.runInContext('openVisitModal(TAITUNG_DB.units[0].id)', context);
  assert.equal(document.getElementById('visitContact').value, '');
  const id = data.units[0].id;
  vm.runInContext(`visitStore[${JSON.stringify(id)}]={contact:'LOCAL_ONLY',notes:'LOCAL_NOTE',history:[]}; openVisitModal(${JSON.stringify(id)})`, context);
  assert.equal(document.getElementById('visitContact').value, 'LOCAL_ONLY');
  context.saveVisitRecord();
  const saved = JSON.parse(storage.get('taitung_oa_field_logs_v1'));
  assert.equal(saved[id].contact, 'LOCAL_ONLY');
  assert.equal(saved[id].notes, 'LOCAL_NOTE');
});
