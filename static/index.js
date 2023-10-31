// function stockName() {
//     const scrollerID = document.querySelector("#scroller-in");
//     const h4Element = scrollerID.querySelector("h4")
//     const stock = h4Element.querySelector("a").textContent;
//     console.log(stock);
// }

var h4all = document.querySelectorAll("#nav h4")
h4all.forEach(function(elem){
    elem.addEventListener("mouseenter",function(){
        crsr.style.scale = 3    
        crsr.style.border = "1px solid #fff"
        crsr.style.backgroundColor = "transparent"
    })
    elem.addEventListener("mouseleave",function(){
        crsr.style.scale = 1    
        crsr.style.border = "0px solid #95C11E"
        crsr.style.backgroundColor = "#95C11E"
    })
})

gsap.to("#nav",{
    backgroundColor :"#021324",
    duration:0.5,
    height:"100px",
    scrollTrigger:{
        trigger:"#nav",
       scroller:"body",
       //markers:true,
       start:"top -10%",
       end:"top -11%",
       scrub:1
    }
    
})
gsap.to("#main",{
    backgroundColor :"#021324",
    scrollTrigger:{
        trigger:"#main",
       scroller:"body",
       //markers:true,
       start:"top -25%",
       end:"top -70%",
       scrub:2
}
})

gsap.from("#about-us img,#about-us-in",{
    y:50,
    opacity:0, 
    duration:1,
    scrollTrigger:{
        trigger:"#about-us",
        scroll:"body",
        //markers:true,
        start:"top 70%",
        end:"top 65%",
        scrub:1
    }
})

/*gsap.from(".card",{
    scale:0.8,
    opacity:0, 
    duration:1,
    scrollTrigger:{
        trigger:".card",
        scroll:"body",
        //markers:true,
        start:"top 70%",
        end:"top 65%",
        scrub:1
    }
})*/

gsap.from("#colon1",{
    y:-70,
    x:70,
    scrollTrigger:{
        trigger:"#colon1",
        scroller:"body",
       // markers:true,
        start:"top 55%",
        end:"top 45%",
        scrub:4
    }
})

gsap.from("#colon2",{
    y:70,
    x:70,
    scrollTrigger:{
        trigger:"#colon1",
        scroller:"body",
       // markers:true,
        start:"top 55%",
        end:"top 45%",
        scrub:4
    }
})

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