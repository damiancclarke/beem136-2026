clear
set obs 1000
gen id = _n
gen firm = mod(_n, 10)
foreach s in 1 2 {
    sort id
    set sortseed `s'
    sort firm
    by firm: gen keep`s' = id[1]
}
count if keep1 != keep2
list firm keep1 keep2 if firm != firm[_n-1] in 1/1000, noobs clean
