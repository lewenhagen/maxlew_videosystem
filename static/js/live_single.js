(function() {
    "use strict";
    document.addEventListener("DOMContentLoaded", function(event) {
        document.documentElement.webkitRequestFullscreen();
    });
    document.addEventListener("keydown", function(event) {
        let key = event.key;

        switch(key) {
            case "1":
            case "2":
            case "3":
            case "4":
                window.location.replace(`/selectcam/${key}`);
                break;
            case "0":
                window.location.replace("/0");
                break;
        }
    })
})();
