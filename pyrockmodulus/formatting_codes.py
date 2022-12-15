# /////////////////////////////////////////////////////////////// #
# !python3.6
# -*- coding: utf-8 -*-
# Compiled by Aly @ Grasselli Geomechanics Group, UofT, 2019 
# Created using PyCharm
# /////////////////////////////////////////////////////////////// #


def calc_timer_values(end_time):
    """
    Function to calculate the time

    :param end_time: Time (Difference in time in seconds)
    :type end_time: float

    :return: Time in minutes and seconds
    :rtype: float
    """

    minutes, sec = divmod(end_time, 60)
    if end_time < 60:
        return ("\033[1m%.2f seconds\033[0m" % end_time)
    else:
        return ("\033[1m%d minutes and %d seconds\033[0m." % (minutes, sec))


def red_text(val):
    """
    Returns text as bold in red font color

    :param val: Text
    :type val: str

    :return: Text as bold in red font color
    :rtype: str
    """

    tex = "\033[1;31m%s\033[0m" % val
    return tex


def green_text(val):
    """
    Returns text as bold in green font color

    :param val: Text
    :type val: str

    :return: Text as bold in green font color
    :rtype: str
    """

    tex = "\033[1;92m%s\033[0m" % val
    return tex


def bold_text(val):
    """
    Returns text as bold

    :param val: Text
    :type val: str

    :return: Text as bold
    :rtype: str
    """

    tex = "\033[1m%s\033[0m" % val
    return tex


def docstring_creator(df):
    """
    Write the example output for a docstring DataFrame

    :param df: DataFrame to be read
    :type df: pandas.DataFrame

    :return: prints the docstring and type for each element in the DataFrame
    :rtype: str
    """

    docstring = 'Index:\n'
    docstring = docstring + f'    {df.index}\n'
    docstring = docstring + 'Columns:\n'
    for col in df.columns:
        docstring = docstring + f'    Name: {df[col].name}, dtype={df[col].dtype}, nullable: {df[col].hasnans}\n'
        print(docstring)


def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=50):
    """
    Call in a loop to create terminal progress bar
    Adjusted bar length to 50, to display on small screen

    :param iteration: current iteration
    :type iteration: int
    :param total: total iteration
    :type total: int
    :param prefix: prefix string
    :type prefix: str
    :param suffix: suffix string
    :type suffix: str
    :param decimals: positive number of decimals in percent complete
    :type decimals: int
    :param bar_length: character length of bar
    :type bar_length: int

    :return: system output showing progress
    :rtype:
    """

    import sys

    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(bar_length * (100. / bar_length) * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '/' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


if __name__ == "__main__":
    try:
        text = "Hello World"
        red_text(text)
        green_text(text)
        bold_text(text)
    except KeyboardInterrupt:
        exit("TERMINATED BY USER")

