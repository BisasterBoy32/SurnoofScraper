  
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
var pusher = new Pusher('fbbf751fdc9f604eb1f8', {
    cluster: 'eu'
});

function downloadResult(storageObj) {
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(storageObj));
    var dlAnchorElem = document.getElementById('downloadAnchorElem');
    dlAnchorElem.setAttribute("href",     dataStr     );
    dlAnchorElem.setAttribute("download", "result.json");
    dlAnchorElem.click();

}

var channel = pusher.subscribe('webScraper');
channel.bind('url-scraped', function(data) {
    received_data = JSON.parse(data.message)
    console.log(received_data)
    app.messages.push(received_data);
});

// var element = document.querySelector(".logs-section");
// element.scrollTop = element.scrollHeight;

channel.bind('scrape-finished', function(data) {
    received_data = JSON.parse(data.message)
    console.log(received_data)
    app.messages.push(received_data);
    if (received_data.type == "success") {
        downloadResult(received_data.data)
    }
});

var app = new Vue({
    el: ".main",
    delimiters: ["[[", "]]"],
    data: {
        inputs : 1,
        date : "lol",
        messages : []
    },
    methods : {
        onFormSubmit : function(e) {
            e.preventDefault();
            const form = this.$el.querySelector("#main-form");
            const formData = new FormData();
            formData.append("file", e.target.elements.file.files[0])
            formData.append("type", e.target.elements.type.value)
            formData.append("bill", e.target.elements.bill.value)
            const config = {
                headers: {
                    "content-type": "multipart/form-data"
                    }
            }

            axios.post("/process/", formData, config)
                .then(
                    res => {
                        console.log(res.data);
                        this.$el.querySelector(".form-section").style.display = "none";
                        this.$el.querySelector(".logs-section").style.display = "block";
                    } ,
                    err => console.log(err)
                )
        }
    }
})