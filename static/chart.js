// // Define Plotly chart layout
// const layout = {
//     title: 'Real-Time Stock Price',
//     xaxis: {
//         title: 'Time',
//         type: 'date'
//     },
//     yaxis: {
//         title: 'Price',
//         type: 'linear'
//     }
// };

// // Initialize the Plotly chart
// const chart = document.getElementById('realTimeChart');
// const initialData = [{
//     x: [],
//     y: [],
//     mode: 'lines',
//     line: {color: 'blue'}
// }];

// Plotly.newPlot(chart, initialData, layout);

// // Function to fetch stock price data and update the chart
// async function updateChart() {
//     const response = await fetch('https://query1.finance.yahoo.com/v8/finance/chart/AAPL?range=1d&interval=1m');
//     const data = await response.json();
//     const timestamp = new Date(data.chart.result[0].timestamp.map(ts => ts * 1000));
//     const prices = data.chart.result[0].indicators.quote[0].close;

//     // Update the chart data
//     Plotly.extendTraces(chart, { x: [timestamp], y: [prices] }, [0]);

//     // Adjust the chart time window (e.g., display last 30 data points)
//     if (timestamp.length > 30) {
//         Plotly.relayout(chart, { xaxis: { range: [timestamp[0], timestamp[29]] } });
//     }
// }

// // Call the updateChart function every minute (adjust interval as needed)
// setInterval(updateChart, 60000); // Update every minute (60000ms)
