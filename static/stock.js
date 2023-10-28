document.addEventListener("DOMContentLoaded", function() {
    let current = document.querySelector("#current");
    const option1 = current;
    const option2 = document.querySelector("#mdays");
    const option3 = document.querySelector("#month");
    const option4 = document.querySelector("#year");
    const option5 = document.querySelector("#max");

    option1.addEventListener("click", function(event) {
        current.removeAttribute("id");
        option1.setAttribute("id", "current");
        current = option1;
    });

    option2.addEventListener("click", function(event) {
        current.removeAttribute("id");
        option2.setAttribute("id", "current");
        current = option2;
    });
    
    option3.addEventListener("click", function(event) {
        current.removeAttribute("id");
        option3.setAttribute("id", "current");
        current = option3;
    });
    
    option4.addEventListener("click", function(event) {
        current.removeAttribute("id");
        option4.setAttribute("id", "current");
        current = option4;
    });
    
    option5.addEventListener("click", function(event) {
        current.removeAttribute("id");
        option5.setAttribute("id", "current");
        current = option5;
    });
});

// const stockPrices = [100, 120, 140, 160, 180, 200, 220];
// const dates = ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06", "2022-01-07"];

// const ctx = document.getElementById("stock-graph").getContext("2d");

// new Chart(ctx, {
//     type: "line",
//     data: {
//         labels: dates,
//         datasets: [
//             {
//                 label: "Stock Price",
//                 data: stockPrices,
//                 borderColor: "blue",
//                 fill: false
//             }
//         ]
//     },
//     options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         scales: {
//             x: [
//                 {
//                     display: true,
//                     scaleLabel: {
//                         display: true,
//                         labelString: "Date"
//                     }
//                 }
//             ],
//             y: [
//                 {
//                     display: true,
//                     scaleLabel: {
//                         display: true,
//                         labelString: "Price"
//                     }
//                 }
//             ]
//         }
//     }
// })