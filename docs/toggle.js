function loadPlot() {
    var plotSelector = document.getElementById('plotSelector');
    var plotFrame = document.getElementById('plotFrame');

    var selectedPlot = plotSelector.value;
    plotFrame.src = selectedPlot;
}
