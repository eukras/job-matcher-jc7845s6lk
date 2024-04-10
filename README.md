# Job Matcher

* [NC 2024-04-10] [Nigel Chapman](mailto:nigel@chapman.id.au)

Match jobseekers to jobs by skills. 

## Results

* It performs the given matching challenge of 10 jobs and 10 job seekers in ~80ms, producing 49 matches.
* It matches jobs and job_seeker files of 10,000 lines each in ~15s, producing 4,000,000 matches. 
* Two matching strategies were implemented, though they were found to perform about the same.
* If we can discard matches under 50%, however, the preemptive matching strategy can cut this time to 8.6s. 

## Implementation Decisions

* Avoid the overhead of class instantiation, esp. for data rows.
* Favour using generators everywhere
* Allow multiple datasets in `datasets/`, switched with `--dataset`.
  * Generate random datasets to any size in `datasets/generated/` by running `generate.py`.
* Use a strategy pattern to compare different implementations:
  * Allow multiple job-matching strategies in `lib/matcher/`, switched with `--matcher`
  * Allow multiple output formats in `lib/writer/`, switched with `--writer`.

## Success Criteria

* Correctness: Does your program correctly match jobseekers to jobs based on their skills?
  * Results are provisionally correct; they can be tested with `python main.py | grep Alice` (or any other name or job title).
* Code quality: Is your code easy to understand and maintain?
  * The structure should be extremely developer-friendly; it has a general adherence to single-responsibility and dependency injection; plus there's a mid-level test suite.
* Extendibility: If we needed to add additional functionality, how difficult would this be?
  * The strategy pattern allows easy extension and comparison.
* Efficiency: How well does your program handle large inputs?
  * It's tested on 10,000 job and job_seekers as noted. 
* Tests: Is your code covered by automated tests?
  * Just run `python -m pytest test/` for results.
  * Or for code coverage: `coverage report -m` (currently 91%).

## Installation

```
$ virtualenv --python=3.11 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python -m pytest test 
===================================================== test session starts ======================================================
platform linux -- Python 3.11.6, pytest-8.1.1, pluggy-1.4.0
rootdir: /home/nigel/Code
configfile: pytest.ini
plugins: Faker-24.8.0
collected 6 items                                                                                                              

test/unit/lib/test_files.py .                                                                                            [ 16%]
test/unit/lib/test_matchers.py ....                                                                                      [ 83%]
test/unit/lib/test_skills.py .                                                                                           [100%]

====================================================== 6 passed in 0.03s =======================================================
```

## Commands

Two command line tools are provided:

* `main.py` performs matching and prints results.
* `generate.py` writes test files of a requested size to `dataset/generated/`.

Use `--help` to see options and defaults:

```
$ python main.py --help
Usage: main.py [OPTIONS]

  Match jobs to job seekers in a specified dataset, using a specified matching
  strategy, and tabulate the results.

Options:
  --dataset [challenge|generated]
                                  [default: (challenge)]
  --matcher [naive|preemptive]    [default: (naive)]
  --writer [csv|tabulate]         [default: (csv)]
  --help                          Show this message and exit.
```

```
$ python generate.py --help
Usage: generate.py [OPTIONS]

Options:
  --num_jobs INTEGER         [default: (1000)]
  --num_job_seekers INTEGER  [default: (1000)]
  --help                     Show this message and exit.
```

## Examples and timings

* The `challenge` data set has 10 jobs and 10 job seekers, each with up to 4 out of around 10 possible skills.
* The `generated` data set can be made to any size (we'll do 10,000 of each), with up to six of 100 possible skills. This is not included in the repository.

* The `naive` matching strategy tests every job against every job seeker: O(n^2). 
* The `preemptive` matching strategy uses a process of skills indexing as data is read through, and is potentially more efficient.

* The `csv` writer sends results to stdout.
* The `tabulate` writer produces pretty, human-readable tables. It's slow on big result sets.

* Timing is on a recent Dell XPS, Ubuntu 23, Python 3.11


### Naive matching on the challenge dataset (80ms)

For the most attractive output, use `--writer=tabulate`.

```
$ time python main.py --writer=tabulate

MATCHER : naive
WRITER  : tabulate
DATASET : datasets/challenge/jobs.csv
        : datasets/challenge/job_seekers.csv

  jobseeker_id  jobseeker_name       job_id  job_title                    matching_skill_count    matching_skill_percent
--------------  -----------------  --------  -------------------------  ----------------------  ------------------------
             7  George Prospect           8  Web Developer                                   4                       100
             1  Alice Seeker              1  Ruby Developer                                  3                       100
             4  Danielle Searcher         5  Machine Learning Engineer                       3                       100
             2  Bob Applicant             2  Frontend Developer                              3                        75
             7  George Prospect           2  Frontend Developer                              3                        75
             3  Charlie Jobhunter         3  Backend Developer                               3                        75
             4  Danielle Searcher         7  Data Analyst                                    3                        75
             6  Fiona Candidate           7  Data Analyst                                    3                        75
             2  Bob Applicant             8  Web Developer                                   3                        75
             9  Ian Jobhunter            10  JavaScript Developer                            3                        75
             3  Charlie Jobhunter         1  Ruby Developer                                  2                        67
             6  Fiona Candidate           5  Machine Learning Engineer                       2                        67
             5  Eddie Aspirant            6  Cloud Architect                                 2                        67
             7  George Prospect           4  Fullstack Developer                             3                        50
             9  Ian Jobhunter             2  Frontend Developer                              2                        50
             1  Alice Seeker              3  Backend Developer                               2                        50
             1  Alice Seeker              9  Python Developer                                2                        50
             3  Charlie Jobhunter         9  Python Developer                                2                        50
             6  Fiona Candidate           9  Python Developer                                2                        50
             8  Hannah Hunter             9  Python Developer                                2                        50
             1  Alice Seeker              4  Fullstack Developer                             2                        33
             2  Bob Applicant             4  Fullstack Developer                             2                        33
             6  Fiona Candidate           1  Ruby Developer                                  1                        33
             7  George Prospect           1  Ruby Developer                                  1                        33
             8  Hannah Hunter             1  Ruby Developer                                  1                        33
            10  Jane Applicant            1  Ruby Developer                                  1                        33
             8  Hannah Hunter             5  Machine Learning Engineer                       1                        33
             4  Danielle Searcher         6  Cloud Architect                                 1                        33
             6  Fiona Candidate           6  Cloud Architect                                 1                        33
             8  Hannah Hunter             6  Cloud Architect                                 1                        33
             6  Fiona Candidate           3  Backend Developer                               1                        25
             8  Hannah Hunter             3  Backend Developer                               1                        25
             1  Alice Seeker              7  Data Analyst                                    1                        25
             3  Charlie Jobhunter         7  Data Analyst                                    1                        25
             8  Hannah Hunter             7  Data Analyst                                    1                        25
             1  Alice Seeker              8  Web Developer                                   1                        25
             9  Ian Jobhunter             8  Web Developer                                   1                        25
            10  Jane Applicant            8  Web Developer                                   1                        25
             4  Danielle Searcher         9  Python Developer                                1                        25
             9  Ian Jobhunter             9  Python Developer                                1                        25
            10  Jane Applicant            9  Python Developer                                1                        25
             2  Bob Applicant            10  JavaScript Developer                            1                        25
             7  George Prospect          10  JavaScript Developer                            1                        25
            10  Jane Applicant           10  JavaScript Developer                            1                        25
             3  Charlie Jobhunter         4  Fullstack Developer                             1                        17
             5  Eddie Aspirant            4  Fullstack Developer                             1                        17
             6  Fiona Candidate           4  Fullstack Developer                             1                        17
             9  Ian Jobhunter             4  Fullstack Developer                             1                        17
            10  Jane Applicant            4  Fullstack Developer                             1                        17

(49 rows)

real	0m0.076s
user	0m0.056s
sys	0m0.020s
```

### Generating a large dataset (2m13s)

For testing performance we'll generate from large data with Faker...

```
$ time python generate.py --num_jobs=10000 --num_job_seekers=10000
Wrote 10000 jobs to datasets/generated/jobs.csv
Wrote 10000 job seekers to datasets/generated/job_seekers.csv

real	2m13.522s
```

If we look at these output files, we find:

```
$ head datasets/generated/jobs.csv
id,title,required_skills
1,"Accountant, chartered certified","['Skill 82', 'Skill 79']"
2,Paediatric nurse,"['Skill 78', 'Skill 39']"
3,Arts development officer,"['Skill 53', 'Skill 21', 'Skill 2', 'Skill 35', 'Skill 35', 'Skill 16']"
4,Chartered management accountant,"['Skill 14', 'Skill 68']"
5,Barista,"['Skill 85', 'Skill 53', 'Skill 93', 'Skill 88', 'Skill 56', 'Skill 30']"
6,Patent examiner,"['Skill 36', 'Skill 78', 'Skill 40', 'Skill 36', 'Skill 46']"
7,Production engineer,"['Skill 7', 'Skill 94']"
8,Food technologist,"['Skill 45', 'Skill 79', 'Skill 47', 'Skill 24']"
9,Waste management officer,"['Skill 88', 'Skill 33', 'Skill 21', 'Skill 47', 'Skill 81']"
```

```
$ head datasets/generated/job_seekers.csv
id,name,skills
1,Debra Ferguson,"['Skill 18', 'Skill 13', 'Skill 99', 'Skill 92']"
2,Amanda Brown,"['Skill 36', 'Skill 62']"
3,Kathleen Charles,"['Skill 76', 'Skill 30', 'Skill 65']"
4,Darren Wall,['Skill 59']
5,Jennifer Ward,"['Skill 72', 'Skill 4', 'Skill 74', 'Skill 12']"
6,Christian Torres,"['Skill 3', 'Skill 65', 'Skill 16']"
7,Calvin Barnett,"['Skill 9', 'Skill 95']"
8,Chad Gray,"['Skill 54', 'Skill 17', 'Skill 3', 'Skill 82', 'Skill 12', 'Skill 85']"
9,Christina Johnson,"['Skill 39', 'Skill 96', 'Skill 68', 'Skill 26']"
```

```
$ wc -l datasets/generated/*
  10001 datasets/generated/jobs.csv
  10001 datasets/generated/job_seekers.csv
  20002 total
```

## Naive matching on generated dataset (1m59s)

Running the same matching operation on the generated CSV Files:

```
$ time python main.py --dataset=generated --writer=tabulate

MATCHER : naive
WRITER  : tabulate
DATASET : datasets/generated/jobs.csv
        : datasets/generated/job_seekers.csv

  jobseeker_id  jobseeker_name               job_id  job_title                                                      matching_skill_count    matching_skill_percent
--------------  -------------------------  --------  -----------------------------------------------------------  ----------------------  ------------------------
          5825  Joseph Carr                    4791  Midwife                                                                           4                       100
          2406  Christopher Bennett             139  Games developer                                                                   3                       100
          7464  Matthew Smith                   791  Records manager                                                                   3                       100
          5865  Ann Murray                      834  Loss adjuster, chartered                                                          3                       100
          2767  Joseph Brown                    935  Purchasing manager                                                                3                       100
          8112  Paula Roberts                  1660  Astronomer                                                                        3                       100
          1810  Gloria White                   2156  Interpreter                                                                       3                       100
          6331  Nicole Ross                    2259  Glass blower/designer                                                             3                       100
... %< ...
          9884  Patricia Hart                  9989  Civil engineer, contracting                                                       1                        17
          9920  Samuel Maldonado               9989  Civil engineer, contracting                                                       1                        17
          9933  David Christensen              9989  Civil engineer, contracting                                                       1                        17
          9942  Chad Vance                     9989  Civil engineer, contracting                                                       1                        17
          9964  Maurice Little                 9989  Civil engineer, contracting                                                       1                        17
          9968  Ryan Green                     9989  Civil engineer, contracting                                                       1                        17
          9972  Rachel Dudley                  9989  Civil engineer, contracting                                                       1                        17
          9975  Mark Green                     9989  Civil engineer, contracting                                                       1                        17

(4087150 rows)

real	1m15.100s
user	1m11.482s
sys	0m3.596s
```

However, it's the tabulation that's using up most of this time. 

Running with the default CSV formatting, we get:

```
$ time python main.py --dataset=generated
jobseeker_id,jobseeker_name,job_id,job_title,matching_skill_count,matching_skill_percent
5825,Joseph Carr,4791,Midwife,4,100
2406,Christopher Bennett,139,Games developer,3,100
7464,Matthew Smith,791,Records manager,3,100
5865,Ann Murray,834,"Loss adjuster, chartered",3,100
2767,Joseph Brown,935,Purchasing manager,3,100
8112,Paula Roberts,1660,Astronomer,3,100
1810,Gloria White,2156,Interpreter,3,100
... %< ...
9920,Samuel Maldonado,9989,"Civil engineer, contracting",1,17
9933,David Christensen,9989,"Civil engineer, contracting",1,17
9942,Chad Vance,9989,"Civil engineer, contracting",1,17
9964,Maurice Little,9989,"Civil engineer, contracting",1,17
9968,Ryan Green,9989,"Civil engineer, contracting",1,17
9972,Rachel Dudley,9989,"Civil engineer, contracting",1,17
9975,Mark Green,9989,"Civil engineer, contracting",1,17

real	0m30.544s
user	0m17.965s
sys	0m4.221s
```

And finally, we can halve this again by piping the ouput to a file rather than echoing it to the terminal. 

```
time python main.py --dataset=generated > output.csv  # <-- Now 15s
```


## Implementing preemptive matching 

The naive implementation is not as slow as might be expected for brute-forcing 100,000,000 skillset comparisons. 

However, it is O(n^2), and we can probably improve that at the cost of keeping more data in memory.

In this approach, we read through jobs and jobseekers to create an index of unique skill sets for both jobs and job_seekers. We find the matching skillsets and generate the results from these, which are shorter.

Unfortunately, this performs just about identically on large and small datasets, and is not worth the added complexity:

```
time python main.py --matcher=preemptive                      # <-- Still about 80ms
time python main.py --matcher=preemptive --dataset=generated  # <-- Still about 30s
```

However, this approach could be much faster if we were to apply a threshold to the percentage matches we woudl accept. The great majority of matches are for only one skill, and for under a 60% match. If I change the preemptive strategy to ignore anything under 60%, which it will do more efficiently than the naive strategy, then we get to 8-9s.

Putting an LRU cache on the percentage calculations slows it down, however. 
