import pandas as pd
from csv import reader, writer


def save_file(session_settings, df, save_folder, file_id, effects_log, extension='parquet'):
    """

    Args:
        session_settings: an instance of the SessionSettings class.
        df: the DataFrame to be saved.
        save_folder: a Path instance for the save folder.
        file_id (str): file identifier to be included in the saved filename.
        effects_log: an instance of the EffectsLog class.
        extension (str): entered in runtime_options.csv (either 'csv' or 'parquet' with 'parquet' the default)

    Returns:
        The passed dict_to_save as a DataFrame while also saving that DataFrame to the save_folder.

    """
    filepath = save_folder / f'{session_settings.session_name}_{file_id}.{extension}'

    if extension not in ['csv', 'parquet']:
        effects_log.logwrite(f'Improper extension provided when attempting to save {file_id} file.')
    if extension == 'parquet':
        df.to_parquet(filepath, engine='fastparquet', compression='snappy', index=False)
    else:
        df.to_csv(filepath, index=False)


def add_id_to_csv(filepath, output_file_id_info):
    """

    Args:
        filepath: the Path object to the file.
        output_file_id_info (list): a list of string info to include as output file identifiers.

    Returns:
        Nothing, but reads the appropriate input file, inserts a new first row and saves the output_file_id_info in that
        first row.

    """

    with open(filepath, 'r') as read_file:
        rd = reader(read_file)
        lines = list(rd)
        lines.insert(0, output_file_id_info)

    with open(filepath, 'w',newline='') as write_file:
        wt = writer(write_file)
        wt.writerows(lines)

    read_file.close()
    write_file.close()
