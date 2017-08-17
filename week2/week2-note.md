### Assume data is linear spearable, PLA always halts     

#### PLA Fact:

![PLA Fact 1](file:///Users/sam/Documents/pla_fact1.jpeg)

![PLA Fact 2](file:////Users/sam/Documents/pla_fact2.jpeg)

#### 因为:

$$ 1 \geq \frac {W_f^T} {||W_f^T||} \frac {W^T} {||W^T||} \geq \sqrt {T} \frac { \min \limits_n y_n \frac {W_f^T} {||W_f||} x_n} {\sqrt { \max\limits_n ||x_n||^2}} $$

#### 所以:

$$ T \leq \frac {(\min \limits_n y_n \frac {W_f^T} {||W_f||} x_n) ^ 2} {\max\limits_n ||x_n||^2} $$


### What if data is not linear spearable? Pocket Algriothm(hold somewhat best w in pocket)
