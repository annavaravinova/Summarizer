# Summarizer

Summarizer takes a pandas dataframe (and others arguments to customize the output), iterates through each of the columns 
in the dataframe, creates summary statistics for each,  prints them out to a table.
Output could be a markdown, html, or xlsx report of each column.

## Inputs
The function takes the following arguments:

dataframe: pandas dataframe. No Default. The passed dataframe requires dataframe name.
round_digits: Integer. Digits to which the numbers reported should be rounded. Default is 4.
feature_numbers: Boolean. Whether or not to add a column indicating the column number. Default is true.
missing_col: Boolean. Adds a column that reports proportion missing. Default in true.
output_type: String. The file format of the output file. xlsx, html,  markdown. Default is html.
output_file: String. The path and filename to which the script should output the results. Default is summary.html 
    in the local directory
append: Boolean. If there is an existing file, should we append the results or should we overwrite the file. 
    Default is true. When append is true, the results are appended. When it is false, the file is overwritten.

## Outputs
The output is a xlsx, html, or markdown file. 
For numeric columns it reports mean, standard deviation, minimum, maximum, median, variation,
Q1,Q2,Q3, IQR, Coefficient of Variation, Number of distinct values.
For object columns it reports the object values and their percentage.
Percentage that are non-missing, and Percentage missing, by default.

Definitions of Things in Output

NotNull = entries with non-missing values
mean (std) = mean (standard deviation).
min = minimum
med = median
max = maximum
var = variation
IQR = Interquartile range
Q1,2,3 = quantile 25,50,75
Coef of Var = Coefficient of variation

## Running the Script
Install the requirements:

pip install -r requirements.txt