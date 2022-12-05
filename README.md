# TSX2StaMPS
This package serves for the preprocessing of high-resolution TerraSAR-X data for the ingestion in StaMPS, to process PSI time-series. It is an extension of the Snap2StaMPS package (https://github.com/mdelgadoblasco/snap2stamps) developed by José Manuel Delgado Blasco and Michael Foumelis in collaboration with Prof. A. Hooper, to automate the pre-processing of Sentinel-1 SLC data and their preparation for ingestion to StaMPS. Since both packages serve for the same, but with different SAR data, the functionality of Snap2StaMPS was partly overtaken to TSX2StaMPS. The package consists of 6 processing steps, which are listed below:

1. Unpack SAR scenes
2. Prepare SAR scenes for preprocessing
3. Subsetting
4. Coregistration
5. Interferogram generation
6. Stamps Export

For further information see the tutorial attached.
