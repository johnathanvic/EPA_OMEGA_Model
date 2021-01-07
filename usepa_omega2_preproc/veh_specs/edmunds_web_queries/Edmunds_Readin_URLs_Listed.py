import pandas as pd
import numpy as np
import Edmunds_Interact

working_directory = 'C:/Users/KBolon/Documents/Python/Edmunds_web_vehicle_specs/'
run_controller = pd.read_csv(working_directory+'Edmunds Run Controller'+'.csv')
start_count = 0 #Set to 0 when time permitts
for run_count in range (0,len(run_controller)):
    continued_readin = str(run_controller['Continue Readin'][run_count])
    input_name = str(run_controller['URL Filename'][run_count])
    output_name = str(run_controller['Output Filename'][run_count])
    url_column_name = str(run_controller['URL Column Name'][run_count])
    model_year = str(run_controller['Model Year'][run_count])
    weberror = pd.Series(np.zeros(1), name = 'Website Errors').replace(0,'')
    edmunds_info = pd.read_csv(working_directory+input_name, encoding = "ISO-8859-1")
    edmunds_makes = edmunds_info['Make']
    edmunds_models = edmunds_info['Model']
    url_list = edmunds_info[url_column_name]
    if continued_readin == 'y':
        readin_table = pd.read_csv(working_directory+output_name, encoding = "ISO-8859-1")
        readin_error_models = pd.Series(readin_table['Model'][pd.isnull(readin_table['Readin_Error'])==False]\
            .unique()).reset_index(drop=True)
        final_table = readin_table
        for error_model in readin_error_models:
            print ('Removing ' + str(error_model))
            final_table = final_table[final_table['Model'] != error_model].reset_index(drop=True)
        final_table.to_csv(working_directory + output_name, index=False)
    for url_count in range(start_count,len(url_list)):
        url = url_list[url_count]
        print(str(url_count) + ',' + str(url))
        if continued_readin == 'n' or (continued_readin == 'y' \
                and (final_table['URL']  == url.upper()).sum() == 0 and (final_table['URL']  == url).sum() == 0):
            model = edmunds_models[url_count]
            make = edmunds_makes[url_count]
            original_output_table, readin_check = Edmunds_Interact.Edmunds_Interact(url)
            if type(original_output_table) == str:
                weberror[len(weberror)] = url
                weberror.to_csv(working_directory + 'Non-Functioning Websites_MY'+str(model_year)+'.csv',index=False)
                continue
            categories = original_output_table['Category']
            output_table = original_output_table.drop('Category',axis=1)
            trims_msrp = output_table.columns.str[1:].str.strip()
            try:
                msrp = pd.Series(trims_msrp.str.rsplit('$').str[1].str.strip(), name = 'MSRP')
            except AttributeError:
                msrp = pd.Series(np.zeros(len(trims_msrp)), name = 'MSRP').astype(str)
            trims = pd.Series(trims_msrp.str.rsplit('$').str[0].str.strip(), name='Trims')
            output_table.columns = trims
            new_output_table = output_table.T.reset_index(drop=True)
            new_output_table.columns = categories.str.upper()
            make_info = pd.Series(np.zeros(len(new_output_table)),name = 'Make').replace(0,make)
            model_info = pd.Series(np.zeros(len(new_output_table)),name = 'Model').replace(0,model)
            url_info = pd.Series(np.zeros(len(new_output_table)), name='URL').replace(0, url)
            reformatted_table = pd.concat([make_info, model_info, trims, msrp, url_info, new_output_table],axis=1)\
            .reset_index(drop=True)

            reformatted_table = pd.concat([readin_check,reformatted_table],axis=1)
            reformatted_table_T = reformatted_table.T
            reformatted_table_T2 = reformatted_table_T[~reformatted_table_T.index.duplicated(keep='first')]
            reformatted_table = reformatted_table_T2.T
            #Remove columns with duplicate names and non-duplicate values (They aren't reliable)
            # reformatted_table.to_csv('/Users/Brandon/Desktop/Individual Runs/' + url.replace('/','-')[url.find('.com')+len('.com'):url.find('features-specs')] + '.csv', index=False)
            for column in pd.Series(reformatted_table.columns).unique():
                if (pd.Series(reformatted_table.columns) == column).sum() > 1:
                    reformatted_table = reformatted_table.drop(column,axis=1)
            try:
                non_merge_columns = list(reformatted_table.columns.difference(final_table.columns))
                merge_columns = list(reformatted_table.columns.difference(non_merge_columns))
                final_table = final_table.merge(reformatted_table, how='outer', on=merge_columns).sort_values('URL')
            except NameError:
                final_table = reformatted_table
            except TypeError:
                reformatted_table.to_csv(working_directory + 'Merge Error Table' + '.csv', index=False)
        # raise SystemExit
            final_table.to_csv(working_directory+output_name, index=False)
    final_table['URL'] = final_table['URL'].str.upper()
    final_table = final_table.sort_values('URL')
    final_table.to_csv(working_directory + output_name, index=False)

