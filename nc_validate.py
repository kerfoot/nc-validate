#! /usr/bin/env python
"""Module for comparing NetCDF files against a NetCDF file template"""

from netCDF4 import Dataset
import os
import sys
import argparse

default_nc_template = u'./templates/IOOS_Glider_NetCDF_v2.0.nc'

def main(args):
    """Validate each specified NetCDF file against a NetCDF template and print
    the results STDOUT.  Errors are printed to STDERR."""
    
    if not args.nc_files:
        sys.stderr.write('No NetCDF files specified for validation\n')
        return 1
        
    for nc_file in args.nc_files:
        validated = validate_ioosdac_nc_file(nc_file, nc_template=args.template)
        if validated:
            sys.stdout.write('Valid file: {:s}\n'.format(nc_file))
        else:
            sys.stdout.write('INVALID file: {:s}\n'.format(nc_file))
    
    return 0
            
def validate_ioosdac_nc_file(nc_file, nc_template=default_nc_template):
    """Validate the NetCDF file against the nc_template NetCDF file.
    
    The specified nc_file is compared against the default_nc_template, which
    should be a NetCDF file fully conforming to the IOOS National Glider Data
    Assembly Center specification.
    """
    
    validated = True
    
    # Make sure the file exists
    if not nc_file:
        sys.stderr.write('No NetCDF file specified for validation.\n')
        sys.stderr.flush()
        return False
    elif not os.path.exists(nc_file):
        sys.stderr.write('Invalid NetCDF file specified: {:s}\n'.format(nc_file))
        sys.stderr.flush()
        return False
    
    sys.stdout.write('Validating file   : {:s}\n'.format(nc_file))
    sys.stdout.write('Validating against: {:s}\n'.format(nc_template))
    sys.stdout.flush()
    
    (nc_path, nc_name) = os.path.split(nc_file)

    # Open up the template and file to validate
    nct = Dataset(nc_template)
    nc = Dataset(nc_file)
    
    # 1. Check global attribures
    global_att_count = 0
    nc_global_atts = nc.ncattrs()
    for att in nct.ncattrs():
        if att not in nc_global_atts:
            sys.stderr.write(' GlobalAttributeError: Missing global attribute: {:s}\n'.format(
                att))
            sys.stderr.flush()
            continue
            
        global_att_count += 1
            
    # 1. Check dimensions
    nc_dim_count = 0
    nc_dim_names = nc.dimensions.keys()
    for dim in nct.dimensions.keys():
        if dim not in nc_dim_names:
            sys.stderr.write(' DimensionEror: Missing dimension: {:s}\n'.format(
                dim))
            sys.stderr.flush()
            validated = False
            continue
            
        nc_dim_count += 1
        
    # 2. Check variables
    nc_var_count = 0
    nc_var_names = nc.variables.keys()
    for var in nct.variables.keys():
        if var not in nc_var_names:
            sys.stderr.write(' VariableError: Missing variable: {:s}\n'.format(
                var))
            sys.stderr.flush()
            validated = False
            continue
        
        # Store reference to current variable
        nc_var = nc.variables[var]
        # Store reference to template variable
        nct_var = nct.variables[var]
        
        # Check datatype
        if nc_var.dtype != nct_var.dtype:
            sys.stderr.write('  VariableError: Incorrect datatype for {:s} ({:s}!={:s})\n'.format(
                var,
                nc_var.dtype.type,
                nct_var.dtype.type))
            sys.stderr.flush()
            validated = False
        
        # Check variable dimension
        if nct.variables[var].dimensions != nc.variables[var].dimensions:
            sys.stderr.write('  VariableError: Incorrect dimension for {:s} ({:s}!={:s}\n'.format(
                var,
                str(nct.variables[var].dimensions),
                str(nc.variables[var].dimensions)))
            validated = False
        
        # Check variable attributes
        nc_var_atts = nc.variables[var].ncattrs()
        for var_att in nct.variables[var].ncattrs():
            if var_att not in nc_var_atts:
                sys.stderr.write('   VariableError: Missing attribute for {:s}: {:s}\n'.format(
                    var,
                    var_att))
                sys.stderr.flush()
                validated = False                
                
    sys.stdout.write('{:d}/{:d} required global attributes validated\n'.format(
        global_att_count,
        len(nct.ncattrs())))
    sys.stdout.write('{:d}/{:d} required dimensions validated\n'.format(
        nc_dim_count,
        len(nct.dimensions)))
    sys.stdout.flush()
    
    return validated
    
if __name__ == '__main__':
    
    arg_parser = argparse.ArgumentParser(description=main.__doc__)
    arg_parser.add_argument('nc_files',
        nargs='*',
        default=[],
        help='One or more NetCDF files to parse')
    arg_parser.add_argument('-t', '--template',
        default=default_nc_template,
        help='Alternate template to validate against (Default={:s}'.format(default_nc_template))
    args = arg_parser.parse_args()

    main(args)
    
    
