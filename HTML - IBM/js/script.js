// Convert temperature in Celsius to Fahrenheit
// Temp(Fahrenheit) = [Temp(Degrees)*9/5] + 32
function convert_temperature() {
    // Get Celsius input and parse as number
    let temp_c = document.getElementById("celsius").value;
    // Convert from Celsius to Fahrenheit
    let temp_f = (temp_c*9/5) + 32;
    document.getElementById("fahrenheit").value = temp_f;
}

// Convert weight in kilograms to pounds
// Weight(Pounds) = Weight(Kgs) * 2.2
function convert_weight() {
    // Get kg input and parse as number
    let kg = document.getElementById("kilo").value;
    // Convert kg to lbs & round to 1 decimal place
    let lbs = (kg*2.205).toFixed(1);
    document.getElementById("pounds").value = lbs;
}

// Convert distance from km to miles
// Distance(Miles) = Distance(Kms) * 0.62137
function convert_distance() {
    // Get km input and parse as number
    let km = document.getElementById("km").value;
    // Convert km to miles & round to 2 decimal places
    let miles = (km*0.62137).toFixed(2);
    document.getElementById("miles").value = miles;
}