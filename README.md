# labfis.py

## Description

Small library (currently only one class) for uncertainty calculations and error propagation.

The uncertainty calculations are in accordance with gaussian’s propagation, as calculated by an analytical method:

$$\Delta_f = \sqrt{\left(\frac{\partial f}{\partial x}\right)^2{\Delta_x}^2 + \left(\frac{\partial f}{\partial y}\right)^2{\Delta_y}^2 + \left(\frac{\partial f}{\partial z}\right)^2{\Delta_z}^2 + ...}$$

Made by and for Physics Laboratory students in IFSC, who can't use uncertainties.py because of mean’s absolute deviation used in its calculation.

To get this library on google colaboratory:

```
!curl --remote-name \

-H 'Accept: application/vnd.github.v3.raw' \

--location https://raw.githubusercontent.com/phisgroup/labfis.py/development/labfis/main.py
```

## Usage

Just import with `from labfis import labfloat` and create an *labfloat* object as:

```
>>> from labfis import labfloat
>>> a = labfloat(1,3)
>>> b = labfloat(2,4)
>>> a*b
(2 ± 7)
```

## Instalation

Intstall master releases with:

```
pip install labfis
```

Install development releases with:

```
pip install git+https://github.com/phisgroup/labfis.py/tree/development
```

## References

 1. Kirchner, James. ["Data Analysis Toolkit #5: Uncertainty Analysis and Error Propagation"](http://seismo.berkeley.edu/~kirchner/eps_120/Toolkits/Toolkit_05.pdf)  (PDF). _Berkeley Seismology Laboratory_. University of California. Retrieved  22 April  2016.
 2. [Goodman, Leo](https://en.wikipedia.org/wiki/Leo_Goodman "Leo Goodman") (1960). "On the Exact Variance of Products". _Journal of the American Statistical Association_. **55** (292): 708–713. [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.2307/2281592](https://doi.org/10.2307%2F2281592). [JSTOR](https://en.wikipedia.org/wiki/JSTOR_(identifier) "JSTOR (identifier)")  [2281592](https://www.jstor.org/stable/2281592).
 3. Ochoa1,Benjamin; Belongie, Serge ["Covariance Propagation for Guided Matching"](http://vision.ucsd.edu/sites/default/files/ochoa06.pdf)
 4. Ku, H. H. (October 1966). ["Notes on the use of propagation of error formulas"](http://nistdigitalarchives.contentdm.oclc.org/cdm/compoundobject/collection/p16009coll6/id/99848/rec/1). _Journal of Research of the National Bureau of Standards_. **70C** (4): 262. [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.6028/jres.070c.025](https://doi.org/10.6028%2Fjres.070c.025). [ISSN](https://en.wikipedia.org/wiki/ISSN_(identifier) "ISSN (identifier)")  [0022-4316](https://www.worldcat.org/issn/0022-4316). Retrieved  3 October  2012.
 5. Clifford, A. A. (1973). _Multivariate error analysis: a handbook of error propagation and calculation in many-parameter systems_. John Wiley & Sons. [ISBN](https://en.wikipedia.org/wiki/ISBN_(identifier) "ISBN (identifier)")  [978-0470160558](https://en.wikipedia.org/wiki/Special:BookSources/978-0470160558 "Special:BookSources/978-0470160558").
 6. Lee, S. H.; Chen, W. (2009). "A comparative study of uncertainty propagation methods for black-box-type problems". _Structural and Multidisciplinary Optimization_. **37** (3): 239–253. [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.1007/s00158-008-0234-7](https://doi.org/10.1007%2Fs00158-008-0234-7).
 7. Johnson, Norman L.; Kotz, Samuel; Balakrishnan, Narayanaswamy (1994). _Continuous Univariate Distributions, Volume 1_. Wiley. p. 171. [ISBN](https://en.wikipedia.org/wiki/ISBN_(identifier) "ISBN (identifier)")  [0-471-58495-9](https://en.wikipedia.org/wiki/Special:BookSources/0-471-58495-9 "Special:BookSources/0-471-58495-9").
 8. Lecomte, Christophe (May 2013). "Exact statistics of systems with uncertainties: an analytical theory of rank-one stochastic dynamic systems". _Journal of Sound and Vibrations_. **332** (11): 2750–2776. [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.1016/j.jsv.2012.12.009](https://doi.org/10.1016%2Fj.jsv.2012.12.009).
 9. ["A Summary of Error Propagation"](http://ipl.physics.harvard.edu/wp-uploads/2013/03/PS3_Error_Propagation_sp13.pdf)  (PDF). p. 2. Retrieved  2016-04-04.
 10. ["Propagation of Uncertainty through Mathematical Operations"](http://web.mit.edu/fluids-modules/www/exper_techniques/2.Propagation_of_Uncertaint.pdf)  (PDF). p. 5. Retrieved  2016-04-04. 
 11. ["Strategies for Variance Estimation"](http://www.sagepub.com/upm-data/6427_Chapter_4__Lee_%28Analyzing%29_I_PDF_6.pdf)  (PDF). p. 37. Retrieved  2013-01-18.
 12. Harris, Daniel C. (2003), [_Quantitative chemical analysis_](https://books.google.com/books?id=csTsQr-v0d0C&pg=PA56)(6th ed.), Macmillan, p. 56, [ISBN](https://en.wikipedia.org/wiki/ISBN_(identifier) "ISBN (identifier)")  [978-0-7167-4464-1](https://en.wikipedia.org/wiki/Special:BookSources/978-0-7167-4464-1 "Special:BookSources/978-0-7167-4464-1")
 13. ["Error Propagation tutorial"](http://www.foothill.edu/psme/daley/tutorials_files/10.%20Error%20Propagation.pdf)  (PDF).  _Foothill College_. October 9, 2009. Retrieved  2012-03-01.