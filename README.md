# Data Challenge Coursework-Added Insights

## Confidence Interval (CI) Formula

The **Confidence Interval (CI)** is a range of values that estimates an unknown population parameter with a certain level of confidence. It consists of a **lower bound** and an **upper bound**.

The general formula for the **CI** is given as:

$$CI = [\text{Lower Bound}, \text{Upper Bound}]$$

where:

- **Lower Bound** is calculated as:

$$\text{Lower Bound} = \bar{x} - z \times \frac{s}{\sqrt{n}}$$

- **Upper Bound** is calculated as:

$$\text{Upper Bound} = \bar{x} + z \times \frac{s}{\sqrt{n}}$$

### **Explanation of Terms**:
- \( \bar{x} \) = Sample Mean
- \( z \) = Z-score corresponding to the confidence level (e.g., 1.96 for 95% confidence)
- \( s \) = Standard deviation of the sample
- \( n \) = Sample size

### **Interpretation**:
A **95% Confidence Interval** means that if we were to take many samples and build a confidence interval from each sample, approximately **95% of the intervals** would contain the true population mean.

For example, if the sample mean is \( \bar{x} = 50 \), the standard deviation is \( s = 5 \), and the sample size is \( n = 100 \), with a 95% confidence level:

$$\text{Lower Bound} = 50 - 1.96 \times \frac{5}{\sqrt{100}} = 49.02$$

$$\text{Upper Bound} = 50 + 1.96 \times \frac{5}{\sqrt{100}} = 50.98$$

Thus, the **Confidence Interval** is:

$$CI = [49.02, 50.98]$$

---

### **How to Interpret**:
- **Narrower intervals** indicate **more precise estimates**. An interval with both positive or negative upper and lower bounds means significant differences.
- **Wider intervals** indicate **less precise estimates**, usually due to smaller sample sizes or higher variability.An interval with either a positive UB and negative LB or vice versa
 means less significant differences.

---


## Total Time Taken and Total Path Length 



The **Total Path Length (TPL)** is a fundamental metric in brain network analysis, used to measure the sum of shortest paths between all pairs of nodes in a network. It is particularly relevant in the study of prefrontal cortex activation and functional connectivity.

The formula for **TPL** is given as:

$$TPL = \sum_{i \neq j} L_{ij}$$

where \( L_{ij} \) represents the shortest path length between nodes \( i \) and \( j \).

In weighted brain networks, the path length between two nodes is calculated as the sum of the inverse of the weights along the shortest path:

$$L_{ij} = \sum_{\text{paths}} \frac{1}{\text{Weight}_{ij}}$$

where:

- \( L_{ij} \) is the path length between nodes \( i \) and \( j \),
- \( \text{Weight}_{ij} \) is the connectivity weight (inverse of time delay) between nodes \( i \) and \( j \).

### **Interpretation**:
- **Lower TPL** indicates more efficient connectivity and better synchronization between brain regions.
- **Higher TPL** suggests less efficient connectivity, potentially indicating increased cognitive load or impairment.

This formula is widely used in the analysis of brain connectivity, especially in functional brain mapping studies involving prefrontal cortex activation.
