# ASOS Product Availability Analysis
*Exploring stockouts and potential lost revenue from ASOS products using Python.*

---

## Key Insights
- **High-price products have highest stockout exposure:** Several brands with average prices above **£40** also have **out-of-stock rates above 40%**, indicating potential unmet demand.
- **Stockouts are concentrated in a few brands:** Five brands are in the high-price/high-stockout quadrant.
- **Estimated lost revenue signals opportunity:** Proxy metric combining price and out-of-stock counts highlights potential revenue loss.
- **Improving availability in high-demand sizes may increase sales:** Focusing on popular sizes in premium products is likely the fastest revenue opportunity.

---

## Project Overview
This analysis investigates ASOS product availability and estimates potential revenue loss due to **out-of-stock sizes**. It includes:
1. Data cleaning and brand extraction
2. Stockout analysis at the product level
3. Aggregation at the brand level
4. Visualisation of high-risk, high-value brands
5. Exporting cleaned data for reuse in Power BI or other tools

---

## Visualisation

See attached file

- **X-axis:** Average product price (£)
- **Y-axis:** Out-of-stock rate
- **Bubble size:** Estimated lost revenue
- **Labels:** Brands with high price and high stockout rates

Red dashed lines indicate the threshold of **£40 price** and **40% out-of-stock rate** for high-priority brands.

---

## How to Run
1. Clone the repository:
```bash
git clone https://github.com/yourusername/asos-stockout-analysis.git
