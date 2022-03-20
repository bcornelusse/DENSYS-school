# Densys school 2022 - March 21 to 25

Optimization and machine learning applied to microgrid optimal control, optimal design, and forecasting.

Prerequisites: 
 - Notions of electrical circuits analysis
 - Notions of scientific computing (we will use Python)

Instructor: 
 - Bertrand Cornélusse

Teaching assistants:
 - Antonin Colot
 - Selmane Dakir
 - Jonathan Dumas
 - Thomas Stegen

# Lectures 

| Date | Topic |
| --- | --- |
| Monday | Lecture: [introduction to mathematical programming](pdf/intro_math_programming_v2.pdf), [LP example 1 notebook](https://colab.research.google.com/drive/1xgO3EhGoG6P5E9BVV7QyPgLJM5HdNDrY?usp=sharing), [LP example 2 notebook](https://colab.research.google.com/drive/1ujoTNfu2_sCoVK7ksqbXgusmAAizvIip?usp=sharing)  |
|               | MIP modeling exercises: [exercises pdf](pdf/MIP_exercises.pdf), [exercise 1 (solved) notebook](https://colab.research.google.com/drive/1dVQyXylIrwJvaD23hY2p1_xkplJfROqm?usp=sharing), [exercise 2 notebook](https://colab.research.google.com/drive/1UoUrG6N2I5RxA5g0IpXCH09gnsGybezG?usp=sharing) |
|               | Lecture: [introduction to optimal power flow (OPF) in DC grids](pdf/NLP_CVXP_DC_OPF.pdf) |
|               | Hands on session: [implement and compare several OPF formulations in a notebook](https://colab.research.google.com/drive/1Nr06HZMWQRHXIu0JGBnVHKV7-8j_cpDu?usp=sharing) |
| Tuesday | Lecture: [operationnal planning](pdf/operating_a_microgrid.pdf)  |
|               |Exercise : [description](https://github.com/bcornelusse/DENSYS-school/blob/main/Operationnal%20planning/OP_application_description.pdf), download the [simulator](https://github.com/bcornelusse/DENSYS-school/blob/main/Operationnal%20planning/microgrid-simulator.zip)|
| Wednesday | Lecture: [introduction to machine learning](pdf/IntroductiontoMachineLearningDENSYS2021.pdf)  |
|               | Exercise: [room occupancy prediction](https://colab.research.google.com/drive/1qhVUg9_W-4U3AcQXyP9ZW7TfmbUX91Mz?usp=sharing) and [data](notebooks/data.zip)|
| Thursday | Lecture: [introduction to point forecasting](https://github.com/jonathandumas/ELEN0445-1-microgrids-forecasting/blob/2b91cfc1b637b2ff17b13786b2407df66b6ac485/pdf/ELEN0445-1-microgrids-forecasting-lesson-1-2021.pdf) ([Video](https://youtu.be/NqezU_J1JQs))   |
|               | Assignment: [point forecasting of PV generation](https://github.com/jonathandumas/ELEN0445-1-microgrids-forecasting/blob/f6c4019274fd17f17e8c3329fffa8ed88917dcd8/pdf/ELEN0445-1-microgrids-forecasting-assignement-2021.pdf)) will be done in exercise session, download the [Python code](notebooks/assignment_files.tar.gz)|
|               | Lecture: [introduction to Probabilistic Forecasting](https://github.com/jonathandumas/ELEN0445-1-microgrids-forecasting/blob/27fcc893882f572d37a953b6a301e1a4f7671e83/pdf/ELEN0445-1-microgrids-forecasting-lesson-2-2021.pdf)  ([Video](https://youtu.be/jvHgJTsXDZg))   |
|               | Assignment: [probabilistic forecasting of PV generation](https://github.com/jonathandumas/ELEN0445-1-microgrids-forecasting/blob/f6c4019274fd17f17e8c3329fffa8ed88917dcd8/pdf/ELEN0445-1-microgrids-forecasting-assignement-2021.pdf) |
| Friday | Lecture: [sizing a microgrid](pdf/microgrids-sizing_a_microgrid.pdf) |
|               | Assignment: [description](pdf/20201210_sizing_assignment.pdf), [code template](notebooks/microgrid_sizing_opt.zip)|

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
