if(location.pathname === "/" || location.pathname=== "/index" || location.pathname === "")
    location.pathname = "/cases/overview";

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