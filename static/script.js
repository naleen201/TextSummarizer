const loader = document.getElementById("loading");

function displayLoading() {
    loader.classList.add("display");
}

function hideLoading() {
    loader.classList.remove("display");
}

function updateSlider() {
    const sliderValue = document.getElementById("summary_size").value;
    document.getElementById("sliderLabel").innerHTML = `Summary Size: ${sliderValue}%`;
}
document.getElementById('inputfile')
    .addEventListener('change', function() {

        var fr = new FileReader();
        fr.onload = function() {
            document.getElementById('input_textarea')
                .value = fr.result;
        }

        fr.readAsText(this.files[0]);
    })


function getSummary() {
    var input_text = document.getElementById("input_textarea").value;
    var summary_size = document.getElementById("summary_size").value;
    displayLoading();
    fetch("summarize", {
        method: "POST",
        body: JSON.stringify({
            text: input_text,
            required_summary_length: summary_size
        }),
        headers: {
            "Content-type": "application/json"
        }
    })
        .then(response => response.json())
        .then((data) => {
            hideLoading();
            document.getElementById("output_textarea").value = data["summary"];
        })
}

function extractText() {
    var url = document.getElementById("inputurl").value;
    fetch('scrape-text?' + new URLSearchParams({
        URL: url
    }))
    .then(response => response.json())
    .then((data) => {
        if(data["scraped_text"] === "Invalid URL")
            alert("Please enter a valid URL.");
        else
            document.getElementById("input_textarea").value = data["scraped_text"];
    })
}


function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}



// Start file download.
document.getElementById("download_button").addEventListener("click", function() {
    // Generate download of hello.txt file with some content
    var text = document.getElementById("output_textarea").value;
    var filename = "Summary.txt";
    if (text.length != 0)
        download(filename, text);
}, false)