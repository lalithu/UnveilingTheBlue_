const navSlide = () => {
  const burger = document.querySelector(".burger");
  const nav = document.querySelector(".right-side");
  //Toggle Nav
  burger.addEventListener("click", () => {
    nav.classList.toggle("nav-active");

    //Burger Animation
    burger.classList.toggle("toggle");
  });
};

const app = () => {
  var dropdownSlide = () => {
    var dropdownburger = document.querySelector(".dropdownburger");
    var dropdown = document.querySelector(".dropdown-article");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle");
    });
  };
  dropdownSlide();

  
  var dropdownSlide1 = () => {
    var dropdownburger = document.querySelector(".dropdownburger1");
    var dropdown = document.querySelector(".dropdown-article1");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active1");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle1");
    });
  };
  dropdownSlide1();

  
  var dropdownSlide2 = () => {
    var dropdownburger = document.querySelector(".dropdownburger2");
    var dropdown = document.querySelector(".dropdown-article2");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active2");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle2");
    });
  };
  dropdownSlide2();

  
  var dropdownSlide3 = () => {
    var dropdownburger = document.querySelector(".dropdownburger3");
    var dropdown = document.querySelector(".dropdown-article3");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active3");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle3");
    });
  }; 
  dropdownSlide3();

  
  var dropdownSlide4 = () => {
    var dropdownburger = document.querySelector(".dropdownburger4");
    var dropdown = document.querySelector(".dropdown-article4");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active4");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle4");
    });
  }; 
  dropdownSlide4();

  
  var dropdownSlide5 = () => {
    var dropdownburger = document.querySelector(".dropdownburger5");
    var dropdown = document.querySelector(".dropdown-article5");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active5");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle5");
    });
  }; 
  dropdownSlide5();

  
  var dropdownSlide6 = () => {
    var dropdownburger = document.querySelector(".dropdownburger6");
    var dropdown = document.querySelector(".dropdown-article6");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active6");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle6");
    });
  }; 
  dropdownSlide6();

  
  var dropdownSlide7 = () => {
    var dropdownburger = document.querySelector(".dropdownburger7");
    var dropdown = document.querySelector(".dropdown-article7");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active7");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle7");
    });
  }; 
  dropdownSlide7();

  
  var dropdownSlide8 = () => {
    var dropdownburger = document.querySelector(".dropdownburger8");
    var dropdown = document.querySelector(".dropdown-article8");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active8");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle8");
    });
  }; 
  dropdownSlide8();

  
  
  var dropdownSlide9 = () => {
    var dropdownburger = document.querySelector(".dropdownburger9");
    var dropdown = document.querySelector(".dropdown-article9");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active9");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle9");
    });
  }; 
  dropdownSlide9();

  
  
  var dropdownSlide10 = () => {
    var dropdownburger = document.querySelector(".dropdownburger10");
    var dropdown = document.querySelector(".dropdown-article10");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active10");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle10");
    });
  }; 
  dropdownSlide10();

  
  var dropdownSlide11 = () => {
    var dropdownburger = document.querySelector(".dropdownburger11");
    var dropdown = document.querySelector(".dropdown-article11");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active11");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle11");
    });
  }; 
  dropdownSlide11();

  var dropdownSlide12 = () => {
    var dropdownburger = document.querySelector(".dropdownburger12");
    var dropdown = document.querySelector(".dropdown-article12");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active12");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle12");
    });
  }; 
  dropdownSlide12();

  
  var dropdownSlide13 = () => {
    var dropdownburger = document.querySelector(".dropdownburger13");
    var dropdown = document.querySelector(".dropdown-article13");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active13");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle13");
    });
  }; 
  dropdownSlide13();

  var dropdownSlide14 = () => {
    var dropdownburger = document.querySelector(".dropdownburger14");
    var dropdown = document.querySelector(".dropdown-article14");
    //Toggle Nav
    dropdownburger.addEventListener("click", () => {
      dropdown.classList.toggle("dropdownburger-active14");
  
      //Burger Animation
      dropdownburger.classList.toggle("dropdowntoggle14");
    });
  }; 
  dropdownSlide14();  
};

function cardScroll() {
  var card_id = document.getElementById("12");
  card_id.scrollIntoView({
    behavior: "smooth",
    block: "center",
    inline: "nearest"
  });
};

cardScroll();
navSlide();
app();