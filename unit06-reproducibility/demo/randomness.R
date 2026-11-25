# randomness.R: the same seed, two versions of R's sampling algorithm
set.seed(1213); print(sample(1:10, 3))          # R >= 3.6.0
suppressWarnings(RNGversion("3.5.0"))
set.seed(1213); print(sample(1:10, 3))          # what R 3.5 gave
