function createNumSpeechAttributesChart(data, verticalLinePosition) {
    // Configuration
    const container = d3.select("#num-speech-attributes-chart .chart-svg-container");
    const containerWidth = container.node().getBoundingClientRect().width;
    const containerHeight = 300;

    // Clear any existing content
    container.html("");
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

    // Filter and parse data
    const filteredData = data.map(d => +d.num_speech_attributes).filter(d => !isNaN(d));
    filteredData.sort((a, b) => a - b);
    // Create container div

    
    // Create SVG
    const svg = container.append("svg")
        .attr("width", config.width + config.margin.left + config.margin.right)
        .attr("height", config.height + config.margin.top + config.margin.bottom)
        .append("g")
        .attr("transform", `translate(${config.margin.left},${config.margin.top})`);
        
    if (svg.select("defs").empty()) {
        const defs = svg.append("defs");
        
        // Drop shadow filter
        defs.append("filter")
            .attr("id", "drop-shadow")
            .attr("height", "120%")
            .attr("width", "120%")
            .append("feGaussianBlur")
            .attr("in", "SourceAlpha")
            .attr("stdDeviation", "1")  // Reduced from 2 to 1
            .attr("result", "blur");
        
        // Clip path to prevent tooltip from being cut off
        defs.append("clipPath")
            .attr("id", "chart-area")
            .append("rect")
            .attr("width", config.width)
            .attr("height", config.height);
    }    
    // Set up scales
    const x = d3.scaleLinear()
        .domain([d3.min(filteredData), d3.max(filteredData)])
        .range([0, config.width]);
    
    // Create histogram generator
    const histogram = d3.histogram()
        .domain(x.domain())
        .thresholds(x.ticks(config.numBins))
        .value(d => d);
    
    const bins = histogram(filteredData);
    
    // Set up y scale for histogram
    const y = d3.scaleLinear()
        .domain([0, d3.max(bins, d => d.length / filteredData.length)])
        .range([config.height, 0]);
    
    // Create bars
    svg.selectAll("rect")
        .data(bins)
        .enter().append("rect")
        .attr("x", d => x(d.x0) + 1)
        .attr("y", d => y(d.length / filteredData.length))
        .attr("width", d => Math.max(0, x(d.x1) - x(d.x0) - 1))
        .attr("height", d => config.height - y(d.length / filteredData.length))
        .attr("fill", "#4e79a7") // Distinct blue color
        .attr("opacity", 0.7);
    // Create KDE line
    const kde = kernelDensityEstimator(kernelEpanechnikov(0.5), x.ticks(config.kdePoints));
    const kdeData = kde(filteredData);
    
    const line = d3.line()
        .x(d => x(d[0]))
        .y(d => y(d[1]));
    
    svg.append("path")
        .datum(kdeData)
        .attr("d", line)
        .attr("fill", "none")
        .attr("stroke", "#e15759") // Distinct red color
        .attr("stroke-width", 2);
    
    // Add vertical line at specified position
    if (config.verticalLine.position !== null && !isNaN(config.verticalLine.position)) {
        // Calculate percentile
        const calculatePercentile = (value) => {
            let countBelow = 0;
            for (let i = 0; i < filteredData.length; i++) {
                if (filteredData[i] <= value) countBelow++;
                else break;  // Data is sorted, so we can break early
            }
            return (countBelow / filteredData.length * 100).toFixed(1);
        };
        
        const percentile = calculatePercentile(config.verticalLine.position);
        
        // Create a group for the vertical line and its tooltip
       // Create a group for the vertical line and its tooltip
        const verticalLineGroup = svg.append("g")
            .attr("class", "vertical-line-group");

        // Add the vertical line
        const vLine = verticalLineGroup.append("line")
            .attr("class", "vertical-line")
            .attr("x1", x(config.verticalLine.position))
            .attr("x2", x(config.verticalLine.position))
            .attr("y1", 0)
            .attr("y2", config.height)
            .attr("stroke", config.verticalLine.color)
            .attr("stroke-width", config.verticalLine.strokeWidth)
            .attr("stroke-dasharray", config.verticalLine.strokeDasharray);

        // Create tooltip group (initially hidden)
        const tooltip = svg.append("g")
            .attr("class", "simple-tooltip")
            .style("opacity", 0);
        
        // Add white background rectangle
        tooltip.append("rect")
            .attr("rx", 4)  // Slightly rounded corners
            .attr("ry", 4)
            .attr("fill", "white")
            .attr("stroke", "#ccc")  // Light gray border
            .attr("stroke-width", 1);
        
        // Add text
        tooltip.append("text")
            .attr("text-anchor", "middle")
            .attr("dy", "0.35em")
            .style("font-size", "12px")
            .style("fill", "#333");  // Dark gray text
        
        // Update hover interactions
        vLine.on("mouseover", function(event) {
            const [_, mouseY] = d3.pointer(event, this);
            const lineX = x(config.verticalLine.position);
            
            // Update text
            tooltip.select("text")
                .text(`${percentile}% of values < ${verticalLinePosition}`);
            
            // Get text size
            const textSize = tooltip.select("text").node().getBBox();
            const padding = 8;
            
            // Position tooltip
            tooltip.attr("transform", `translate(${lineX},${mouseY - 30})`);
            
            // Size background to fit text
            tooltip.select("rect")
                .attr("x", -textSize.width / 2 - padding)
                .attr("y", -textSize.height / 2 - padding / 2)
                .attr("width", textSize.width + padding * 2)
                .attr("height", textSize.height + padding)
                .attr("fill", "white")  // Set background color
                .attr("stroke", "black") // Optional: Add a border
                .attr("opacity", 1);  // Ensure it's fully visible
            tooltip.raise()
            tooltip.style("opacity", 1);
        })
        .on("mouseout", () => tooltip.style("opacity", 0));
            
    }
    // Add x axis
    svg.append("g")
        .attr("transform", `translate(0,${config.height})`)
        .call(d3.axisBottom(x));
    
    // Add y axis
    svg.append("g")
        .call(d3.axisLeft(y));
    
    // Add x axis label
    svg.append("text")
        .attr("class", "axis-label")
        .attr("x", config.width / 2)
        .attr("y", config.height + config.margin.bottom - 10)
        .style("text-anchor", "middle")
        .text("Count of Speech Attributes");
    
    // Add y axis label
    svg.append("text")
        .attr("class", "axis-label")
        .attr("transform", "rotate(-90)")
        .attr("x", -config.height / 2)
        .attr("y", -config.margin.left + 15)
        .style("text-anchor", "middle")
        .text("Density");
    
    // Add title
    svg.append("text")
        .attr("class", "chart-title")
        .attr("x", config.width / 2)
        .attr("y", -config.margin.top / 2)
        .style("text-anchor", "middle")
        .text("Distribution of Number of Speech Attributes");
}

// Kernel functions same as above...