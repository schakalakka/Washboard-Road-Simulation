# Python Simulation of Washboards Formation on Unpaved Highways

Discrete washboard road simulation.

## Authors

* Spyridoula C. S., chrysikopoulou.spyridoula@gmail.com
* Cristian Estany B., cresbabellpuig@gmail.com
* Andreas Radke, radkeandreas@gmail.com
* Dani Salgado. R. daniel.salgado@e-campus.uab.cat

## Abstract

Several simulations and models have been purposed till the date, ranging from mathematical analysis to experimentation and simulation, everything with the purpose of gaining some insight about the washboard phenomenon, which has been classified as a complex dynamical system with some chaotic component.

In this project we propose a two dimensional, discrete mathematical model which is translated to an iterative algorithm that tries to reproduce the washboards dynamics observed in the experiments by several authors \cite{riley1971road, TheDynamicsofGranularRipplesFormedbyRollingWheels}. As an starting point, the basic discrete model purposed by David C. Mays and Boris A. Faybishenko in 2000, \cite{discretepaper}, is considered. The lack of realism of that basic model has motivated us to propose new improvements and models for the processes that seem to contribute to washboards formation. To model the road-surface interaction, we propose a probabilistic model for the so-called digging and piling process. To model environmental effects such as diffusion due to wind \cite{continuouspaper} and bump stability due to gravity \cite{modelpile,ontheshape,discretepilemodel}, a road smoothing strategy that model these kinds of phenomena is proposed.

The dependence of the road profile after some vehicle passes on the initial profile, and the dependence of model parameters on the road surface patterns obtained with our model are also studied and analysed. In addition, a methodology to estimate the wavelength of possible periodic or quasi-periodic regions in the obtained patterns of the road's surface is also proposed.

## Program guide

To be continued.

## References

* [1] J.G. Riley. The road corrugation phenomenon: a simulation and experimental evaluation.
Cornell Univ., 1971.
* [2] Nicolas Taberlet, Stephen W. Morris, and Jim N. McElwaine. Washboard road: The dynamics
of granular ripples formed by rolling wheels. Phys. Rev. Lett., 99:068003, Aug 2007.
* [3] David C. Mays and Boris A. Faybishenko. Washboards in unpaved highways as a complex
dynamic system. Complex., 5(6):51–60, July 2000.
* [4] Joseph A. Both, Daniel C. Hong, and Douglas A. Kurtze. Corrugation of roads. Physica A:
Statistical Mechanics and its Applications, 301(1):545 – 559, 2001.
* [5] Antal Károlyi and János Kertész. Lattice-gas model of avalanches in a granular pile. Phys.
Rev. E, 57:852–856, Jan 1998.
* [6] Herrmann H.J. On the shape of a sandpile. Physics of Dry Granular Media., 350, 1998.
* [7] Rafael J. Martínez-Durá Ignacio García-Fernández, Marta Pla-Castells. A discrete model for
the dynamics of sandpile surfaces. Proceedings of the Industrial Simulation Conference, pages
64–68, 2007.
* [8] Andreas Radke. Daniel Salgado R. Spyridoula C. S., Cristian Estany B. Washboarding simulation
in python. https://github.com/schakalakka/Washboard-Road-Simulation, 2018.
* [9] Douglas Kurtze, Daniel C. Hong, and Joseph A. Both. The genesis of washboard roads. 15:3344–
3346, 10 2001.
* [10] Anne-Florence Bitbol, Nicolas Taberlet, Stephen W. Morris, and Jim N. McElwaine. Scaling
and dynamics of washboard roads. Phys. Rev. E, 79:061308, Jun 2009.
* [11] Valeria Barra, Boris Boutkov, JiaMing Chen, Yuxin Chen, Michael DePersio, Ensela Mema,
Jimmy Moore, Juan Restrepo, Marisabel Rodriguez Rodriguez, Tural Sadigov, and TingWang.
A smooth ride on a bumpy road - graduate student mathematical modeling camp 2014 report,
06 2014.
* [12] K.B. Mather. The cause of road corrugations and the instability of surfaces under wheel action.
Civil Engineering and Public Works Review, 57, 1962.
* [13] Wikipedia contributors. Angle of repose — wikipedia, the free encyclopedia, 2018. [Online;
accessed 27-January-2018].
* [14] Wikipedia contributors. Autocorrelation — wikipedia, the free encyclopedia, 2018. [Online;
accessed 30-January-2018].
* [15] Juan Pablo Bello. Periodicity detection, Course: MPATE-GE 2623 Music Information Retrieval.
New York University.
* [16] R.B.L.; Carson R.M. Stoddart, J.; Smith. Transporting engineering journal. ASCE, page 376, 1982.

## License
