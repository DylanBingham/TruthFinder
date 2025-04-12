function createAvgSentencePolarityChart(data, verticalLinePosition = 0) {
    const container = d3.select("#avg-sentence-polarity-chart .chart-svg-container");
    const containerWidth = container.node().getBoundingClientRect().width;
    const containerHeight = 300;
    
    // Clear only the chart area
    container.html("");

    // Config with proper dimensions accounting for margins
    const config = {
        width: containerWidth - 40, // Account for padding
        height: containerHeight - 40,
        margin: { top: 30, right: 20, bottom: 40, left: 40 }, // Reduced margins
        numBins: 30, // Reduced number of bins for smaller containers
        kdePoints: 500,
        verticalLine: {
            position: verticalLinePosition,
            color: "#FF5733",
            strokeWidth: 2,
            strokeDasharray: "5,5",
            hoverColor: "#FF0000"
        }
    };
    const filteredData = data.map(d => +d.avg_sentence_polarity).filter(d => !isNaN(d));
    filteredData.sort((a, b) => a - b);

    // Also, split the data into two groups based on the binary_label
    const dataLabel0 = data
        .filter(d => +d.binary_label === 0)
        .map(d => +d.avg_sentence_subjectivity)
        .filter(d => !isNaN(d));
    const dataLabel1 = data
        .filter(d => +d.binary_label === 1)
        .map(d => +d.avg_sentence_subjectivity)
        .filter(d => !isNaN(d));


    // Create SVG with dimensions that account for margins
    const svg = container.append("svg")
        .attr("width", config.width + config.margin.left + config.margin.right)
        .attr("height", config.height + config.margin.top + config.margin.bottom)
        .append("g")
        .attr("transform", `translate(${config.margin.left},${config.margin.top})`);
        
    // Create defs if they don't exist
    if (svg.select("defs").empty()) {
        const defs = svg.append("defs");
        
        // Drop shadow filter
        defs.append("filter")
            .attr("id", "drop-shadow")
            .attr("height", "120%")
            .attr("width", "120%")
            .append("feGaussianBlur")
            .attr("in", "SourceAlpha")
            .attr("stdDeviation", "1")
            .attr("result", "blur");
        
        // Clip path to prevent tooltip from being cut off
        defs.append("clipPath")
            .attr("id", "chart-area")
            .append("rect")
            .attr("width", config.width)
            .attr("height", config.height);
    }
    
    // Set up scales using config dimensions
    const x = d3.scaleLinear()
        .domain([-1, 1]) // Fixed domain for polarity (-1 to 1)
        .range([0, config.width]);
    
    // Create histogram generator
    const histogram = d3.histogram()
        .domain(x.domain())
        .thresholds(x.ticks(config.numBins))
        .value(d => d);
    
    const bins = histogram(filteredData);
    
    // Calculate maximum relative frequency from the histogram
    const maxHistogram = d3.max(bins, d => d.length / filteredData.length);

    // Create KDE line with explicit styling
    const kdeEstimator = kernelDensityEstimator(kernelEpanechnikov(0.5), x.ticks(config.kdePoints));
    // Compute KDE data for the two subsets
    const kdeData0 = kdeEstimator(dataLabel0);
    const kdeData1 = kdeEstimator(dataLabel1);

    // Calculate maximum KDE values for each subset
    const maxKDE0 = d3.max(kdeData0, d => d[1]);
    const maxKDE1 = d3.max(kdeData1, d => d[1]);
    
    // Unify the y-scale: use the larger of the histogram max and KDE max
    const yDomainMax = Math.max(maxHistogram, maxKDE0, maxKDE1);
    const y = d3.scaleLinear()
        .domain([0, yDomainMax])
        .range([config.height, 0]);
    
    // // Create bars with explicit styling
    // svg.selectAll("rect")
    //     .data(bins)
    //     .enter().append("rect")
    //     .attr("x", d => x(d.x0) + 1)
    //     .attr("y", d => y(d.length / filteredData.length))
    //     .attr("width", d => Math.max(0, x(d.x1) - x(d.x0) - 1))
    //     .attr("height", d => config.height - y(d.length / filteredData.length))
    //     .attr("fill", "steelblue")
    //     .attr("opacity", 0.7);
    
    const line = d3.line()
        .x(d => x(d[0]))
        .y(d => y(d[1]));
    
    // Plot KDE curve for binary_label === 0    
    svg.append("path")
        .datum(kdeData0)
        .attr("d", line)
        .attr("fill", "none")
        .attr("stroke", "#e15759") // Distinct red color
        .attr("stroke-width", 2);

    // Plot KDE curve for binary_label === 1
    svg.append("path")
        .datum(kdeData1)
        .attr("d", line)
        .attr("fill", "none")
        .attr("stroke", "#4daf4a") // Green (or your chosen color)
        .attr("stroke-width", 2);
    
    // Add vertical line at specified position
    if (config.verticalLine.position !== null && !isNaN(config.verticalLine.position)) {
        const calculatePercentile = (value) => {
            let countBelow = 0;
            for (let i = 0; i < filteredData.length; i++) {
                if (filteredData[i] <= value) countBelow++;
                else break;
            }
            return (countBelow / filteredData.length * 100).toFixed(1);
        };
        
        const percentile = calculatePercentile(config.verticalLine.position);
        
        const verticalLineGroup = svg.append("g")
            .attr("class", "vertical-line-group");

        // Vertical line
        const vLine = verticalLineGroup.append("line")
            .attr("x1", x(config.verticalLine.position))
            .attr("x2", x(config.verticalLine.position))
            .attr("y1", 0)
            .attr("y2", config.height)
            .attr("stroke", config.verticalLine.color)
            .attr("stroke-width", config.verticalLine.strokeWidth)
            .attr("stroke-dasharray", config.verticalLine.strokeDasharray);

        // Simplified tooltip
        vLine.on("mouseover", function(event) {
            const [_, mouseY] = d3.pointer(event, this);
            
            svg.append("text")
                .attr("class", "value-label")
                .attr("x", x(config.verticalLine.position) + 5)
                .attr("y", mouseY)
                .text(`${percentile}% < ${verticalLinePosition.toFixed(2)}`)
                .attr("font-size", "10px")
                .attr("fill", "black");
        })
        .on("mouseout", function() {
            svg.selectAll(".value-label").remove();
        });
    }
        
    // Simplified axes with fixed domain ticks
    svg.append("g")
        .attr("transform", `translate(0,${config.height})`)
        .call(d3.axisBottom(x).ticks(5).tickValues([-1, -0.5, 0, 0.5, 1]));
    
    svg.append("g")
        .call(d3.axisLeft(y).ticks(5));
    
    // Simplified labels - adjusted to account for margins
    svg.append("text")
        .attr("x", config.width / 2)
        .attr("y", config.height + config.margin.bottom - 10) // Adjusted for bottom margin
        .style("text-anchor", "middle")
        .style("font-size", "10px")
        .text("Polarity Score (-1 to 1)");
    
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("x", -config.height / 2)
        .attr("y", -config.margin.left + 15) // Adjusted for left margin
        .style("text-anchor", "middle")
        .style("font-size", "10px")
        .text("Density");
}

// Kernel Density Estimation functions (unchanged)
function kernelDensityEstimator(kernel, X) {
    return function(V) {
        return X.map(function(x) {
            return [
                x,
                d3.mean(V, function(v) { return kernel(x - v); })
            ];
        });
    };
}

function kernelEpanechnikov(k) {
    return function(v) {
        return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
    };
}