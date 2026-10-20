# Unit 4: The Linux command line

Run everything from this folder (`cd unit04-linux`).

| File | What it is |
|---|---|
| `data/mroz.csv` | Mroz (1987) data, the same file as Unit 3 |
| `data/waves/mroz_part*.csv` | `mroz.csv` split into four pieces, each with its own header row |
| `data/references.txt` | 15 well-known economics papers, one reference per line |
| `data/firms.csv` | A small **made-up** firm register with messy names and mixed date formats, for practising regular expressions |
| `code/stack_waves.sh` | Stacks the four pieces back into one file, `output/mroz_stacked.csv` |
| `code/run_all.sh` | Master script: stacks the data, checks the result, and makes a table |
| `code/loops.py` | The loop over regression specifications from Unit 3 |

To check everything works:

```bash
bash code/run_all.sh
```
