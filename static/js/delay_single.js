(function() {
    "use strict";

    document.addEventListener("keydown", function(event) {
        let key = event.key;

        switch(key) {
            case "1":
            case "2":
            case "3":
            case "4":
                window.location.replace(`/selectbox/${key}`);
                break;
            case "0":
                window.location.replace("/0");
                break;
        }
    })
})();
