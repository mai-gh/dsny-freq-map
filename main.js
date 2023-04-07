const Attribution = ol.control.Attribution;
const View = ol.View;
const useGeographic = ol.proj.useGeographic;
const defaultControls = ol.control.defaults.defaults;
const TileLayer = ol.layer.Tile;
const OSM = ol.source.OSM;
const Map = ol.Map;
const GeoJSON = ol.format.GeoJSON;
//const Projection = ol.proj.Projection;

const VectorLayer = ol.layer.Vector;
const VectorSource = ol.source.Vector;
const Style = ol.style.Style;
const Stroke = ol.style.Stroke;
const Fill = ol.style.Fill;
const Text = ol.style.Text;

useGeographic();
const map = new Map({
  target: "map",
  view: new View({
    center: [-73.9449975, 40.645244],
    zoom: 11,
  }),
  layers: [
    new TileLayer({
      source: new OSM(),
    }),
    new VectorLayer({
      source: new VectorSource({
        url: "./data.json",
        format: new GeoJSON(),
      }),
      style: (feature) => {
        const labelStyle = new Style({
          text: new Text({
            font: '13px Calibri,sans-serif',
            stroke: new Stroke({
              color: '#fff',
              width: 8,
            }),
          }),
        });
        const zoneStyle = new Style({
          stroke: new Stroke({
            color: "green",
            width: 2,
          }),
          fill: new Fill({
            color: "rgba(0, 255, 0, 0.4)",
          }),
        });
        labelStyle.getText().setText([
        `Trash: ${feature.get('refuse')}`, '',
        '\n', '',
        `Bulk: ${feature.get('bulk')}`, '',
        '\n', '',
        `Recycling: ${feature.get('recycling')}`, '',
        ]);
        return [zoneStyle, labelStyle]
      },
    }),
  ],
});
