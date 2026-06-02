# Data Cleaning Decisions

## Missing MRP Values

The `MRP` column contained missing values that would prevent accurate revenue calculations. A hierarchical median imputation strategy was used:

1. Product Name median
2. Product Line median
3. Global dataset median

The median was chosen because it is less sensitive to extreme prices than the mean and better represents a typical selling price.

---

## Missing Discount Values

Missing discount values were interpreted as no discount being applied and replaced with `0`.

Discount values greater than `100%` were capped at `100%` to remove invalid records while preserving the transaction.

---

## Missing Units Sold

The `Units_Sold` column contained missing values. These were filled using the median quantity sold within the same `Product_Line`.

The median was selected because sales quantities may contain unusually large purchases that can distort the mean. Using the Product Line median preserves category-specific sales behavior while providing a realistic estimate for missing values.

Any remaining missing values were filled using the overall dataset median.

---

## Zero Unit Transactions

Transactions with `Units_Sold = 0` were removed from the final dataset.

These records do not represent valid sales or return transactions and would produce zero-value revenue records that add noise to downstream analysis.

---

## Missing Size Values

Missing size values were replaced using the mode (most frequently occurring size).

Since size is a categorical variable, the mode provides a more appropriate estimate than numerical measures such as the mean or median.

---

## Revenue Recalculation

The original `Revenue` column contained a large number of unrealistic values and inconsistencies.

Revenue was recalculated using the following business rule:

Revenue = MRP × Units_Sold × (1 − Discount_Applied)

This ensured consistency across all transactions and created a reliable metric for analysis.

---

## Missing Profit Values

The dataset did not contain cost information, preventing a reliable profit recalculation.

To preserve records for analysis, missing profit values were filled using the dataset median. The median was selected because it is more robust to unusually high or low profit values than the mean.

Profit values greater than revenue were flagged for review through the `Profit_Flag` column.

---

## Data Quality Validation

Before loading the cleaned data into PostgreSQL, validation checks were performed to ensure:

* All MRP values were positive
* All Units Sold values were greater than zero
* All discount values were between 0% and 100%

These checks help prevent invalid records from entering the analytical database.
