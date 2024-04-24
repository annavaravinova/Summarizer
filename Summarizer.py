import pandas as pd
import pytablewriter
from tabulate import tabulate
import os
from pytablewriter import ExcelXlsxTableWriter
import xlsxwriter
class SummaryDataFrame:
    def __init__(self):
        self.summary_cols = ['Number', 'Feature', 'Description', 'Percent of NotNull)', 'NotNull', 'Missing']

    def GetSummaryForColumn(self, number, col_name):
        col_set = self.df[col_name]
        col_summary = []

        # set Number of Feature
        if self.feature_numbers is True:
            col_summary.append(number)

        # get Feature name and type of column
        feature = ''
        feature += col_name
        if self.data_type[col_name] == 'float64':
            feature += '\n' + ('[%s]' % ('float'))
        elif self.data_type[col_name] == 'int64':
            feature += '\n' + ('[%s]' % ('integer'))
        elif self.data_type[col_name] == 'object':
            feature += '\n' + ('[%s]' % ('object(categorial)'))

        col_summary.append(feature)

        # get Description
        col_summary.append(self.GetDescription(col_name))

        # get distinct values
        if self.data_type[col_name] == 'object':
            col_summary.append(self.GetPercentForFeature(col_name))
        else:
            col_summary.append('%d unique val.' % (len(col_set.value_counts())))

        # get NotNull and Percent of NotNull
        notnull = 'NotNull: '
        missing_count = col_set.isnull().sum()
        notnull_count = self.row_count - missing_count
        notnull += str(notnull_count)
        if notnull_count == 0:
            notnull += '\n' + '(0%)'
        else:
            notnull += '\n' + ('(%0.' + str(self.round_digits) + 'f%%)') % (100 * (notnull_count / self.row_count))

        col_summary.append(notnull)

        # get Missing values
        if self.missing_col is True:
            missing = 'Missing: '
            missing += str(missing_count)
            if missing_count == 0:
                missing += '\n' + '(0%)'
            else:
                missing += '\n' + ('(%0.' + str(self.round_digits) + 'f%%)') % (100*(missing_count/self.row_count))

            col_summary.append(missing)

        return col_summary

        # set IQR
    def GetIQR(self, col_name):
        col_set = self.df[col_name]
        q1 = col_set.quantile(0.25)
        q3 = col_set.quantile(0.75)
        return q3 - q1


    def GetDescription(self, col_name):
        col_set = self.df[col_name]
        desc_values = ''

        if self.data_type[col_name] == 'float64':
            desc_values += '\n' + (('mean +-std: %0.' + str(self.round_digits) + 'f +-%0.' + str(self.round_digits) + 'f') % (col_set.mean(), col_set.std()))
            desc_values += '\n' + ('   min, max, median, var:')
            desc_values += '\n' + (('%0.' + str(self.round_digits) + 'f , %0.' + str(self.round_digits) + 'f , %0.' + str(self.round_digits) + 'f , %0.' + str(self.round_digits) + 'f') % (col_set.min(), col_set.max() , col_set.median(), col_set.var()))
            desc_values += '\n' + (('   Q1: %0.' + str(self.round_digits) + 'f, Q2: %0.' + str(self.round_digits) +'f, Q3: %0.' + str(self.round_digits) +'f') % (col_set.quantile(0.25), col_set.quantile(0.5), col_set.quantile(0.75)))
            desc_values += '\n' + (('   IQR , Coef of Var: %0.' + str(self.round_digits) + 'f ,%0.' + str(self.round_digits) + 'f') % (self.GetIQR(col_name), col_set.std()/col_set.mean()))
        elif self.data_type[col_name] == 'int64':
            desc_values += '\n' + (('mean +-std: %0.' + str(self.round_digits) + 'f +-%0.' + str(self.round_digits) + 'f') % (col_set.mean(), col_set.std()))
            desc_values += '\n' + ('   min, max, median:')
            desc_values += '\n' + ('%d , %d , %d' % (col_set.min(), col_set.max(), col_set.median()))
            desc_values += '\n' + (('   Q1: %0.' + str(self.round_digits) + 'f, Q2: %0.' + str(self.round_digits) +'f, Q3: %0.' + str(self.round_digits) +'f') % (col_set.quantile(0.25), col_set.quantile(0.5), col_set.quantile(0.75)))
            desc_values += '\n' + (('   IQR , Coef of Var: %d ,%0.' + str(self.round_digits) + 'f ,%0.' + str(self.round_digits) + 'f') % (self.GetIQR(col_name), col_set.std() / col_set.mean()))
        elif self.data_type[col_name] == 'object':
            col_count_list = list(self.df.groupby(col_name)[col_name].count().items())
            idx = 1
            for group_name, count in col_count_list:
                desc_values += '\n' + ('%d. %s' % (idx, group_name))
                idx += 1

        return desc_values

    def GetPercentForFeature(self, col_name):
        desc_values = ''
        col_count_list = list(self.df.groupby(col_name)[col_name].count().items())
        idx = 1
        for group_name, count in col_count_list:
            desc_values += (('  %d. %d(%0.' + str(self.round_digits) + 'f%%)') % (idx , count, 100 * (count / self.row_count)))
            idx += 1

        return desc_values

        #to create a xlsx file
    def WriteToExcelFile(self):
        writer = pytablewriter.ExcelXlsxTableWriter()
        writer.open(self.output_file)

        writer.make_worksheet(self.df.name)
        writer.header_list = self.summary_cols
        writer.value_matrix = self.df_summary
        writer.write_table()

        writer.close()


        # to create markdown-output
    def OutputMarkdown(self):
        writer = pytablewriter.MarkdownTableWriter()

        writer.table_name = self.df.name
        writer.header_list = self.summary_cols
        writer.value_matrix = self.df_summary

        writer.write_table()

        # to create a markdown file
    def WriteMarkdownFile(self):
        if self.append is True:
            f = open(self.output_file, 'a')
        else:
            f = open(self.output_file, 'w')
        f.write('\n')
        f.write('Data Frame Summary')
        f.write('\n')
        f.write(self.df.name)
        f.write('\n')
        f.write('N: ' + str(self.row_count))
        f.write('\n')
        f.write((tabulate(self.df_summary, tablefmt='simple', headers=self.summary_cols)))
        f.write('\n')
        f.close()

        #to create a html file
    def WriteHtmlFile(self):
        temp_file_name = str(self.output_file).split('.')[0] + '.md'
        if self.append is True:
            f = open(temp_file_name, 'a')
        else:
            f = open(temp_file_name, 'w')
        f.write('\n')
        f.write('<center>Data Frame Summary</center>')
        f.write('\n')
        f.write('<center>' + self.df.name + '</center>')
        f.write('\n')
        f.write('<center>' + 'N: ' + str(self.row_count) + '</center>')
        f.write('\n')
        f.write((tabulate(self.df_summary, tablefmt='simple', headers=self.summary_cols)))
        f.write('\n')
        f.close()

        os.system('pandoc -s -c custom.css -o ' + self.output_file + ' ' + temp_file_name)
        # os.unlink(temp_file_name)


        #method to summarize dataframe
    def summarize(self, dataframe,
                    round_digits=4,
                    feature_numbers=True,
                    missing_col=True,
                    output_type='html',
                    output_file='summary.html',
                    append=True):
        self.df = dataframe
        self.round_digits = round_digits
        self.feature_numbers = feature_numbers
        self.missing_col = missing_col
        self.output_type = output_type
        self.output_file = output_file
        if self.output_type == 'html':
            self.output_file = str(self.output_file).split('.')[0] + '.html'
        elif self.output_type == 'markdown':
            self.output_file = str(self.output_file).split('.')[0] + '.md'
        elif self.output_type == 'xlsx':
            self.output_file = str(self.output_file).split('.')[0] + '.xlsx'
        self.append = append

        self.summary_cols = []

        if self.feature_numbers is True:
            self.summary_cols.append('Number')

        self.summary_cols.append('Feature')
        self.summary_cols.append('Description')
        self.summary_cols.append('Percent of NotNull')
        self.summary_cols.append('NotNull')

        if self.missing_col is True:
            self.summary_cols.append('Missing')

        self.data_type = self.df.dtypes

        self.row_count = len(self.df)

        self.cols = list(self.df.columns.values)
        self.col_count = len(self.cols)

        self.df_summary = []

        for col_idx in range(0, self.col_count):
            col_summary = self.GetSummaryForColumn(col_idx + 1, self.cols[col_idx])
            self.df_summary.append(col_summary)

        if self.output_type == 'xlsx':
            self.WriteToExcelFile()
        elif self.output_type == 'markdown':
            self.OutputMarkdown()
            self.WriteMarkdownFile()
        elif self.output_type == 'html':
            self.OutputMarkdown()
            self.WriteHtmlFile()


#load dataset and set the name(required)
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pd.read_csv(url, names=names)
dataset.name = 'iris'

#call the method summarize from SummaryDaraFrame-class
proba = SummaryDataFrame()
proba.summarize(dataset, 3, output_type = 'markdown')

proba.summarize(dataset, 3, output_type = 'xlsx')

#pandas to check the Summarizer
dataset.describe()
dataset.info()
dataset.isnull().any()
columns = list(dataset.columns)
for col in columns:
  if dataset[col].dtype =='object':
    print(col, dataset[col].unique(),'unique:' ,len(dataset[col].unique()))
    continue
  print(col, 'uniqie: ',len(dataset[col].unique()))

