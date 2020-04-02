(function() {
    "use strict";

    document.addEventListener("keydown", function(event) {
        let key = event.key;

        switch(key) {
            case "1":
            case "2":
            case "3":
            case "4":
            case "5":
            case "6":
            case "7":
            case "8":
            case "9":
                if (parseInt(key) < document.getElementsByTagName("li").length) {
                    window.location.replace(`/selectbox/${key}`);
                }
                break;
            case "+":
                window.location.replace("/0");
                break;
        }
    })
})();
