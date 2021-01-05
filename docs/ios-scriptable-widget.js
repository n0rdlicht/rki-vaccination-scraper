// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: gray; icon-glyph: syringe;

// Licence: Robert Koch-Institut (RKI), dl-de/by-2-0
// Vaccine API by @twesterhuys / https://github.com/n0rdlicht

// Set a state manually
const state = "Baden-Württemberg" // or "Germany", "Schleswig-Holstein", "Nordrhein-Westpfahlen", ...

// Vaccination API
const vaccineStatus = encodeURI("https://api.vaccination-tracker.app/v1/de-vaccinations-current?geo=" + state);

console.log(vaccineStatus)

// Initialize Widget
let widget = await createWidget();
if (!config.runsInWidget) {
  Safari.open("https://api.vaccination-tracker.app");
  await widget.presentSmall();
}

Script.setWidget(widget);
Script.complete();

// Build Widget
async function createWidget(items) {

  let title = state.toUpperCase();

  let list = new ListWidget();

  // Add background gradient
  let gradient = new LinearGradient();
  gradient.locations = [0,1];
  gradient.colors = [
    new Color("141414"),
    new Color("13233F")
  ];
  list.backgroundGradient = gradient;
  
  const number = await getVaccineData();

  let quote = number.quote.toLocaleString();

  let header, label;

  list.addSpacer(3);

  header = list.addText(state.toUpperCase());
  header.textColor = new Color("FFFFFF");
  if(state.length < 12){
    header.font = Font.boldSystemFont(14);
  } else {
    header.font = Font.boldSystemFont(9);
  }

  list.addSpacer(6);

  label = list.addText("+" + number.delta_vortag.toLocaleString() + "💉");
  label.font = Font.mediumSystemFont(24);
  label.textColor = new Color("FFFFFF");

  let dF = new DateFormatter();
  dF.useMediumDateStyle();
  dF.useNoTimeStyle();

  const since = list.addText("am " + dF.string(new Date(number.updated)));
  since.font = Font.mediumSystemFont(10);
  since.textColor = Color.gray();

  list.addSpacer(8);

  header = list.addText("Impfquote".toUpperCase());
  header.font = Font.mediumSystemFont(12);
  header.textColor = new Color("FFFFFF");
  
  label = list.addText(quote + "%");
  label.font = Font.mediumSystemFont(24);
  label.textColor = new Color("FFFFFF");

  if (number.quote < 30) {
    label.textColor = Color.red();
  } else if (number.quote >= 30 && number.quote < 67) {
    label.textColor = Color.orange();
  } else {
    label.textColor = Color.green();
  }

  list.addSpacer(5);

  let dF2 = new DateFormatter();
  dF2.useShortDateStyle();
  dF2.useShortTimeStyle();

  const updated = list.addText("Stand: " + dF2.string(new Date(number.published)));
  updated.font = Font.mediumSystemFont(10);
  updated.textColor = Color.gray();

  return list;

}

// Get vaccination rates
async function getVaccineData() {
  let data = await new Request(vaccineStatus).loadJSON();
  const attr = data.data[0];
  var values = {}
  values["updated"] = data.last_update
  values["published"] = data.last_published
  data.data.forEach(row => {
    if(row["key"] == "sum") {
      values["quote"] = row["quote"];
    }
    if(row["key"] == "sum" || row["key"] == "delta_vortag"){
      if(row["value"]) {
        values[row["key"]] = row["value"];
      }
      else {
        values[row["key"]] = "k.A.";
      }
    }
  });
  return values;
}