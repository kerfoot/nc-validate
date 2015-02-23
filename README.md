Quick & Dirty NetCDF File Validation
====================================

A python module for comparing one or more NetCDF files against a known NetCDF
template.  Results are printed to STDOUT and errors (i.e.: missing dimensions,
variables, global and variable attributes) are printed to STDERR.

The comparison is very simple.  The template file is read and then compared to
the structure of each of the files specified on the command line.  Data
integrity is <b>NOT</b> checked.

Type:

    > nc_validate -h

for usage.

The module may be executed from the command line.  If run this way, the
specified files are compared to the template file contained in:

    ./templates/IOOS_Glider_NetCDF_v2.0.nc

If you would like to change the file against which the specified files are
compared, you can do one of the following:

- Use the -t or --template option and specify the location of the template
file.

Run the script like this:

    > nc_validate.py --template PATH_TO_TEMPLATE FILE1[, FILE2, ...]

- Put the file somewhere and specify it's location in the <b>default_nc_template</b> variable (line #9).

Then run the script like this:

    > nc_validate.py FILE1[, FILE2, ...]

