let availableKeywords = [];
let companyNames = [];
let tickerNames = [];

fetch("../static/assets/data.json")
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    companyNames = data.company;
    tickerNames = data.ticker;
    availableKeywords = companyNames;
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
});

const resultBox = document.querySelector(".result-box");
const inputBox = document.querySelector(".input-box");

inputBox.onkeyup = function() {
    let result = [];
    let input = inputBox.value;
    if(input.length) {
        result = availableKeywords.filter((keyword)=>{
            return keyword.toLowerCase().includes(input.toLowerCase());
        });
        // console.log(result);
    }
    display(result);

    if(!result.length) {
        resultBox.innerHTML = "";
    }
}

function display(result) {
    const content = result.map((list)=>{
        return "<li onclick=selectInput(this)>" + list + "</li>";
    });
    resultBox.innerHTML = "<ul>" + content.join("") + "</ul>";
}

function selectInput(list) {
    inputBox.value = "";
    resultBox.innerHTML = "";
    const name = list.innerHTML;
    let ticker = "";
    console.log("Problem");
    for(let i = 0; i < companyNames.length; i ++) {
        if(name === companyNames[i]) {
            ticker = tickerNames[i];
            console.log(ticker);
            break;
        }
    }

    const stockURL = `/${ticker}`;
    window.open(stockURL, "_blank");
}