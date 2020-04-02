(function() {
    "use strict";

    let selectedCams = [];
    let camSelection = document.createElement("div");
    let selected = document.getElementsByClassName("selected");

    camSelection.innerHTML = "<h3>Choose 2 cameras, then press Enter</h3>";
    document.getElementsByClassName("lists")[0].appendChild(camSelection);
    document.addEventListener("DOMContentLoaded", function(event) {
        document.documentElement.webkitRequestFullscreen();
    });
    document.addEventListener("keydown", function(event) {
        // event.preventDefault();
        let key = event.key;
        console.log(key);
        switch(key) {
            case "1":
            case "2":
            case "3":
            case "4":
                try {
                    if (selectedCams.length < 2) {
                        if (parseInt(key) !== document.getElementsByTagName("li").length) {
                            document.getElementsByTagName("li")[key-1].classList.toggle("selected");

                        }

                        if (selectedCams.indexOf(key) === -1) {
                            selectedCams.push(key);
                        } else {
                            selectedCams.splice(selectedCams.indexOf(key), 1);
                        }
                        if (selectedCams.length === 1) {
                            document.getElementsByTagName("li")[selectedCams[0]-1].classList.toggle("left");
                        } else if (selectedCams.length === 2) {
                            document.getElementsByTagName("li")[selectedCams[1]-1].classList.toggle("right");
                        }
                    } else {
                        document.getElementsByTagName("ul")[0].lastElementChild.classList.toggle("flash");
                    }

                } catch(e) {
                    console.log(e);
                }
                // window.location.replace(`/select-dual-cams/${key}`);
                break;
            case "Enter":
                if (selectedCams.length != 2) {
                    console.log("need 2 cameras");
                } else {
                    window.location.replace(`/select-dual-delay-left/${selectedCams[0]}/${selectedCams[1]}`);
                }
                break;
            case "+":
                window.location.replace("/0");
                break;

        }
    })
})();
