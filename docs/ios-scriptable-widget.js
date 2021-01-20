// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: green; icon-glyph: magic;

// Licence: Robert Koch-Institut (RKI), dl-de/by-2-0
// Vaccine API by @twesterhuys / https://github.com/n0rdlicht
// Location detection by @mkreuz

const options = [
  "Germany",
  "Baden-Württemberg",
  "Bayern",
  "Berlin",
  "Brandenburg",
  "Bremen",
  "Hamburg",
  "Hessen",
  "Mecklenburg-Vorpommern",
  "Niedersachsen",
  "Nordrhein-Westfalen",
  "Rheinland-Pfalz",
  "Saarland",
  "Sachsen",
  "Sachsen-Anhalt",
  "Schleswig-Holstein",
  "Thüringen"
]

//Data storage
const cacheStorage = FileManager.local();
const cacheStoragePath = cacheStorage.cacheDirectory();
const pathCache = cacheStorage.joinPath(cacheStoragePath, "location.txt")

// const state = "Baden-Württemberg" // or "Germany", "Schleswig-Holstein", "Nordrhein-Westpfahlen", ...
const stateData = await getState();
const state = stateData[0];
const locationBased = stateData[1];
const validInput = stateData[2];

// Vaccination API
const vaccineStatus = encodeURI("https://api.vaccination-tracker.app/v1/de-vaccinations-current?geo=" + state);

// Initialize Widget
let widget = await createWidget();
if (!config.runsInWidget) {
//   Safari.open("https://api.vaccination-tracker.app");
  await widget.presentSmall();
}

Script.setWidget(widget);
Script.complete();

// Build Widget
async function createWidget(items) {
  
  let list = new ListWidget();
  
    // Add background gradient
    let gradient = new LinearGradient();
    gradient.locations = [0,1];
    gradient.colors = [
      new Color("141414"),
      new Color("13233F")
    ];
    list.backgroundGradient = gradient;
  
  if(validInput){

    let title = state.toUpperCase();
    
    const number = await getVaccineData();
  
    let quote = (Math.round(number.quote_initial*100)/100).toLocaleString();
  
    let header, label;
  
    list.addSpacer(3);
    
    let titleStack = list.addStack();
  
    header = titleStack.addText(state.toUpperCase());
    header.textColor = new Color("FFFFFF");
    if(state.length < 12){
      header.font = Font.boldSystemFont(14);
    } else {
      header.font = Font.boldSystemFont(10);
    }
   
    if(locationBased){
      let sym = titleStack.addImage(createSymbol("location").image);
      sym.resizable = false;
      sym.tintColor = Color.white();
      sym.imageSize = new Size(24,16);
    }
  
    list.addSpacer(6);
    
    let deltaVortag = "k.A.";
    if(number.delta_vortag_initial > 10000){
      value = Math.round(number.delta_vortag_initial / 100) / 10;
      deltaVortag = "+" + value.toLocaleString() + "k";
    }
    else if(number.delta_vortag_initial > 1000){
      value = Math.round(number.delta_vortag_initial / 10) / 100;
      deltaVortag = "+" + value.toLocaleString() + "k";
    }
    else {
       deltaVortag = "+" + number.delta_vortag_initial.toLocaleString();
    }
   
    label = list.addText(deltaVortag + "💉");
    label.font = Font.mediumSystemFont(24);
    label.textColor = new Color("FFFFFF");
  
    let dF = new DateFormatter();
    dF.useMediumDateStyle();
    dF.useNoTimeStyle();
  
    const since = list.addText("am " + dF.string(new Date(number.updated)));
    since.font = Font.mediumSystemFont(10);
    since.textColor = Color.gray();
  
    list.addSpacer(8);
  
    header = list.addText("Erstimpfquote".toUpperCase());
    header.font = Font.mediumSystemFont(12);
    header.textColor = new Color("FFFFFF");
    
    label = list.addText(quote + "%");
    label.font = Font.mediumSystemFont(24);
    label.textColor = new Color("FFFFFF");
  
    if (number.quote_initial < 30) {
      label.textColor = Color.red();
    } else if (number.quote_initial >= 30 && number.quote_initial < 67) {
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
  }
  else {
    label = list.addText("Ungültiger Parameter.");
    label.font = Font.boldSystemFont(16);
    label.textColor = new Color("FFFFFF");
    
    list.addSpacer(5);
    
    label = list.addText("Bundesland oder Germany");
    label.font = Font.mediumSystemFont(14);
    label.textColor = new Color("FFFFFF");
  }

  return list;

}

// Get vaccination rates
async function getVaccineData() {
  let data = await new Request(vaccineStatus).loadJSON();
  var values = {}
  values["updated"] = data.last_update
  values["published"] = data.last_published
  data.data.forEach(row => {
    if(['sum_initial','quote_initial','delta_vortag_initial'].includes(row["key"])){
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

async function getState(){
  
  let state = "Germany";
  let locationBased = false;
  let valid = true;
  
  if(args.widgetParameter && options.includes(args.widgetParameter)) {
    state = args.widgetParameter;
  }
  else if(args.widgetParameter){
    valid = false;
  }
  
  else {
    const location = await getLocation();
    
    if (location){
      const lat = location.latitude;
      const lng = location.longitude;
    
      const reverse = await Location.reverseGeocode(lat, lng, "de");
      const response = reverse[0];
    
      if (response.postalAddress.state && response.postalAddress.isoCountryCode === "DE") {
        state = response.postalAddress.state;
        cacheStorage.writeString(pathCache, state);
        locationBased = true;
      }
    }
    else if (cacheStorage.fileExists(pathCache)) {
      state = cacheStorage.readString(pathCache);
    }
  }
  return [state, locationBased, valid];
}

async function getLocation() {
  try {
    if (args.widgetParameter) {
      const fixedCoordinates = args.widgetParameter.split(",").map(parseFloat);
      return { latitude: fixedCoordinates[0], longitude: fixedCoordinates[1] };
    } else {
      Location.setAccuracyToThreeKilometers();
      return await Location.current();
    }
  } catch (e) {
    return null;
  }
}

function createSymbol(name) {
  let font = Font.systemFont(12);
  let sym = SFSymbol.named(name);
  sym.applyFont(font);
  return sym;
}