# TopSeed
Topseed is a new technique that selects the most promising seeds for improving the symbolic execution with learning-based approach.

# How to execute our approach

For executing TopSeed, you can run experiment by following command in the '~/topseed' directory.
```python
$ python topseed.py program_configs/diffutils.json 3600 1 --eta_time=120
```
Each argument of the command indicates:
* program_configs/diffutils.json : description of the benchmark for testing the program
* 3600 : the total testing budget(sec)
* 1 : the prefix number of the experiment (the directory would be set as 'topseed/#1experiment')
* --eta_time=120 : the small time budget (hyperparameter $\eta_{time}$ in Algorithm 3)

If you want to conduct experiments of BASE (without our seeding approach), you can run the following commands.
```python
$ python base.py program_configs/diffutils.json 3600 1 --eta_time=120
```

After executing experiments, the results are stored in 'topseed/#{1}experiment/' with the name of '{benchmark}\_{1}\_result.coverage', '{benchmark}\_{1}\_result.err.log'.

Furthermore, if you want to assess the test cases generated during each iteration, you can access all generated data with following path:
* './topseed/#{1}experiment/iteration_\*/klee-out-0/\*.ktest' files


# Check the results of experiments
To check the branch coverage and bug from the results of experiments, you can easily analyze all results using following command:
```python
$ python analysis.py diff
# Set the iteration numbers of data : {index1} {index2} {index3}
                                                Coverage
The coverage results of #{index1}experiment:      824
The coverage results of #{index2}experiment:      876        
The coverage results of #{index3}experiment:      990
```