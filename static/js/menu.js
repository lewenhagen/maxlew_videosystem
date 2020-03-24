(function() {
    "use strict";

    document.addEventListener("keydown", function(event) {
        let key = event.key;
        console.log(event);
        switch(key) {
            case "1":
            case "2":
            case "3":
            case "4":
            case "5":
            case "6":
            case "7":
            case "8":
                window.location.replace(`/${key}`);
                break;
            case "9":
                window.location.replace(`/splashscreen`);
                break;
            case "0":
                window.location.replace("/0");
                break;

        }
    })

})();
