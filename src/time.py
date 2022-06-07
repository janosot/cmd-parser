from option_parser import OptionParser, Option

def main():
    parser = OptionParser()

    version_option = Option('V','version')
    version_option.set_description('Print version information on standard output, then exit successfully')

    format_option = Option('f', 'format')
    format_option.set_description('Specify output format, possibly overriding the format specified in the environment variable TIME.')
    format_option.set_parameter_settings(
        parameter_type=str,
        required=True,
        metavar='FORMAT'
    )

    portability_option = Option('p', 'portability')
    portability_option.set_description('Use the portable output format')
    
    output_option = Option('o', 'output')
    output_option.set_description('Do not send the results to stderr, but overwrite the specified file.')
    output_option.set_parameter_settings(
        parameter_type=str,
        required=True,
        metavar='FILE'
    )

    append_option = Option('a', 'append')
    append_option.set_description('(Used together with -o.) Do not overwrite but append.')
    
    verbose_option = Option('v', 'verbose')
    verbose_option.set_description('Give very verbose output about all the program knows about.')

    parser.add_options(
        version_option,
        format_option,
        portability_option,
        output_option,
        append_option,
        verbose_option
    )

    options = parser.parse()

    if(options.is_set(version_option)):
        pass
        ### Code ###
    if(options.is_set(format_option)):
        output_format = options.get_option_parameter(format_option)
        ### Code ###
    if(options.is_set(portability_option)):
        pass
        ### Code ###
    if(options.is_set(output_option)):
        filename = options.get_option_parameter(output_option)
        if(options.is_set(append_option)):
            pass
            ### Code ###
    if(options.is_set(verbose_option)):
        pass
        ### Code ###

if __name__ == '__main__':
    main()
    
    
