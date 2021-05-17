const graph = function (dom_name, graph_type, heading, labels_data, dataset) {

    let color_genration = new Array();
    let dynamicColors = function () {
        var r = Math.floor(Math.random() * 255);
        var g = Math.floor(Math.random() * 255);
        var b = Math.floor(Math.random() * 255);
        return "rgb(" + r + "," + g + "," + b + ")";
    };

    for (let i = 0; i < labels_data.length; i++) {
        color_genration.push(dynamicColors())
    }

    new Chart(dom_name, {
        type: graph_type,
        data: {
            labels: labels_data,
            datasets: [{
                label: heading,
                data: dataset,
                backgroundColor: color_genration,
            }
            ]
        },
        options: {

            scales:
                {
                    y: {
                        beginAtZero: true,
                        ticks: {precision: 0,}
                    }
                }
        }
    });
}

const get_ctx = function (id){
    return document.getElementById(id).getContext('2d');
};