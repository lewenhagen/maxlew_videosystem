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
                window.location.replace(`/${key}`);
                break;
            case "6":
                window.location.replace(`/all_quad`);
                break;
            case "7":
            case "8":
            case "9":
                window.location.replace(`/splashscreen`);
                break;
            case "+":
                window.location.replace("/0");
                break;

        }
    })

})();
