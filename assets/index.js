if(location.pathname === "/" || location.pathname === "")
    location.pathname = "/index";

window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.twitter_upd = {
    twitter_upd: function(a, b, c) {
        console.log("Twitter feed update");
        try {
            twttr.widgets.load();
        }
        catch (e) {

        }

        return "upd";
    }
}