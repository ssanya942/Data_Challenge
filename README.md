# Total Path Length (TPL) Formula in Brain Networks

The **Total Path Length (TPL)** is a fundamental metric in brain network analysis, used to measure the sum of shortest paths between all pairs of nodes in a network. It is particularly relevant in the study of prefrontal cortex activation and functional connectivity.

The formula for TPL is given as:

\[
TPL = \sum_{i \neq j} L_{ij}
\]

where \( L_{ij} \) represents the shortest path length between nodes \( i \) and \( j \).

In weighted brain networks, the path length between two nodes is calculated as the sum of the inverse of the weights along the shortest path:

\[
L_{ij} = \sum_{\text{paths}} \frac{1}{\text{Weight}_{ij}}
\]

where:

- \( L_{ij} \) is the path length between nodes \( i \) and \( j \),
- \( \text{Weight}_{ij} \) is the connectivity weight (inverse of time delay) between nodes \( i \) and \( j \).

**Interpretation:**
- Lower **TPL** indicates more efficient connectivity and better synchronization between brain regions.
- Higher **TPL** suggests less efficient connectivity, potentially indicating increased cognitive load or impairment.

This formula is widely used in the analysis of brain connectivity, especially in functional brain mapping studies involving prefrontal cortex activation.

