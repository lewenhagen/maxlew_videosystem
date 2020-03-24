(function() {
    "use strict";

    document.addEventListener("keydown", function(event) {
        let key = event.key;
        // console.log(event);
        switch(key) {
            case "1":
            case "2":
            case "3":
            case "4":
            case "5":
                window.location.replace(`/${key}`);
                break;
            case "6":
                console.log("yay");
                break;
            case "8":

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
