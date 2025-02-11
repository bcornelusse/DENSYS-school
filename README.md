# Densys school 2025

Optimization and machine learning applied to microgrid optimal control, optimal design, and forecasting.

Prerequisites: 
 - Notions of electrical circuits analysis
 - Notions of scientific computing (we will use Python)

Instructor: 
 - Bertrand Cornélusse

Teaching assistants:
 - Clément Moureau
 - Thomas Stegen


# Lectures 

| Day | Time | Topic |
| --- | --- | --- |
| February 13 | Remote | [Introduction and objectives](pdf/densys_1_1_intro.pdf) |
|        |  | [Introduction to optimization, a simple network flow problem](pdf/densys_1_2_LP_network_flow.pdf) |
|        |       | [LP example 1 notebook, Pyomo example](https://colab.research.google.com/drive/1xgO3EhGoG6P5E9BVV7QyPgLJM5HdNDrY?usp=sharing), [LP example 2 notebook](https://colab.research.google.com/drive/1ujoTNfu2_sCoVK7ksqbXgusmAAizvIip?usp=sharing) |
|        | | [Homework](https://colab.research.google.com/drive/1lrWL7sOrazTzlapVxcxrv_ZvVUZADC0h?usp=sharing) |
| March 12 |  | [Real-time optimization of a microgrid](pdf/densys_2_1_RTO.pdf) |
|         |  | [Hands on session](https://colab.research.google.com/drive/1kC0bY-wds_kCIuEd2WDQNj-F-j5024-p?usp=sharing) |
| March 26 | Remote  | TO BE MODIFIED  Lecture: [Introduction to machine learning](pdf/IntroductiontoMachineLearningDENSYS2021.pdf)  |
|          |     | TO BE MODIFIED Exercise: [Room occupancy prediction](https://colab.research.google.com/drive/1qhVUg9_W-4U3AcQXyP9ZW7TfmbUX91Mz?usp=sharing) and [data](notebooks/data.zip)|
|          |  | TO BE MODIFIED Lecture: [Introduction to point forecasting](https://github.com/jonathandumas/ELEN0445-1-microgrids-forecasting/blob/2b91cfc1b637b2ff17b13786b2407df66b6ac485/pdf/ELEN0445-1-microgrids-forecasting-lesson-1-2021.pdf) ([Video](https://youtu.be/NqezU_J1JQs))   |
|          |       | [Hand on forecasting session](https://colab.research.google.com/drive/1PZ6NR96HIhTFtHbq3Y6l6DlpnmL85zsD?usp=sharing), [Zip file if you want to run it on your machine](notebooks/forecasting_student_version.zip)|
| April 2 |   | TO BE MODIFIED [Operational planning in a (single-bus) microgrid with perfect forecasts and sizing](pdf/20230404_microgrids_optimization.pdf) |
|          |       | [Assignment](pdf/DENSYS_HW.pdf) and [code template](Operationnal%20planning/DENSYS_HW.zip) |



# References to dig the forecasting topic :)

Lectures of Professor Pierre Pinson. :
* [Renewables in Electricity Markets](http://pierrepinson.com/index.php/teaching/), in particular the modules 8, 9, and 10.
* [Statistical and Machine Learning for Forecasting](https://youtu.be/e7uMRluA01M) during the DTU CEE Summer School 2019 on "Data-Driven Analytics and Optimization for Energy Systems", 17-21 June 2019, Copenhagen, Denmark.

Note: Pierre Pinson is internationally recognized as a leading academic in forecasting, (stochastic) optimization and game theory for energy systems and markets, thanks to his multidisciplinary expertise in Operations Research and Management Science, Statistics, Economics, Meteorology and Energy/Electrical Engineering

The book:
```
@book{morales2013integrating,
  title={Integrating renewables in electricity markets: operational problems},
  author={Morales, Juan M and Conejo, Antonio J and Madsen, Henrik and Pinson, Pierre and Zugno, Marco},
  volume={205},
  year={2013},
  publisher={Springer Science \& Business Media}
}
```

The forecasting part of the thesis:
```
@thesis{dumas2021weather,
  title={Weather-based forecasting of energy generation, consumption and price for electrical microgrids management},
  author={Dumas, Jonathan},
  journal={arXiv preprint arXiv:2107.01034},
  year={2021}
}
```
