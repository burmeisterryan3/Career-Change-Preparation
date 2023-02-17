function compute()
{
    // Initialize value for computation of simple interest
    let principal = parseInt(document.getElementById("principal").value);
    let rate = parseFloat(document.getElementById("rate").value);
    let years = parseInt(document.getElementById("years").value);
    let future_year = new Date().getFullYear() + years;

    //Compute total
    let interest = principal * years * rate / 100;
    let amount = principal + interest;
    let result = document.getElementById("result");


    if (principal <= 0) {
        alert("Please enter a positive number!");
        document.getElementById("principal").focus();
    }
    else {
        result.innerHTML = `If you deposit \$<mark>${principal}</mark>,<br>\n`+
            `at an interest rate of <mark>${rate}</mark>\%.<br>`+
            `You will receive an amount of \$<mark>${amount}</mark>,<br>`+
            `in the year <mark>${future_year}</mark><br>`;
    }
}
function updateRate() {
    let rateval = document.getElementById("rate").value;
    document.getElementById("rate_val").innerText = rateval;
}
        