function charCount() {
    var element=document.getElementById('textarea').value.length;
    document.getElementById('textarea_count').innerHTML=element+"/10000 (Max Character 10000).";
}

function getSummary() {
    var input_text = document.getElementById("input_textarea").value;
    var summary_size = document.getElementById("summary_size").value;
    fetch('summarize?' + new URLSearchParams({
        text: input_text,
        required_summary_length: summary_size,
    }))
        .then(response => response.json())
        .then((data) => {
            document.getElementById("output_textarea").value = data["summary"];
        })
}