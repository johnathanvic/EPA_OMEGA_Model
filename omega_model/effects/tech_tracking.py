"""

Functions to track vehicle technology use.


----

**CODE**

"""


def calc_tech_tracking(calendar_years):

    """

    Args:
        calendar_years: The calendar years for which to generate tech tracking data.

    Returns:
        A dictionary of key, value pairs where the key is a tuple (vehicle_id, calendar_year, age) and the value is a dictionary of key, value pairs providing
        vehicle attributes (e.g., model_year, reg_class_id, in_use_fuel_id, etc.) and tech attributes (e.g., 'gdi', 'turb11', etc.) and their attribute values.

    """
    from producer.vehicle_annual_data import VehicleAnnualData
    from producer.vehicles import VehicleFinal
    from producer.vehicles import DecompositionAttributes

    tech_flag_list = DecompositionAttributes.other_values + DecompositionAttributes.offcycle_values
    id_attribute_list = ['name', 'manufacturer_id', 'model_year', 'base_year_reg_class_id', 'reg_class_id',
                         'in_use_fuel_id', 'target_co2e_grams_per_mile']

    new_vehicle_info_dict = dict()
    new_vehicle_tech_flag_dict = dict()
    tech_tracking_dict = dict()
    for calendar_year in calendar_years:
        vads = VehicleAnnualData.get_vehicle_annual_data(calendar_year)

        for vad in vads:

            vehicle_id, age, registered_count = vad.vehicle_id, vad.age, vad.registered_count
            key = vehicle_id, int(calendar_year), int(age)

            if vehicle_id not in new_vehicle_info_dict:
                new_vehicle_info_dict[vehicle_id] = VehicleFinal.get_vehicle_attributes(vehicle_id, id_attribute_list)

            name, mfr_id, model_year, base_year_reg_class_id, reg_class_id, in_use_fuel_id, \
            target_co2e_grams_per_mile \
                = new_vehicle_info_dict[vehicle_id]

            if target_co2e_grams_per_mile is not None:

                tech_tracking_dict[key] = {'calendar_year': int(calendar_year),
                                           'model_year': model_year,
                                           'age': int(age),
                                           'name': name,
                                           'manufacturer_id': mfr_id,
                                           'base_year_reg_class_id': base_year_reg_class_id,
                                           'reg_class_id': reg_class_id,
                                           'in_use_fuel_id': in_use_fuel_id,
                                           'registered_count': registered_count,
                                           }

                if vehicle_id not in new_vehicle_tech_flag_dict:
                    new_vehicle_tech_flag_dict[vehicle_id] = dict()
                    tech_flag_values = VehicleFinal.get_vehicle_attributes(vehicle_id, tech_flag_list)
                    for idx, tech_flag in enumerate(tech_flag_list):
                        new_vehicle_tech_flag_dict[vehicle_id].update({tech_flag: tech_flag_values[idx]})

                # calc volumes and weight flags
                for tech_flag, tech_flag_value in new_vehicle_tech_flag_dict[vehicle_id].items():
                    if tech_flag_value is None:
                        tech_tracking_dict[key].update({f'{tech_flag}_volume': tech_flag_value})
                    elif tech_flag == 'curb_weight':
                        tech_tracking_dict[key].update({tech_flag: tech_flag_value})
                        tech_tracking_dict[key].update({'fleet_pounds': tech_flag_value * registered_count})
                    elif tech_flag == 'weight_reduction':
                        tech_tracking_dict[key].update({tech_flag: tech_flag_value})
                    else:
                        tech_tracking_dict[key].update({f'{tech_flag}_volume': tech_flag_value * registered_count})

                # calc shares
                for tech_flag, tech_flag_value in new_vehicle_tech_flag_dict[vehicle_id].items():
                    if tech_flag_value is None:
                        tech_tracking_dict[key].update({f'{tech_flag}_share': tech_flag_value})
                    elif tech_flag == 'curb_weight':
                        pass
                    elif tech_flag == 'weight_reduction':
                        pass
                    else:
                        tech_tracking_dict[key].update({f'{tech_flag}_share': tech_flag_value})
                    
    return tech_tracking_dict
